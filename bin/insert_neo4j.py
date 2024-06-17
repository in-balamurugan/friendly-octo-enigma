from neo4j import GraphDatabase
import neo4j.time

class Neo4jChecker:

    def __init__(self, uri):
        self.driver = GraphDatabase.driver(uri)

    def close(self):
        self.driver.close()

    def add_person_and_relationship(self, person_data, relationship_data=None):
        with self.driver.session() as session:
            session.execute_write(self._create_person_and_relationship, person_data, relationship_data)

    @staticmethod
    def _create_person_and_relationship(tx, person_data, relationship_data):
        # Create the person node
        query = (
            "MERGE (p:Person {name: $name, dateOfBirth: $dateOfBirth}) "
            "RETURN p"
        )
        result = tx.run(query, name=person_data["properties"]["name"], dateOfBirth=person_data["properties"]["dateOfBirth"])
        person_node = result.single()["p"]

        # Create the relationship if data is provided
        if relationship_data:
            query = (
                "MATCH (a:Person {name: $existing_person_name}), (b:Person {name: $new_person_name}) "
                "MERGE (a)-[r:%s {date: $relationship_date}]->(b) "
                "RETURN r" % relationship_data["type"]
            )
            tx.run(query, 
                   existing_person_name=relationship_data["existing_person_name"], 
                   new_person_name=person_data["properties"]["name"], 
                   relationship_date=relationship_data["date"])

# Example usage:
if __name__ == "__main__":
    uri = "bolt://localhost:7687"  # Change this to your Neo4j URI

    checker = Neo4jChecker(uri)



    checker.close()