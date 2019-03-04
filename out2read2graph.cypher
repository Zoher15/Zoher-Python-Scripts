
#Construct Graph
LOAD CSV WITH HEADERS 
FROM "file:///simpleout1.csv"  
AS network
MERGE (arg1:Node {id:network.`Argument 1`})
MERGE (arg2:Node {id:network.`Argument(s) 2`})
WITH arg1,arg2,network
CALL apoc.create.relationship(arg1, network.`Relation`, {}, arg2) yield rel
RETURN arg1,rel,arg2

#Delete
MATCH (n)
DETACH DELETE n