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


class Topic(StructuredNode):
    name = StringProperty(unique_index=True)

    def delete_if_orphan(self):
        count = db.cypher_query(
            f"MATCH p=(t:Topic{{name: '{self.name}'}})-[r:TAGGED_WITH]-(a) RETURN count(p)"
        )[0][0][0]

        if count == 0:
            self.delete()
