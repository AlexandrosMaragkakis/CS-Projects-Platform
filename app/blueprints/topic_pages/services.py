from app.blueprints.project_submissions.models import Project, Topic
from neomodel import db  # type: ignore


def get_topic_info(topic_name):
    topic = Topic.nodes.get_or_none(name=topic_name)

    if topic is None:
        raise ValueError(f"Topic {topic_name} not found")

    # Get the total number of projects in the topic
    total_projects = db.cypher_query(
        f"MATCH p=(t:Topic{{name: '{topic_name}'}})-[r:TAGGED_WITH]-(a) RETURN count(p)"
    )[0][0][0]

    # Get the total number of unique students who worked on projects in the topic
    unique_students = db.cypher_query(
        f"MATCH p=(t:Topic{{name: '{topic_name}'}})-[r:SKILLED_IN]-(s:Student) RETURN count(distinct s)"
    )[0][0][0]

    # Get the students who are skilled in the topic
    students = db.cypher_query(
        f"MATCH p=(t:Topic{{name: '{topic_name}'}})-[r:SKILLED_IN]-(s:Student) \
          RETURN s.full_name, s.username"
    )[0]

    # log students to file
    with open("students.txt.tmp", "a") as f:
        f.write(str(students) + "\n")
    with open("total_projects.txt.tmp", "a") as f:
        f.write(str(total_projects) + "\n")
    with open("unique_students.txt.tmp", "a") as f:
        f.write(str(unique_students) + "\n")

    return total_projects, unique_students, students


def get_all_topics():
    topics = Topic.nodes.all
    return [topic.name for topic in topics]
