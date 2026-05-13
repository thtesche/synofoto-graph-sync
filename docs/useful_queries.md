# Useful Graph Queries (Cypher)

Use these queries with the `scripts/query_graph.py` tool or in the Memgraph/Neo4j Browser.

## 1. Database Inventory
Check how many nodes of each type exist in your database.
```cypher
MATCH (n) 
RETURN labels(n) as labels, count(n) as count
```

## 2. Relationship Statistics
See how your data is connected.
```cypher
MATCH ()-[r]->() 
RETURN type(r) as relationship, count(r) as count
```

## 3. Location Search (Recursive)
Find all photos within a specific country (e.g., Deutschland), including all its sub-locations (States, Cities, Streets).
```cypher
MATCH (l:Location {name: 'Deutschland'})<-[:PART_OF*0..]-(loc)<-[:LOCATED_AT]-(p:Photo) 
RETURN count(p) as total_photos
```

## 4. Sampling Photos with Locations
Get a quick look at the latest imported photos and their most specific location.
```cypher
MATCH (p:Photo)-[:LOCATED_AT]->(l:Location) 
RETURN p.filename, l.name 
LIMIT 10
```

## 5. Finding People and their Families
```cypher
MATCH (per:Person)-[:BELONGS_TO_FAMILY]->(f:Family)
RETURN per.name, f.name
```

## 6. Most Frequent Objects (AI Tags)
```cypher
MATCH (obj:Object)<-[:HAS_OBJECT]-()
RETURN obj.name, count(*) as frequency
ORDER BY frequency DESC
LIMIT 20
```
