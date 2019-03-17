MATCH (n) DETACH DELETE n
MATCH (n)-[r]-(m) Return n,r,m
//1 Import
CREATE INDEX ON :Resource(uri);//prestep
//CALL semantics.importRDF("file:///C:/Users/zoya/Downloads/claimreviews_db.rdf","RDF/XML", { shortenUrls: false, typesToLabels: false, commitSize: 25000 })
CALL semantics.importRDF("file:///gpfs/home/z/k/zkachwal/Carbonate/Downloads/claimreviews_db.rdf","RDF/XML", { shortenUrls: false, typesToLabels: false, commitSize: 25000 });

//2 labeling the nodes
MATCH (n) with n, SPLIT(n.uri,"/")[-1] as name SET n.label=name;
MATCH (n) with n, SPLIT(n.label,"#")[-1] as name SET n.label=name;
//3 labeling the relationships
MATCH ()-[r]-() with r, SPLIT(type(r),"/")[-1] as name SET r.label=name;
MATCH ()-[r]-() with r, SPLIT(r.label,"#")[-1] as name SET r.label=name;
//4 merging nodes with sameAs relationships
MATCH (n)-[r1:`http://www.w3.org/2002/07/owl#sameAs`]->(m) where m.uri starts with 'http://dbpedia.org/resource/' and toLower(n.label)=toLower(m.label) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//5 merging nodes with equivalentClass relationships
MATCH (n)-[r1:`http://www.w3.org/2002/07/owl#equivalentClass`]->(m) where m.uri starts with 'http://dbpedia.org/resource/' and toLower(n.label)=toLower(m.label) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//6 merging verbs like show_1 and show_2 with show
MATCH (n)-[r{label:'type'}]->(m) where split(n.label,'_')[0]=toLower(m.label) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
////Merging verbs with their verbnet forms
MATCH (n)-[r{label:'equivalentClass'}]->(m) where split(m.label,'_')[0]=n.label with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//Set new neo4j labels
MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'}) set n:trump;
MATCH (n{uri:'http://dbpedia.org/resource/Hillary_Clinton'}) set n:hillary;

MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'}) remove n:claim5005;
MATCH (n{uri:'http://dbpedia.org/resource/Hillary_Clinton'}) remove n:claim5005;




//7 add degree to the nodes
MATCH (n)-[r]-(m)
WITH n, count(m) as c, collect(r) as rs
UNWIND rs as r
set n.degree=log(c);
// and relationships
MATCH (n)-[r]-(m)
WITH n,m, collect(r) as rs
UNWIND rs as r
set r.degree=(n.degree+m.degree)/2;

//8 calculate shortest paths
MATCH (start{uri:'http://dbpedia.org/resource/Donald_Trump'}), (end{uri:'http://dbpedia.org/resource/Vladimir_Putin'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost
//Query and delete the ssp nodes
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n

//9 DB Pedia Ego Network of Donald_Trump
MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'})-[r*1..2]-(m)  where m.uri starts with 'http://dbpedia.org/resource/' Return n,r,m

