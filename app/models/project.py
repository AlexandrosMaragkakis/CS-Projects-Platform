from neomodel import (  # type: ignore
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    Relationship,
    IntegerProperty,
)
from neomodel import db  # type: ignore


class Project(StructuredNode):
    uid = UniqueIdProperty()
    github_id = IntegerProperty(unique_index=True)
    github_url = StringProperty(unique_index=True)
    title = StringProperty()
    description = StringProperty()

    tagged_with = Relationship("Topic", "TAGGED_WITH")
