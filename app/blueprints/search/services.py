from app.blueprints.project_submissions.models import Project, Topic
from app.blueprints.auth.models import Student
from neomodel import db  # type: ignore


def search_by_topic_(topic_name):
    topic = Topic.nodes.get_or_none(name=topic_name)

    if topic is None:
        raise ValueError(f"Topic {topic_name} not found")

    projects = Project.nodes.all()
    projects = [p for p in Project.nodes.all() if topic in p.tagged_with.all()]
    with open("search_by_topic.txt.tmp", "a") as f:
        f.write(str(projects) + "\n")
    return projects


def get_available_topics():
    topics = Topic.nodes.all()
    return [topic.name for topic in topics]


def find_topics(search_term):

    try:
        query = """
        CALL db.index.fulltext.queryNodes('topicsFulltextIndex', $search_term)
        YIELD node, score
        RETURN node.name AS topic, score
        ORDER BY score DESC
        """

        # fuzzy search
        results = db.cypher_query(query, {"search_term": search_term + "~"})

        # log results to file
        with open("search_results.txt.tmp", "a") as f:
            f.write(str(results) + "\n")
        # Convert to list of dictionaries for easy JSON serialization
        matched_topics = [
            {"name": topic, "score": score} for topic, score in results[0] if score > 0
        ]
        # log matched_topics to file
        with open("matched_topics.txt.tmp", "a") as f:
            f.write(str(matched_topics) + "\n")

        return matched_topics
    except Exception as e:
        raise ValueError(f"Error finding matching topics: {str(e)}")


def find_users(search_term):

    # log query to file
    with open("search_query.txt.tmp", "a") as f:
        f.write(search_term + "\n")
    try:
        query = """
        CALL db.index.fulltext.queryNodes('studentsFulltextIndex', $search_term)
        YIELD node, score
        RETURN node.full_name AS name,
               node.github_username AS github_username,
               node.username AS username,
               node.uid AS uid,
               score
        ORDER BY score DESC
        """

        # fuzzy search
        results = db.cypher_query(query, {"search_term": search_term + "~"})

        # log results to file
        with open("search_results.txt.tmp", "a") as f:
            f.write(str(results) + "\n")

        # Convert to list of dictionaries for easy JSON serialization
        users_data = [
            {
                "name": name,
                "github_username": github_username,
                "username": username,
                "uid": uid,
                "score": score,
            }
            for name, github_username, username, uid, score in results[0]
            if score > 0
        ]
        # log users_data to file
        with open("users_data.txt.tmp", "a") as f:
            f.write(str(users_data) + "\n")

        return users_data
    except Exception as e:
        raise ValueError(f"Error finding users: {str(e)}")


def find_projects(search_term):

    try:
        query = """
        CALL db.index.fulltext.queryNodes('projectsFulltextIndex', $search_term)
        YIELD node, score
        WITH node, score
        MATCH (s:Student)-[:WORKED_IN]-(node)
        RETURN s.full_name AS full_name, s.username AS username, node.title AS title,
               node.github_url AS github_url, score
        ORDER BY score DESC
        """

        # fuzzy search, must see if ~ works for entire string or just the last word
        results = db.cypher_query(query, {"search_term": search_term + "~"})

        # log results to file
        with open("search_results.txt.tmp", "a") as f:
            f.write(str(results) + "\n")

        # Convert to list of dictionaries for easy JSON serialization
        projects_data = [
            {
                "full_name": full_name,
                "username": username,
                "title": title,
                "github_url": github_url,
                "score": score,
            }
            for full_name, username, title, github_url, score in results[0]
            if score > 0
        ]
        # log projects_data to file
        with open("projects_data.txt.tmp", "a") as f:
            f.write(str(projects_data) + "\n")

        return projects_data
    except Exception as e:
        raise ValueError(f"Error finding projects: {str(e)}")
