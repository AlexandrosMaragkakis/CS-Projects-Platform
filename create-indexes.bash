#!/bin/bash

# Wait for Neo4j to be fully up and running
sleep 15

# Create indexes using Cypher commands
cypher-shell -u neo4j -p test1234 <<EOF
CREATE FULLTEXT INDEX topicsFulltextIndex IF NOT EXISTS FOR (n:Topic) ON EACH [n.name];
CREATE FULLTEXT INDEX studentsFulltextIndex IF NOT EXISTS FOR (n:Student) ON EACH [n.full_name];
CREATE FULLTEXT INDEX projectsFulltextIndex IF NOT EXISTS FOR (n:Project) ON EACH [n.title, n.description];
EOF
