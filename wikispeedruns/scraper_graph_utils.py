import random

from db import get_db
from pymysql.cursors import DictCursor


SCRAPER_DB = "scraper_graph"
ARTICLE_TABLE = SCRAPER_DB + ".articleid"
EDGE_TABLE = SCRAPER_DB + ".edgeidarticleid"


def batchQuery(queryString, arr, cur):
    format_strings = ','.join(['%s'] * len(arr))
    cur.execute(queryString % format_strings,tuple(arr))
    return cur.fetchall()

def getLinks(pages, forward = True):

    output = {}
    
    with get_db().cursor(cursor=DictCursor) as cur:
        if forward:
            queryString = "SELECT * FROM " + EDGE_TABLE + " WHERE src IN (%s)"
            #queryString = "SELECT * FROM edges WHERE src IN (%s)"
            queryResults = batchQuery(queryString, list(pages.keys()), cur)
            
            for queryEntry in queryResults:
                title = queryEntry['src']
                if title in pages:
                    
                    if title not in output:
                        output[title] = [queryEntry['dest']]
                    else:
                        output[title].append(queryEntry['dest'])
                        
        else:
            queryString = "SELECT * FROM " + EDGE_TABLE + " WHERE dest IN (%s)"
            queryResults = batchQuery(queryString, list(pages.keys()), cur)
            
            for queryEntry in queryResults:
                title = queryEntry['dest']
                if title in pages:
                    
                    if title not in output:
                        output[title] = [queryEntry['src']]
                    else:
                        output[title].append(queryEntry['src'])
            
        return output
    
    
    

def convertToID(name):
    with get_db().cursor(cursor=DictCursor) as cur: 
        queryString = "SELECT articleID from " + ARTICLE_TABLE + " where name=%s"
        cur.execute(queryString, str(name))
        output = cur.fetchall()

        if len(output) > 0:
            return output[0]['articleID']
        else:
            raise ValueError(f"Could not find article with name: {name}")
    
    
def convertToArticleName(id):
    
    with get_db().cursor(cursor=DictCursor) as cur: 
        queryString = "SELECT * from " + ARTICLE_TABLE + " where articleID=%s"
        cur.execute(queryString, str(id))
        output = cur.fetchall()

        if len(output)>0:
            return output[0]['name']
        else:
            raise ValueError(f"Could not find article with id: {id}")
        
        
        

def numLinksOnArticle(title):
        
    links = getLinks({title:True}, forward=True)
        
    if title in links:
        links = links[title]
        
        return len(links)
        
    return 0



def randomFilter(bln, chance):
    if bln:
        if random.random() > chance:
            return True
    return False


def countWords(string):
    counter = 1
    for i in string:
        if i == ' ' or i == '-':
            counter += 1
    return counter



def getRandomArticle():
    with get_db().cursor() as cur:
        query = "SELECT max(articleID) FROM " + ARTICLE_TABLE + ";"
        cur.execute(query)
        (maxID, ) = cur.fetchone()
        
        while(True):
            yield random.randint(1, maxID)