from app.models.project import Project
from app.models.user import Student
from app.models.topic import Topic
from neomodel import db  # type: ignore

# TODO: find_* functions have a lot of duplicated code, consider refactoring


def search_by_topic_(topic_name):
    topic = Topic.nodes.get_or_none(name=topic_name)

    if topic is None:
        raise ValueError(f"Topic {topic_name} not found")

    # projects = Project.nodes.all()
    projects = [p for p in Project.nodes.all() if topic in p.tagged_with.all()]
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

        # Convert to list of dictionaries for easy JSON serialization
        matched_topics = [
            {"name": topic, "score": score} for topic, score in results[0] if score > 0
        ]

        return matched_topics
    except Exception as e:
        raise ValueError(f"Error finding matching topics: {str(e)}")


def find_users(search_term):

    try:
        query = """
        CALL db.index.fulltext.queryNodes('studentsFulltextIndex', $search_term)
        YIELD node, score
        RETURN node.full_name AS name,
               node.github_username AS github_username,
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
                "uid": uid,
                "score": score,
            }
            for name, github_username, uid, score in results[0]
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
        RETURN s.full_name AS full_name, s.uid AS uid, node.title AS title,
               node.github_url AS github_url, score
        ORDER BY score DESC
        """

        # fuzzy search, must see if ~ works for entire string or just the last word
        results = db.cypher_query(query, {"search_term": search_term + "~"})

        # Convert to list of dictionaries for easy JSON serialization
        projects_data = [
            {
                "full_name": full_name,
                "uid": uid,
                "title": title,
                "github_url": github_url,
                "score": score,
            }
            for full_name, uid, title, github_url, score in results[0]
            if score > 0
        ]
        # log projects_data to file
        with open("projects_data.txt.tmp", "a") as f:
            f.write(str(projects_data) + "\n")

        return projects_data
    except Exception as e:
        raise ValueError(f"Error finding projects: {str(e)}")
