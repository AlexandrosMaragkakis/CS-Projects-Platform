from neomodel import (  # type: ignore
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    EmailProperty,
    Relationship,
)

from flask_login import UserMixin  # type: ignore


class User(StructuredNode, UserMixin):

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
    github_username = StringProperty(unique_index=True)
    github_token = StringProperty(unique_index=True)
    worked_in = Relationship(
        "app.blueprints.project_submissions.models.Project", "WORKED_IN"
    )
    skilled_in = Relationship(
        "app.blueprints.project_submissions.models.Topic", "SKILLED_IN"
    )
    # interested_in = Relationship(
    #    "app.blueprints.project_submissions.models.Topic", "INTERESTED_IN"
    # )

    def get_projects(self):
        return self.worked_in.all()

    def get_topics(self):
        return self.skilled_in.all()


class Company(User):
    company_name = StringProperty(unique_index=True)
