from neomodel import (  # type: ignore
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    Relationship,
)


class Project(StructuredNode):
    uid = UniqueIdProperty()
    github_url = StringProperty(unique_index=True)
    title = StringProperty()
    description = StringProperty()

    tagged_with = Relationship("Topic", "TAGGED_WITH")


class Topic(StructuredNode):
    name = StringProperty(unique_index=True)
