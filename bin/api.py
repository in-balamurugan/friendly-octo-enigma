from fastapi import FastAPI, HTTPException, Body
from sqlmodel import SQLModel
from neo4j import GraphDatabase
import neo4j.time
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Neo4jChecker:

    def __init__(self, uri):
        self.driver = GraphDatabase.driver(uri)

    def close(self):
        self.driver.close()

    def add_person_with_optional_relationship(self, person_data, existing_person_name=None, relationship_type=None, relationship_date=None):
        with self.driver.session() as session:
            return session.execute_write(self._create_person_and_relationship, person_data, existing_person_name, relationship_type, relationship_date)

    def view_persons_and_relationships(self):
        with self.driver.session() as session:
            print( session.execute_read(self._view_persons_and_relationships))
            return session.execute_read(self._view_persons_and_relationships)

    @staticmethod
    def _create_person_and_relationship(tx, person_data, existing_person_name, relationship_type, relationship_date):
        query = (
            "CREATE (p:Person {name: $name, dateOfBirth: $dateOfBirth}) "
            "RETURN p"
        )
        result = tx.run(query, name=person_data["properties"]["name"], dateOfBirth=person_data["properties"]["dateOfBirth"])
        person_node = result.single()["p"]
        return person_node

    @staticmethod
    def _view_persons_and_relationships(tx):
        query = (
            "MATCH (a:Person)-[r]->(b:Person) "
            "RETURN a.name AS from, type(r) AS relationship, r.date AS date, b.name AS to "
            "UNION "
            "MATCH (p:Person) "
            "WHERE NOT (p)--() "
            "RETURN p.name AS from, NULL AS relationship, NULL AS date, NULL AS to"
        )
        result = tx.run(query)
        return [record for record in result]

class PersonData(SQLModel):
    name: str
    dateOfBirth: str

uri = "bolt://localhost:7687"
neo4j_checker = Neo4jChecker(uri)

@app.post("/add_person/")
def add_person(person_data: PersonData = Body(...)):
    person_dict = {
        'element_id': '1',
        'labels': frozenset({'Person'}),
        'properties': {
            'name': person_data.name,
            'dateOfBirth': neo4j.time.Date.fromisoformat(person_data.dateOfBirth)
        }
    }

    try:
        neo4j_checker.add_person_with_optional_relationship(person_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success"}

@app.get("/view_persons/")
def view_persons():
    try:
        persons = neo4j_checker.view_persons_and_relationships()
        return persons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
