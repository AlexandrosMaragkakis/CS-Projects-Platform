#!/bin/bash

# Wait for Neo4j to be fully up and running
sleep 15
echo "Creating indexes and constraints..."
# Create indexes and constraints using Cypher commands
cypher-shell -u neo4j -p test1234 <<EOF
CREATE FULLTEXT INDEX topicsFulltextIndex IF NOT EXISTS FOR (n:Topic) ON EACH [n.name];
CREATE FULLTEXT INDEX studentsFulltextIndex IF NOT EXISTS FOR (n:Student) ON EACH [n.full_name];
CREATE FULLTEXT INDEX projectsFulltextIndex IF NOT EXISTS FOR (n:Project) ON EACH [n.title, n.description];
CREATE CONSTRAINT unique_topic_name IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE;
CREATE CONSTRAINT unique_project_github_id IF NOT EXISTS FOR (p:Project) REQUIRE p.github_id IS UNIQUE;
CREATE CONSTRAINT unique_user_email IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE;
CREATE CONSTRAINT unique_student_github_username IF NOT EXISTS FOR (s:Student) REQUIRE s.github_username IS UNIQUE;
CREATE CONSTRAINT unique_student_github_token IF NOT EXISTS FOR (s:Student) REQUIRE s.github_token IS UNIQUE;
CREATE CONSTRAINT unique_company_name IF NOT EXISTS FOR (c:Company) REQUIRE c.company_name IS UNIQUE;
CREATE CONSTRAINT unique_github_project_url IF NOT EXISTS FOR (p:Project) REQUIRE p.github_url IS UNIQUE;
CREATE CONSTRAINT unique_uid IF NOT EXISTS FOR (u:User) REQUIRE u.uid IS UNIQUE;
CREATE CONSTRAINT unique_project_uid IF NOT EXISTS FOR (p:Project) REQUIRE p.uid IS UNIQUE;
EOF
echo "Indexes and constraints created."