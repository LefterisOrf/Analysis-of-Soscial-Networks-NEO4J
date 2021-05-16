# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:37:49 2021

Article creation:
    
    article = Node('Article', title = titleT, year = yearT, journal = journalT)
    graph.create(article)
    for author in authors:
        authorGr = Node('Author', name = author.text)
        graph.create(authorGr)
        graph.create(Relationship(authorGr, 'WROTE', article))

@author: Lefteris Orfanidis
"""
import gzip
from lxml import etree
import csv

parser = etree.XMLParser(load_dtd = True)
dtd = '<!DOCTYPE dblp SYSTEM "dblp.dtd">'

startArticle = "<article"
endArticle = "</article>"

startInproceeding = "<inproceedings"
endInproceeding = "</inproceedings>"

startIncollection = "<incollection"
endIncollection = "</incollection>"

writingArt = False
xmlArt = dtd

writingInpr = False
xmlInpr = dtd

writingInc = False
xmlInc = dtd

'''
csv_articles = open('articles.csv', mode= 'w',)
fieldnames = ['title', 'year', 'journal']
csv_art_writer = csv.DictWriter(f = csv_articles, delimiter = '\t',fieldnames = fieldnames)
csv_art_writer.writeheader()

csv_authors = open('authors.csv', mode = 'w')
fieldnames = ['name']
csv_aut_writer = csv.DictWriter(csv_authors, fieldnames)
csv_aut_writer.writeheader()
'''
csv_relationships = open('relationships.csv', mode = 'w')
fieldnames = ['author', 'relationship', 'title', 'year', 'journal', 'pages', 'isFirst', 'isLast']
csv_rel_writer = csv.DictWriter(csv_relationships, fieldnames)
csv_rel_writer.writeheader()

articleNum = 0;
def handleArticle(xml):
    xmldoc = etree.fromstring(xml, parser = parser)
    if xmldoc.find(".//title") == None:
        return
    titleT = xmldoc.find(".//title").text
    yearT = None
    journalT = None
    pagesT = None
    if titleT:
        titleT = titleT.replace('"', '')
        titleT = titleT.replace("'", "")
        if xmldoc.find(".//year") != None:
            yearT = xmldoc.find(".//year").text
        if xmldoc.find(".//journal") != None:
            journalT = xmldoc.find(".//journal").text
        if xmldoc.find(".//pages") != None:
            journalT = xmldoc.find(".//pages").text
            
        if journalT != None and yearT != None and int(yearT) > 2018:
            global articleNum
            articleNum += 1
            count = 0
            authors = xmldoc.findall(".//author")
            for author in authors:
                if count == 0:
                    csv_rel_writer.writerow({'author' : author.text, 'relationship' : 'WROTE', 'title' : titleT , 'year' : yearT, 'journal' : journalT, 'pages' : pagesT, 'isFirst': True, 'isLast': False})
                elif count == len(authors) - 1:
                    csv_rel_writer.writerow({'author' : author.text, 'relationship' : 'WROTE', 'title' : titleT , 'year' : yearT, 'journal' : journalT, 'pages' : pagesT, 'isFirst': False, 'isLast': True})
                else:
                    csv_rel_writer.writerow({'author' : author.text, 'relationship' : 'WROTE', 'title' : titleT , 'year' : yearT, 'journal' : journalT, 'pages' : pagesT, 'isFirst': False, 'isLast': False})
                count += 1
    
def handleInproceeding(xml):
    xmldoc = etree.fromstring(xml, parser = parser)
    title = xmldoc.find(".//title").text
    if title:
        year = xmldoc.find(".//year").text
        print(year)
        booktitle = xmldoc.find(".//booktitle").text
        print(booktitle)
        authors = []
        for author in xmldoc.findall(".//author"):
            authors.append(author)
            print("\t" + author.text)
    
def handleIncollection(xml):
    xmldoc = etree.fromstring(xml, parser = parser)
    title = xmldoc.find(".//title").text
    if title:
        year = xmldoc.find(".//year").text
        booktitle = xmldoc.find(".//booktitle").text
        if xmldoc.find(".//publisher") == None:
            return
        print("-------------INCOLLECTION--------------------------")
        publisher = xmldoc.find(".//publisher").text
        print(title)
        print(year)
        print(booktitle)
        print(publisher)
        authors = []
        for author in xmldoc.findall(".//author"):
            authors.append(author)
            print("\t" + author.text)
        print("-----------------------------------------------------")


with gzip.open("dblp.xml.gz", "rt") as file:
    for line in file:
        if endArticle in line:
            index = line.find(endArticle) + len(endArticle)
            xmlArt += line[:index]
            handleArticle(xmlArt)
            xmlArt = dtd
            writingArt = False
            
        if startArticle in line:
            writingArt = True
            index = line.find(startArticle)
            xmlArt += line[index:]
        elif writingArt == True:
            xmlArt += line
            
        
        if articleNum > 300000:
            break
        
        '''
        if endInproceeding in line:
            index = line.find(endInproceeding) + len(endInproceeding)
            xmlInpr += line[:index]
            handleInproceeding(xmlInpr)
            xmlInpr = dtd
            writingInpr = False
            
        if startInproceeding in line:
            writingInpr = True
            index = line.find(startInproceeding)
            xmlInpr += line[index:]
        elif writingInpr == True:
            xmlInpr += line
        '''


print("Number of articles is: {}".format(articleNum))





'''
with gzip.open("dblp.xml.gz", "rt") as file:
    num = 0
    for line in file:
        if endPublication in line:
            index = line.find(endPublication) + len(endPublication)
            xml += line[:index]
            num += 1
            handleInproceeding(xml)
            xml = dtd
            writing = False
            
        if startPublication in line:
            writing = True
            index = line.find(startPublication)
            xml += line[index:]
        elif writing == True:
            xml += line

print("Number of inprocedings is: {}".format(num))

with gzip.open("dblp.xml.gz", "rt") as file:
    num = 0
    for line in file:
        if endIncollection in line:
            index = line.find(endIncollection) + len(endIncollection)
            xml += line[:index]
            num += 1
            handleIncollection(xml)
            xml = dtd
            writing = False
            
        if startIncollection in line:
            writing = True
            index = line.find(startIncollection)
            xml += line[index:]
        elif writing == True:
            xml += line

print("Number of incollections is: {}".format(num))
'''
