///Setting Degree
MATCH (n) WITH n,
MATCH (n)-[r]->() with n,r,size((n)-[r]->()) as degree
RETURN degree

MATCH (n) WITH collect(n) as nodes
unwind nodes as node
MATCH (node)-[r]-() with r,size((node)-[r]->()) as degree
SET r.degree=degree
return r.degree

MATCH (n)-[r]->(m)
WITH n, count(m) as c, collect(r) as rs
UNWIND rs as r
set n.outdegree=c
set r.degree=c
RETURN r.degree
///Shortes Path Stream
MATCH (start{uri:'http://dbpedia.org/resource/Donald_Trump'}), (end{uri:'http://dbpedia.org/resource/Barack_Obama'})
CALL algo.shortestPath.stream(start, end, 'degree')
YIELD nodeId, cost
RETURN algo.getNodeById(nodeId).name AS name, cost
///
MATCH (start{uri:'http://dbpedia.org/resource/Donald_Trump'}), (end{uri:'http://dbpedia.org/resource/Vladimir_Putin'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount,totalCost
///Query the sssp
MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'})-[r:sssp]-(m)
RETURN n,r,m
////Get Donald_Trump rels
MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'})-[r]-(m) Return n,r,m LIMIT 20
MATCH (n{uri:'http://dbpedia.org/resource/Barack_Obama'})-[r]-(m) Return n,r,m LIMIT 20
http://dbpedia.org/resource/Barack_Obama
MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'})-[r*1..2]-(m) Return n,r,m LIMIT 50
MATCH a=(n:`schema.org/Person`)-[r*1..3]->(m:`schema.org/Person`) Return a LIMIT 20
MATCH a=(n:`schema.org/Person`)-[r*1..3]->(m:`schema.org/Person`) Return a LIMIT 20
MATCH a=(n{uri:'http://dbpedia.org/resource/Donald_Trump'})-[*1..5]-(m) where m.uri starts with 'http://dbpedia.org/resource/' Return a LIMIT 100
//
MATCH a=(n{uri:'http://dbpedia.org/resource/Donald_Trump'})-[*1..10]->(m{uri:'http://dbpedia.org/resource/Hillary_Clinton'}) Return a LIMIT 10
MATCH (from{uri:'http://dbpedia.org/resource/Donald_Trump'}),(to{uri:'http://dbpedia.org/resource/Hillary_Clinton'}) CALL algo.shortestPath.stream(from, to, "cost") 
yield path as path, cost as cost
return path,cost 
//
MATCH (n) WHERE n.uri = 'http://dbpedia.org/resource/Hillary_Clinton'
CALL apoc.path.subgraphNodes(n, {maxLevel:1,whitelistNodes:"+'http://schema.org/Person'"}) YIELD node
RETURN node
//
MATCH (n{uri:'http://dbpedia.org/resource/Hillary_Clinton'}),(m) where m.uri starts with 'http://dbpedia.org/resource/'
CALL apoc.path.subgraphNodes(n, {maxLevel:10,whitelistNodes:m}) YIELD node
RETURN node
//
MATCH (from{uri:'http://dbpedia.org/resource/Vladimir_Putin'}),(to{uri:'http://dbpedia.org/resource/United_States'}),path = shortestpath((from)-[*]-(to))
with path
WHERE length(path)>2
return path
///Deletions
//1 POS
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/pos.owl' detach delete n
//2 Offsets
//MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/domain.owl#offset' detach delete n
//3 'Thing'
MATCH (n) where n.uri starts with 'http://www.w3.org/2002/07/owl#Thing' detach delete n
//4. 'Event'
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#Event' detach delete n
//5. Quantifiers
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/quantifiers.owl#' detach delete n
//6. Docuverse
MATCH (n:`http://www.essepuntato.it/2008/12/earmark#StringDocuverse`) detach delete n
//7. Self Loops
MATCH (n)-[r]-(n) delete r

//1 Import
CREATE INDEX ON :Resource(uri)//prestep
CALL semantics.importRDF("file:///C:/Users/zoya/Downloads/claimreviews_db.rdf","RDF/XML", { shortenUrls: false, typesToLabels: false, commitSize: 25000 })
//2 labeling the nodes
MATCH (n) with n, SPLIT(n.uri,"/")[-1] as name SET n.label=name return n.label
MATCH (n) with n, SPLIT(n.label,"#")[-1] as name SET n.label=name return n.label
//3 labeling the relationships
MATCH ()-[r]-() with r, SPLIT(type(r),"/")[-1] as name SET r.label=name return r.label
MATCH ()-[r]-() with r, SPLIT(r.label,"#")[-1] as name SET r.label=name return r.label
//5 merging nodes with sameAs relationships
MATCH (n)-[r:`http://www.w3.org/2002/07/owl#sameAs`]->(n)
delete r
//
MATCH (n)-[r1:`http://www.w3.org/2002/07/owl#sameAs`]->(m) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node
//6 merging nodes with equivalentClass relationships
MATCH (n)-[r:`http://www.w3.org/2002/07/owl#equivalentClass`]->(n)
delete r
//
MATCH (n)-[r1:`http://www.w3.org/2002/07/owl#equivalentClass`]->(m) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node
//
MATCH (n)-[r:`http://www.w3.org/2002/07/owl#equivalentClass`]->(n)
delete r

//7 merging nodes with hasInterpretant relationships
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(n) delete r
//
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(m) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/domain.owl#offset' with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node
//
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(n)
delete r

//8 merging nodes with denotes relationships
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#denotes`]->(n)
delete r
//
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#denotes`]->(m) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/domain.owl#offset' with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node
//
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#denotes`]->(n)
delete r
//10 Delete refer to quanitifiers,determiners and quality
MATCH ()-[r:`http://www.ontologydesignpatterns.org/ont/fred/quantifiers.owl#hasQuantifier`]->(m)
OPTIONAL MATCH (m)-[r1]->(o)
delete r1,o,r,m
//
MATCH ()-[r:`http://www.ontologydesignpatterns.org/ont/fred/quantifiers.owl#hasDeterminer`]->(m)
OPTIONAL MATCH (m)-[r1]->(o)
delete r1,o,r,m

MATCH (n) with collect([n,n.uri]) as events
unwind events as event
set event[0].label=semantics.getIRILocalName(event[1])
return event
