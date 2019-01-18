#For URL Extraction
import time
import datetime
import email
import imaplib
import mailbox
import re
import psycopg2
import nltk
import traceback
import logging
import urllib.request
from textblob import TextBlob
from nltk.corpus import wordnet
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from ISOLanguages import iso_639_choices    #File
from TestingFunctions import printline    #File
from TestingFunctions import checkpoint    #File
from summa import keywords
from googletrans import Translator
#For Data Extraction
from goose3 import Goose
import os
#For UUID Generation
import uuid
imaplib._MAXLINE = 5000000


conn = psycopg2.connect(database="testdb", user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
cur = conn.cursor()


#database = "testdb"
#user = 'postgres'
#post_password = '1234'
#host = "127.0.0.1"
#port = "5432"
#username ='feeds@gladiris.com'
#password = 'Abcde@12345'
#table_name = 'complete3'

def unread_emails(username,password,table_name):
    emails_info = []
    emailz = {}
    
    g = Goose()
    j=1
    default_media_url = {"News" : "https://res.cloudinary.com/dx0ow30uf/image/upload/v1532504563/news_tytmnz.jpg",
    "Sports":"https://res.cloudinary.com/dx0ow30uf/image/upload/v1532505728/cover_image_upk3cz.jpg",
    "Health" : "https://res.cloudinary.com/dx0ow30uf/image/upload/v1532505566/health-wellness_hygxy6.jpg",
    "Technology":"https://res.cloudinary.com/dx0ow30uf/image/upload/v1532505629/technology1_kkikcm.jpg",
    "Money":"https://res.cloudinary.com/dx0ow30uf/image/upload/v1532505796/Th11-Paper-money_vfzejh.jpg",
    "Humour":" https://res.cloudinary.com/dx0ow30uf/image/upload/v1532505453/smiley-1706233_1280-1200x800_gyajmf.jpg"}

    translator = Translator()
    EMAIL_ACCOUNT = username
    PASSWORD = password
    imap_url = 'imap.gmail.com'

    def slicer(my_str,sub):
        index=my_str.find(sub)
        if index !=-1 :
            return my_str[index:]
        return my_str

    def Get_Image_metaUrl_Api(url):
        import http.client
        conn = http.client.HTTPSConnection("api.urlmeta.org")
        conn.request("GET", "/?url="+url)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")

        if data.find('"status":"OK"'):
            imgind = data.find(',"image":"')
            if imgind != -1:
                imgind = imgind + 10
                quoteIndex = data[imgind:].find('"')
                return "Image",(data[imgind:imgind+quoteIndex])
            else:
                return "Api Failiure"," "
        return " "," no image"

    def findDateInBody(body):
        months = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ', 'Jul ','Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
        date = " "
        for i in range (len(months)):
            if months[i] in str(body):
                ind = str(body).find(months[i])
                subBody = str(body)[ind:]
                date = str(body)[ind:ind+20]
                break
        return date

    def stringToTimestamp(local_message_date):
        months = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ', 'Jul ','Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
        month = local_message_date[:4]
        monthValue = months.index(month)
        monthValue = monthValue + 1
        comaIndex = local_message_date.find(',')
        now = datetime.datetime.now()
        if comaIndex == -1:
            return '0'
        collenIndex = local_message_date.find(':')
        if collenIndex == -1:
            return '0'
        year = local_message_date[comaIndex-4:comaIndex]
        date = str(now.day)
        if re.findall(r'\d+', local_message_date[4:comaIndex-4]):
            date = str(re.findall(r'\d+', local_message_date[4:comaIndex-4])[0])
        if int(date)< 10:
            date = '0'+date
        hour = local_message_date[comaIndex+1:collenIndex]
        minute = local_message_date[collenIndex+1:collenIndex+3]
        complete = year.strip()+"-"+str(monthValue)+"-"+date.strip()+" "+hour.strip()+":"+minute.strip()+":"+"00"
        return complete

    def Subject_Language_Detector(subject, body):
        if len(body)>10:
            return iso_639_choices[detect(body)]
        return iso_639_choices[detect(subject)]

    def Content_Init_Tag_Detector(subject):
        special_char = ['-','|',':']
        init_tag = 'Not Found'
        if any(x in subject for x in special_char):
            charlist = list(filter(lambda x:  x in subject, special_char))
            head, sep, tail = subject.partition(charlist[0])
            subject = tail
            if any(x in subject for x in special_char):
                charlist = list(filter(lambda x:  x in subject, special_char))
                head, sep, tail = subject.partition(charlist[0])
                subject = tail
                init_tag= head
        return init_tag

    def get_synonyms(word):
        synonyms = []
        answer = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
                for i in range (len(synonyms)):
                    word = synonyms[i]
                    for syn in wordnet.synsets(word):
                        for l in syn.lemmas():
                            answer.append(l.name())
        answer = list(set(answer))
        return answer

    def Content_Type_Detector(subject):
        type_detected = " "
        sports_list = ['Cricket','Tennis','Kabadi','Boxing','Football','Sports','World Cup']
        humor_list = ['Funny','Humor']
        health_list = ['Health','Lifestyle']
        news_list = ['World','Special','News']

        if subject ==  " ":
            return type_detected
        types_list = ['Sports','Health','Humor','Lifestyle','Technology','Funny','Cricket','Tennis','Money','World Cup','World','Football','Money','Special','News']
        for x in range (len(types_list)):
            if subject.find(types_list[x]) != -1:
                type_detected = types_list[x]
                break
        for x in range (len(sports_list)):
            if type_detected.find(sports_list[x]) != -1:
                type_detected = 'Sports'
                return type_detected
                break
        for x in range (len(humor_list)):
            if type_detected.find(humor_list[x]) != -1:
                type_detected = 'Humour'
                return type_detected
                break
        for x in range (len(news_list)):
            if type_detected.find(news_list[x]) != -1:
                type_detected = 'News'
                return type_detected
                break
        for x in range (len(health_list)):
            if type_detected.find(health_list[x]) != -1:
                type_detected = 'Health'
                return type_detected
                break
        return type_detected

    def getKeys(body, sub):
        if body == " ":
            print("No Body")
            Body = sub
        else:
            Body = body
        keywords_Str =" "
        blob = TextBlob(Body)
        keys = blob.noun_phrases
        keyswords_local = str(keys)
        keywords_Str = keyswords_local
        keywords_Str = keywords_Str.replace("'", "")
        return keywords_Str

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('INBOX')#[Gmail]/Starred
    #mail.select('[Gmail]/Starred')


    #date = (datetime.date.today() - datetime.timedelta(weeks=10)).strftime("%d-%b-%Y")
    #result, data = mail.uid('search', None,'(SENTSINCE {0})'.format(date))#ALL/UNSEEN
    result, data = mail.uid('search', None,'UNSEEN')
    i = len(data[0].split())
    now = datetime.datetime.now()
    rows_inserted = 0
    for x in range(i):
        print(str(x+1))
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        try:
            raw_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(raw_email))
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            date_tuple = email.utils.parsedate_tz(email_message['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                local_message_date = "%s" %(str(local_date.strftime("%b %d %Y, %H:%M")))
                email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
                email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
                subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

            #INIT_TAG
            init_tag = Content_Init_Tag_Detector(subject)
            global_body = " "
            global_url = " "
            source = " "
            keywords_Str = " "
            Media_Type = " "
            media_url = " "
            content_type = " "
            DateinMail = " "
            news_language = " "
            Added_on = " "
            ParentCategory = " "
            Xsubject = " "
            parent_Category_Origin = " "
            Added_on = (str)(now.strftime("%Y-%m-%d %H:%M"))
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    body = body.decode('utf-8')
                    DateinMail = findDateInBody(body)
                    global_body = re.sub("<.*?>", " ", body)
                    urls = re.findall(r'(https?://\S+)', global_body)
                    if(len(urls)>0):
                        global_url = urls[0]

                    #SOURCE
                        head, sep, tail = global_url.partition('//')
                        source = tail
                        if('www' in source):
                            source = source.replace('www.',"")
                        head, sep, tail = source.partition('/')
                        source =  head
                        if '"' in source:
                            source =  source.replace('"',"")
                    if source ==" ":
                        head, sep, tail = email_from.partition('<')
                        source =  head

                    #PARENT_CATEGORY
                    ParentCategory = Content_Type_Detector(subject)
                    if ParentCategory == " ":
                        ParentCategory = Content_Type_Detector(body)
                        parent_Category_Origin = "Description"
                    else:
                        parent_Category_Origin = "Headline"

                    #XSUBJECT
                    if '::' in subject:
                       collenIndex = subject.rfind('::')
                       Xsubject = subject[:collenIndex]

                   #SUBJECT
                    if '::' in subject:
                       head, sep, tail = subject.partition('::')
                       subject = tail

                    #NEWS LANGUAGE
                    news_language = Subject_Language_Detector(subject, body)

                    #DATE INSIDE THE MAIL
                    if(DateinMail==" "):
                        DateinMail = local_message_date

                    #BODY
                    head, sep, tail = body.partition(DateinMail)
                    body = tail
                    if "You are receiving this" in body:
                        head, sep, tail =  body.partition("You are receiving this")
                    body = head
                    body = body.strip()

                    #MEDIA
                    Media_Type, media_url = Get_Image_metaUrl_Api(global_url)
                    if Media_Type == "Api Failiure":

                        #DEFAULT
                        Media_Type = "Image"
                        if ParentCategory != " ":
                            media_url = default_media_url[ParentCategory]
                        link = re.findall(r'https?://.*', body)
                        if len(link) != 0:
                            media_url = link[0]

                    #KEYWORDS
                    if news_language.strip() !="English":
                        translator = Translator()
                        bodylength = len(body)
                        if bodylength >2000:
                            bodylength = 2000
                        try:
                            output = translator.translate(body[:bodylength])
                            mailBody = output.text
                            output = translator.translate(subject)
                            mailSubject = output.text
                        except Exception as e:
                            conn.rollback()
                    else:
                        mailBody = body
                        mailSubject = subject
                    keywords_Str = getKeys(mailBody, mailSubject)
                    priority = "0"
                    body = body.replace("Media files:","")
                    Description = re.sub(r'^https?:\/\/.*[\r\n]*', '', body, flags=re.MULTILINE)

                    #DATE 
                    DateinMail = stringToTimestamp(DateinMail)
                    if DateinMail == '0':
                        DateinMail = stringToTimestamp(local_message_date)
                        
##################################################################################    
#------------------------  INSERT INTO DATABASE  --------------------------#

                    #local_date, local_message_date, email_from,source, Description, keywords, ParentCategory, parent_Category_Origin

                    article = g.extract(url = global_url)
                    x1 = str(uuid.uuid4())
                    x2=global_url
                    x3=article.cleaned_text
                    x4=article.title
                    x5=source
                    x6=ParentCategory
                    #print(type(table_name))
                    cur.execute("INSERT INTO complete4(UUID,URL,CONTENT,TITLE,SOURCE,DOMAIN) VALUES(%s,%s,%s,%s,%s,%s) ",(x1,x2,x3,x4,x5,x6));
                    conn.commit();               
 
                    
##################################################################################




                                                       
        except Exception as e:
            print(e)
            continue
            #print('Theres and error')
            #logging.error(traceback.format_exc()+e+ str(subject.encode('utf-8').strip()))    
    #print('over')
    return emails_info

#username ='feeds@gladiris.com'
#password = 'Abcde@12345'
#ani = unread_emails(username,password,table_name)
