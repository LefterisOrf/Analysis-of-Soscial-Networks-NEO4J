# -*- coding: utf-8 -*-
"""
Created on Sun May  9 17:45:54 2021

@author: Lefor
"""
import time
from py2neo import Graph

def importFromCSVtoNeoArticles(graph):
    print('Starting Insertion.')
    
    queryRel = '''
    call apoc.periodic.iterate(
        "LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS rowRel RETURN rowRel",
        "MERGE (auth:Author {name:rowRel.author})
         MERGE (pub:Publication {title: replace(rowRel.title, '\\"', ''), year: toInteger(rowRel.year), journal: rowRel.journal})
         CREATE (auth)-[:WROTE{isLeadAuthor: rowRel.isFirst, isLastAuthor: rowRel.isLast}]->(pub)",
         {batchSize:200, parallel:true, iterateList:true}
    )
               '''
    
    
    start = time.time()
    graph.run(queryRel)
    print('Insertion of relationships completed. Execution lasted: {}'.format(time.time() - start))
    

def runQuery(query, name = None, year = None):
    data = graph.run(query, qname = name, qyear = year)
    count = 0
    for d in data:
        count += 1
        print(d)
    print(count)  

def matchQueries(graph):
    print('Find the titles (title, year) of publications that a particular author has published.')
    runQuery( '''
             MATCH (auth:Author)-[:WROTE]->(pub:Publication)
             WHERE auth.name = $qname
             RETURN pub.title AS Title, pub.year as Year
            ''', 'Ana Marusic')
    print('---------------------------------------------------------')
    print('Find the co-authors of an author (name, number of co-authorships) for a particular year.')
    runQuery('''
             MATCH (auth:Author)-[:WROTE]->(pub:Publication)
             WHERE auth.name = $qname AND pub.year = $qyear
             
             MATCH (coAuth:Author)-[:WROTE]->(pub)
             WHERE coAuth.name <> auth.name
             
             RETURN coAuth.name AS name, COUNT(coAuth) as CoAuthorships
             ''', 'Ana Marusic', 2020)
    print('---------------------------------------------------------\n\n\n\n')
    print('Find the top-K authors (name, count) with regard to most conference/journal publications.')
    runQuery('''
             MATCH (auth:Author)-[:WROTE]->(pub:Publication)
             
             RETURN auth.name AS name, COUNT(pub) as Publications
             ORDER BY COUNT(pub) DESC
             LIMIT 10
             ''', 'Ana Marusic', 2020)
    print('---------------------------------------------------------')
    print('Find the top-K authors (name, count) with regard to most co-authors in a single work.')
    runQuery('''
             MATCH (auth:Author)-[:WROTE]->(pub:Publication)
             MATCH (coAuth:Author)-[:WROTE]->(pub)
             WHERE coAuth.name <> auth.name
             
             RETURN auth.name, pub.title, COUNT(coAuth)
             ORDER BY COUNT(coAuth) DESC
             LIMIT 10
             
             
             
             ''', 'Ana Marusic', 2020)
    print('---------------------------------------------------------')

graph = Graph(password="m222")
while True:
    command = int(input('Type 0 to delete all data, 1 to insert data from csv, 2 to create csv from the xml, 3 to run the queries.\n'))
    if command == 0:
        print('Deleting graph..')
        graph.delete_all()
    elif command == 1:
        print('Importing csv to db.')
        importFromCSVtoNeoArticles(graph)
    elif command == 2:
        print('Unavailable')
    elif command == 3:
        print('Running queries...')
        matchQueries(graph)
    else:
        print('Exiting')
        break;
        