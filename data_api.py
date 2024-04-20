import requests
import sqlite3
import time
import re,html
 

class DataAPI():
    def __init__(self,db):
        # exclude boards /t/, /f/ and /3/
        self.boards=['tg', 'fit', 'his', 'pw', 'xs', 'n', 'lit', 'i', 'vip', 'out', 'ck', 'co', 'wsr', 'w', 'mu', 'lgbt', 'u', 'soc', 'vmg', 'x', 'd', 'hm', 'c', 'sci', 'po', 'vm', 'vg', 'jp', 'biz', 'vr', 'cm', 'adv', 'bant', 'gd', 'g', 'diy', 'mlp', 'b', 'fa', 'trv', 'a', 'vst', 'h', 'gif', 'hr', 'trash', 's4s', 'aco', 'ic', 'vt', 'sp', 'int', 'm', 'news', 'toy', 'r', 'an', 'e', 'qst', 'p', 'wsg', 'vrpg', 'v', 'tv', 'o', 'cgl', 'qa', 's', 'wg', 'vp', 'hc', 'pol', 'r9k', 'y', 'k']
        self.db_name=db

    def cleantext(self,raw_text):
        raw_text=raw_text.replace('&gt;','>')
        reply_tag_pattern = re.compile(r'>>\d+') # remove reply tag
        url_pattern = re.compile(r'https?://\S+|www\.\S+') # remove urls
        CLEANR = re.compile('<.*?>') # remove html tags
        cleantext = re.sub(CLEANR, '', raw_text)
        cleantext = reply_tag_pattern.sub('', cleantext)
        cleantext = html.unescape(cleantext)
        cleantext=url_pattern.sub('',cleantext)
        chanpattern = r'&gt;&gt;\d{8}'
        cleantext=cleantext.replace("&#039;" ,"'")
        cleantext = re.sub(chanpattern, '', cleantext)
        return cleantext

   
    def getPosts(self,board):
        posts=[]
        url='https://a.4cdn.org/'+board+'/catalog.json'
        data=requests.get(url).json()
        for d in data:
            for thrd in d['threads']:
                thread_url='https://a.4cdn.org/'+board+'/thread/'+str(thrd['no'])+'.json'
                #print(thread_url)
                post_data=requests.get(thread_url).json()
                for p in post_data['posts']: 
                    if 'com' in p: 
                        if 'capcode' not in p:
                            print(p['no'])
                            posts.append(p)
                            #time.sleep(2)
                time.sleep(2)
        print('posts scraped from ', board)
        '''
        for idx in range(1, 10):
            url = 'https://a.4cdn.org/'+board+'/'+str(idx)+'.json'
            data = requests.get(url).json()
            posts=[]
            for thrd in data['threads']:
                for post in thrd['posts']:
                    if 'capcode' not in post:
                        posts.append(post)                        
        '''
        return posts
    # add table to database where table name is the board name
    def addTableToDB(self,table_name):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE "+table_name+" (no,now, com)")
    # get posts from board and insert into table
    def addDataFromBoard(self,table_name):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        data=self.getPosts(table_name)
        dataentries=[]
        for d in data: 
            if 'com' in d:
                #clean text
                text=d['com']
                text=self.cleantext(text)
                if len(text)> 3:
                    entry= (d['no'],d['now'],text)
                    print(d['no'])
                    dataentries.append(entry)
        cur.executemany("INSERT INTO "+table_name+" VALUES(?, ?, ?)", dataentries)
        con.commit() 
    # get posts from table
    def getDataFromTable(self,table_name):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        res = cur.execute("SELECT  DISTINCT * FROM "+table_name)
        return res.fetchall()
    # add tables to database
    def initDB(self):
        # table_name is the name of board 
        for b in self.boards:
            self.addTableToDB(str(b))

    # get text from a bunch of boards and write to database
    # each table corresponds to specific board
    def writeData(self):
        for b in self.boards:
            self.addDataFromBoard(b)
            print('added data from ',b)  
            time.sleep(2)
        return
    # retrieve all data as dict list
    def retrieveData(self):
        data=[]
        for b in self.boards:
            d=self.getDataFromTable(b)
            data.append({'board':b,'data':d})
        return data
    # count no. of posts in each table and total number posts in db
    # print counts to console 
    def databaseCounter(self):
        d=self.retrieveData()
        posts=0
        result=[]
        for e in d: 
            count=len(e['data'])
            posts+=count
            print(e['board'], len(e['data']))
            result.append({'board':e['board'],'count':count})
        print('total posts: ',posts)
        return {'data': result,'total_posts':posts} 
    
    # posts from specific board
    def getPostsFromBoard(self,board):
        d=self.retrieveData()
        for i in range(len(d)):
            if d[i]['board']==board:
                return d[i]['data']
            i=i+1 
    # add tables to db and add dataentries to db
    def createDatabase(self):  
        self.initDB()
        self.writeData()
        self.databaseCounter() #check no. of posts in each table

    # makes new copy of database and add all distinct items to db
    # manually delete current database file
    def removeDuplicates(self,new_db_name):
        # curr database
        con1=sqlite3.connect(self.db_name)
        cur1=con1.cursor()
        # new database
        con = sqlite3.connect(new_db_name)
        cur = con.cursor()  
        for board in self.boards:
            # create table for each board
            create_table="CREATE TABLE "+board+" (no,now, com)"
            cur.execute(create_table)
            # add data to new database from old one
            res = cur1.execute("SELECT DISTINCT * FROM "+board).fetchall()
            cur.executemany("INSERT INTO "+board+" VALUES(?, ?, ?)",res)
            con.commit() 

# to add new data to dataset
DataAPI('data.db').databaseCounter()
DataAPI('data.db').writeData()
DataAPI('data.db').removeDuplicates('new.db')
DataAPI('new.db').databaseCounter()




 
 
 

#posts=DataAPI('data.db').getPosts('gif')

#p=DataAPI('data.db').retrieveData()[0]['data'][0]
#print(p)
