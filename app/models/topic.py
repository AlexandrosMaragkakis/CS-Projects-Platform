from neomodel import StructuredNode, StringProperty, db  # type: ignore


class Topic(StructuredNode):
    name = StringProperty(unique_index=True)

    def delete_if_orphan(self):
        count = db.cypher_query(
            f"MATCH p=(t:Topic{{name: '{self.name}'}})-[r:TAGGED_WITH]-(a) RETURN count(p)"
        )[0][0][0]

        if count == 0:
            self.delete()
