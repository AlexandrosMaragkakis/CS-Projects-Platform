from neomodel import (  # type: ignore
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    RelationshipTo,
    EmailProperty,
)

from flask_login import UserMixin  # type: ignore


class User(StructuredNode, UserMixin):
    """Database model for Neo4j"""

    uid = UniqueIdProperty()
    email = EmailProperty(unique_index=True)
    password_hash = StringProperty()
    full_name = StringProperty()

    @staticmethod
    def get_by_id(user_id):
        return User.nodes.get_or_none(uid=user_id)

    @staticmethod
    def get_by_email(email):
        return User.nodes.get_or_none(email=email)

    @staticmethod
    def register_user(
        email,
        password_hash,
        full_name,
    ):
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
        )
        user.save()
        return user

    def get_id(self):
        return self.uid


class Student(User):
    github_username = StringProperty()
    github_token = StringProperty()
    # worked_in_projects = RelationshipTo("Project", "WORKED_IN")
    # interested_topics = RelationshipTo("Topic", "INTERESTED_IN")
    # skilled_topics = RelationshipTo("Topic", "SKILLED_IN")
    pass


class Company(User):
    company_name = StringProperty()
