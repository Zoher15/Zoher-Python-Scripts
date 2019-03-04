//1 Import
CREATE INDEX ON :Resource(uri)//prestep
CALL semantics.importRDF("file:///C:/Users/zoya/Downloads/claimreviews_db.rdf","RDF/XML", { shortenUrls: false, typesToLabels: true, commitSize: 9000 })
//2 Delete POS relationships and nodes
MATCH (n)-[r:`http://www.ontologydesignpatterns.org/ont/fred/pos.owl#pennpos`]->(v) delete r,v
//TRICKY
MATCH (n)-[r:`http://www.ontologydesignpatterns.org/ont/fred/pos.owl#boxerpos`]->(v) where v.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/pos.owl'
MATCH (v)-[r1]->(m)
return v,r1,m
OPTIONAL MATCH (m)-[r1]->(o)
delete r,v
//3 labeling the nodes
MATCH (n) with n, SPLIT(n.uri,"/")[-1] as name SET n.label=name return n.label
MATCH (n) with n, SPLIT(n.label,"#")[-1] as name SET n.label=name return n.label
//4 labling the relationships
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
//
MATCH ()-[r:`http://www.w3.org/2002/07/owl#sameAs`]->()
delete r

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
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(n)
delete r
//
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(m) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node
//
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#hasInterpretant`]->(n)
delete r

//8 merging nodes with denotes relationships
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#denotes`]->(m) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:"overwrite",mergeRels:true}) yield node
return node
//
MATCH (n)-[r:`http://ontologydesignpatterns.org/cp/owl/semiotics.owl#denotes`]->(n)
delete r
//9 Delete refer to claim
MATCH (n)-[r]-(m:`http://www.essepuntato.it/2008/12/earmark#StringDocuverse`) delete r,m
//10 Delete refer to quanitifiers,determiners and quality
MATCH ()-[r:`http://www.ontologydesignpatterns.org/ont/fred/quantifiers.owl#hasQuantifier`]->(m)
OPTIONAL MATCH (m)-[r1]->(o)
delete r1,o,r,m
//
MATCH ()-[r:`http://www.ontologydesignpatterns.org/ont/fred/quantifiers.owl#hasDeterminer`]->(m)
OPTIONAL MATCH (m)-[r1]->(o)
delete r1,o,r,m
//11. Delete references to event
MATCH ()-[r]->(m{uri:'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#Event'})
delete r,m
//12. Delete possible type relationships and nodes
MATCH ()-[r:`http://www.ontologydesignpatterns.org/ont/boxer/boxer.owl#possibleType`]->(m)
delete r,m