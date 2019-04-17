MATCH (n)-[r]-(m) Return n,r,m
MATCH p=(n:dbpedia{uri:'http://dbpedia.org/resource/Hillary_Clinton'})-[*0..1]-(o:dbpedia)-[*0..1]-(m:dbpedia{uri:'http://dbpedia.org/resource/Donald_Trump'}) Return p LIMIT 7

MATCH (n) DETACH DELETE n;
//1 Import
CREATE INDEX ON :Resource(uri);//prestep
//CALL semantics.importRDF('file:///C:/Users/zoya/Downloads/claimreviews_db.rdf','RDF/XML', { shortenUrls: false, typesTolabel_names: false, commitSize: 25000 })
CALL semantics.importRDF('file:///gpfs/home/z/k/zkachwal/Carbonate/Downloads/claimreviews_db.rdf','RDF/XML', { shortenUrls: false, typesTolabel_names: false, commitSize: 100000 });

CALL semantics.importRDF('file:///gpfs/home/z/k/zkachwal/Carbonate/Downloads/falsegraph.rdf','RDF/XML', { shortenUrls: false, typesTolabel_names: false, commitSize: 100000 });

CALL semantics.importRDF('file:///gpfs/home/z/k/zkachwal/Carbonate/Downloads/truegraph.rdf','RDF/XML', { shortenUrls: false, typesTolabel_names: false, commitSize: 100000 });
CALL semantics.importRDF('file:///C:/Users/zoya/Downloads/truegraph.rdf','RDF/XML', { shortenUrls: false, typesTolabel_names: false, commitSize: 100000 });

CALL semantics.importRDF('file:///C:/Users/zoya/Downloads/falsegraph.rdf','RDF/XML', { shortenUrls: false, typesTolabel_names: false, commitSize: 100000 });

CALL semantics.importRDF('file:///gpfs/home/z/k/zkachwal/Carbonate/Downloads/3458.rdf','RDF/XML', { shortenUrls: false, typesTolabel_names: false, commitSize: 100000 });


//1 Add prefix label_names for colors
MATCH (n) where n.uri starts with 'http://www.w3.org/2000/01/rdf-schema#' set n:rdfs;
MATCH (n) where n.uri starts with 'http://www.w3.org/1999/02/22-rdf-syntax-ns#' set n:rdf;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#' set n:dul;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/vn/abox/role/' set n:vnrole;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/vn/' set n:vn;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/boxer/boxing.owl#' set n:boxing;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/boxer/boxer.owl#' set n:boxer;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/d0.owl#' set n:d0;
MATCH (n) where n.uri starts with 'http://schema.org/' set n:schemaorg;
MATCH (n) where n.uri starts with 'http://www.essepuntato.it/2008/12/earmark#' set n:earmark;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/domain.owl#' set n:fred;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/quantifiers.owl#' set n:fredquant;
MATCH (n) where n.uri starts with 'http://www.w3.org/2006/03/wn/wn30/schema/' set n:wn;
MATCH (n) where n.uri starts with 'http://www.ontologydesignpatterns.org/ont/fred/pos.owl#' set n:pos;
MATCH (n) where n.uri starts with 'http://ontologydesignpatterns.org/cp/owl/semiotics.owl#' set n:semiotics;
MATCH (n) where n.uri starts with 'http://www.w3.org/2002/07/owl#' set n:owl;
MATCH (n) where n.uri starts with 'http://dbpedia.org/resource/' set n:dbpedia;
//2 label_nameing the nodes
MATCH (n) with n, SPLIT(n.uri,'/')[-1] as name SET n.label_name=name;
MATCH (n) with n, SPLIT(n.label_name,'#')[-1] as name SET n.label_name=name;
//3 label_nameing the relationships
MATCH ()-[r]-() with r, SPLIT(type(r),'/')[-1] as name SET r.label_name=name;
MATCH ()-[r]-() with r, SPLIT(r.label_name,'#')[-1] as name SET r.label_name=name;
//4 Delete '%27'
MATCH (n) with n,split(n.label_name,'_') as splitn where n.label_name='%27' or (splitn[0]=~'%27' and splitn[1]=~'[0-9]+') DETACH delete n;
//4 merging nodes with sameAs relationships
MATCH (n:fred)-[r:`http://www.w3.org/2002/07/owl#sameAs`]->(m:dbpedia) where not n.label_name='Of' and not n.label_name='Thing' with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:'overwrite',mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//// remove merged label_names
MATCH (n:dbpedia) remove n:fred;
//5 merging nodes with equivalentClass relationships
MATCH (n:fred)-[r:`http://www.w3.org/2002/07/owl#equivalentClass`]->(m:dbpedia) where not n.label_name='Of' and not n.label_name='Thing' with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:'overwrite',mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//// remove merged label_names
MATCH (n:dbpedia) remove n:fred;
//#######################################################################DO THIS MULTIPLE TIMES
//6 merging verbs like show_1 and show_2 with show
MATCH (n:fred)-[r:`http://www.w3.org/1999/02/22-rdf-syntax-ns#type`]->(m) with n,r,m,split(n.label_name,'_') as splitn where splitn[0]=toLower(m.label_name) and splitn[1]=~'[0-9]+' with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:'overwrite',mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//// remove merged label_names
MATCH (n:dbpedia) remove n:fred;
////Merging verbs with their verbnet forms
MATCH (n:fred)-[r:`http://www.w3.org/2002/07/owl#equivalentClass`]->(m:vn) where toLower(split(n.label_name,'_')[0])=toLower(split(m.label_name,'_')[0]) with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:'overwrite',mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//
MATCH (n:fred)-[r:`http://www.w3.org/2002/07/owl#sameAs`]->(m:dbpedia) where toLower(split(n.label_name,'_')[0])=toLower(split(m.label_name,'_')[0]) and not n.label_name='Of' and not n.label_name='Thing' with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:'overwrite',mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//// remove merged label_names
MATCH (n:dbpedia) remove n:fred;
MATCH (n:fred)-[r:`http://www.w3.org/2002/07/owl#equivalentClass`]->(m:dbpedia) where toLower(split(n.label_name,'_')[0])=toLower(split(m.label_name,'_')[0]) and not n.label_name='Of' and not n.label_name='Thing' with collect([n,m]) as events
unwind events as event
CALL apoc.refactor.mergeNodes([event[0],event[1]],{properties:'overwrite',mergeRels:true}) yield node
return node;
//// delete self loops
MATCH (n)-[r]-(n) delete r;
//// remove merged label_names
MATCH (n:dbpedia) remove n:fred;
//##############################################################################
//// remove merged label_names
MATCH (n:dbpedia) remove n:fred;
//// remove merged label_names
MATCH (n:vn) remove n:fred;

//######################################################################################
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
MATCH (start{uri:'http://dbpedia.org/resource/Hillary_Clinton'}), (end{uri:'http://dbpedia.org/resource/Donald_Trump'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both',nodeQuery:'dbpedia'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost;
//Query and delete the ssp nodes
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n;
//
MATCH (start{uri:'http://dbpedia.org/resource/Bill_Clinton'}), (end{uri:'http://dbpedia.org/resource/Donald_Trump'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both',nodeQuery:'dbpedia'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost;
//
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n;

MATCH (start{uri:'http://dbpedia.org/resource/Hillary_Clinton'}), (end{uri:'http://dbpedia.org/resource/Barack_Obama'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both',nodeQuery:'dbpedia'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost;
//Query and delete the ssp nodes
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n;

MATCH (start{uri:'http://dbpedia.org/resource/Donald_Trump'}), (end{uri:'http://dbpedia.org/resource/Barack_Obama'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both',nodeQuery:'dbpedia'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost;
//Query and delete the ssp nodes
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n;

MATCH (start{uri:'http://dbpedia.org/resource/Donald_Trump'}), (end{uri:'http://dbpedia.org/resource/Bill_Clinton'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both',nodeQuery:'dbpedia'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost;
//Query and delete the ssp nodes
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n;

MATCH (start{uri:'http://dbpedia.org/resource/Hillary_Clinton'}), (end{uri:'http://dbpedia.org/resource/Bernie_Sanders'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both',nodeQuery:'dbpedia'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost;
//Query and delete the ssp nodes
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n;

MATCH (start{uri:'http://dbpedia.org/resource/Beto_O'Rourke'}), (end{uri:'http://dbpedia.org/resource/Bernie_Sanders'})
CALL algo.shortestPath(start, end, 'degree',{write:true,writeProperty:'sssp',direction:'both',nodeQuery:'dbpedia'})
YIELD writeMillis,loadMillis,nodeCount, totalCost
RETURN writeMillis,loadMillis,nodeCount, totalCost;
//Query and delete the ssp nodes
MATCH (n) WHERE EXISTS(n.sssp) remove n.sssp RETURN n;

//9 DB Pedia Ego Network of Donald_Trump
MATCH p=(n:dbpedia{uri:'http://dbpedia.org/resource/Hillary_Clinton'})-[*1..2]-(m:dbpedia{uri:'http://dbpedia.org/resource/Donald_Trump'}) Return p
MATCH p=(n:dbpedia{uri:'http://dbpedia.org/resource/Barack_Obama'})-[*1..2]-(m:dbpedia{uri:'http://dbpedia.org/resource/Donald_Trump'}) Return p
MATCH p=(n:dbpedia{uri:'http://dbpedia.org/resource/Barack_Obama'})-[*1..2]-(m:dbpedia{uri:'http://dbpedia.org/resource/Hillary_Clinton'}) Return p

//Set new neo4j label_names
MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'}) set n:trump;
MATCH (n{uri:'http://dbpedia.org/resource/Hillary_Clinton'}) set n:hillary;

MATCH (n{uri:'http://dbpedia.org/resource/Donald_Trump'}) remove n:claim5005;
MATCH (n{uri:'http://dbpedia.org/resource/Hillary_Clinton'}) remove n:claim5005;


