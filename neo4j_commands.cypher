#Deleting

MATCH (n) DETACH DELETE n
MATCH (n)-[r]-(m) Return n,r,m

#Load CSV
LOAD CSV WITH HEADERS 
FROM "file:///simpleout1.csv"  
AS network
MERGE (arg1:Node {id:network.`Argument 1`})
MERGE (arg2:Node {id:network.`Argument(s) 2`})
WITH arg1,arg2,network
CALL apoc.create.relationship(arg1, network.`Relation`, {}, arg2) yield rel
RETURN arg1,rel,arg2

//Loading RDF
CREATE INDEX ON :Resource(uri)#prestep
CALL semantics.importRDF("file:///claimreviews_db_2_12_10_52AM.rdf","RDF/XML", { shortenUrls: false, typesToLabels: true, commitSize: 9000 })

CALL semantics.importRDF("file:///C:/Users/zoya/Desktop/Zoher/factcheckgraph/claimreviews_db_2_12_10_52AM.rdf","RDF/XML", { shortenUrls: false, typesToLabels: true, commitSize: 9000 })

CALL semantics.importRDF("file:///C:/Users/zoya/Downloads/claimreviews_db.rdf","RDF/XML", { shortenUrls: false, typesToLabels: true, commitSize: 9000 })
CALL semantics.importRDF("file:///C:/Users/zoya/Downloads/4922.rdf","RDF/XML", { shortenUrls: false, typesToLabels: true, commitSize: 9000 })

//Return all nodes and relationships
MATCH (n)-[r]-(m) Return n,r,m

//deleting POS relationships
MATCH (n)-[r:`http://www.ontologydesignpatterns.org/ont/fred/pos.owl#pennpos`]->(v) delete r,v

//replacing word string with child node if there is only one child
MATCH (n)-[r:`http://www.essepuntato.it/2008/12/earmark#refersTo`]->(m),(n)-[r1]->(o) where (exists(n.`http://www.w3.org/2000/01/rdf-schema#label`) and size((n)-[]->())=2)  create (o)-[r2:`http://www.essepuntato.it/2008/12/earmark#refersTo`]->(m) set r2=r delete r,r1,n

//Replacing word string with child node along 'denotes' path
MATCH (n)-[r1:`http://www.ontologydesignpatterns.org/cp/owl/semiotics.owl#denotes`]->(m),(n)-[r2:`http://www.ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(o),(n)-[r3:`http://www.essepuntato.it/2008/12/earmark#refersTo`]->(p),(o)-[]->(q) where exists(n.`http://www.w3.org/2000/01/rdf-schema#label`) 
create (m)-[r4:`http://www.ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(o) set r4=r2
create (m)-[r5:`http://www.essepuntato.it/2008/12/earmark#refersTo`]->(p) set r5=r3 


//labeling the nodes
MATCH (n) with n, SPLIT(n.uri,"/")[-1] as name SET n.label=name return n.label
MATCH (n) with n, SPLIT(n.label,"#")[-1] as name SET n.label=name return n.label

//labling the relationships
MATCH (n)-[r]-(m) with r, SPLIT(type(r),"/")[-1] as name SET r.label=name return r.label

//replacing sameAs and equivalentClass

MATCH (n)-[r1:`http://www.w3.org/2002/07/owl#sameAs`]->(m) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"override",mergeRels:true}) yield node
return node

MATCH (n)-[r1:`http://www.w3.org/2002/07/owl#equivalentClass`]->(m) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"override",mergeRels:true}) yield node
return node

MATCH (n)-[r:`http://www.ontologydesignpatterns.org/ont/vn/abox/role/Theme`]-(m) return n,r,m
