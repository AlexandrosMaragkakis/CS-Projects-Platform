from flask import render_template  # type: ignore
from app.blueprints.topic_pages import topic_bp
from .services import get_topic_info, get_all_topics


@topic_bp.route("/topics/<topic>")
def topic(topic):
    total_projects, unique_students, students = get_topic_info(topic)

    return render_template(
        "topic.html",
        topic=topic,
        total_projects=total_projects,
        unique_students=unique_students,
        students=students,
    )
