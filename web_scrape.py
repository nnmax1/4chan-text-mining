


import requests,time
import urllib
import re
 
# old 4chan webscraping stuff

def cleanhtml(raw_html):
    CLEANR = re.compile('<.*?>') 
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

# save a file in a certain directory 
def saveFileLocally(url, dir):
    name=url.split('/')[4]
    file_name='./'+dir+'/'+name
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)

# simple way to read each line of txt file into a python list
# each element in list will be a line in the txt file
def getFromFile(file):
    arr = []
    file1 = open(file, 'r')
    Lines = file1.readlines()
    # Strips the newline character
    for line in Lines:
        arr.append(str(line.strip()))
    file1.close()
    return arr

# download images from urls listed in a board_images.txt file
def downloadImages(file, board):
    urls=getFromFile(file)
    for u in urls:
        if '.gif' in u:  
            print(u)
            saveFileLocally(u, board)
        elif '.webm' in u: 
            print(u)
            saveFileLocally(u, board)
        time.sleep(1)

def getUrlsFromThread(board, thread):
    f = open(board+"_"+thread+"_urls.txt", "a")
    url = 'https://a.4cdn.org/'+board+'/thread/'+thread+'.json'
    r=requests.get(url).json()
    for data in r['posts']: 
        if 'tim' in data:
            u='https://i.4cdn.org/'+board+"/"+str(data['tim'])+data['ext']
            if requests.get(u).status_code == 200:       
                print(u)
                f.write(u+'\n')
    f.close()
    return 
#  send data thru discord webhook 
def webhookSendData(webhook, desc,title,url, username):
    data = {
        "embeds":[
            {
                'description':desc,
                'title':title,
                'url':url
            }
        ]
    }  
    result = requests.post(webhook, json = data)
    return result

def getPosts(board):
    #f = open(board+"_images.txt", "a")
    for idx in range(1, 10):
        url = 'https://a.4cdn.org/'+board+'/'+str(idx)+'.json'
        data = requests.get(url).json()
        posts=[]
        for thrd in data['threads']:
            for post in thrd['posts']:
                if 'capcode' not in post:
                    posts.append(post)                

        return posts
def webhookSendImages(board,webhook):
    #f = open(board+"_images.txt", "a")
    for idx in range(1, 10):
        url = 'https://a.4cdn.org/'+board+'/'+str(idx)+'.json'
        data = requests.get(url).json()
        posts=[]
        for thrd in data['threads']:
            for post in thrd['posts']:
                if 'tim' in post:
                    u='https://i.4cdn.org/'+board+"/"+str(post['tim'])+post['ext']
                    data={"content":u, 'username':'bot'}
                    result = requests.post(webhook, json = data)
                    print(u,result)
                    time.sleep(2)

# send posts to discord channel with webhook
def scrapePosts(board,webhook):
    data=getPosts(board)
    i=0
    for d in data:
        if i>0:
            if 'com' in d:
                com=cleanhtml(d['com'])
            else: 
                com=''
            url=''
            if d['resto']== 0:
                url='https://boards.4chan.org/'+board+'/thread/'+str(d['no'])
                print(url)
            else:
                url='https://boards.4chan.org/'+board+'/thread/'+str(d['resto'])+"#p"+str(d['no'])
            #print(com)
            print(url)
            if com!='':
                webhookSendData(webhook, com, str(d['now']),url,'bot')
                time.sleep(1)
        i=i+1
        



boards=['r9k','wsg','gif', 'b','s4s','soc','bant','lgbt']
thread='26065854'
webhook='https://discord.com/api/webhooks/....'

#getUrlsFromThread(boards[2],thread)
#downloadImages(boards[2]+'_'+thread+'_urls.txt', boards[2])
#webhookSendImages(boards[1],webhook)
#scrapePosts(boards[0,webhook])


 