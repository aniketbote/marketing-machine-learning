import os
import random
def load_data(path,seed): 
  train_texts = []
  for fname in sorted(os.listdir(path)):
    if fname.endswith('.txt'):
      with open(os.path.join(path,fname),'r') as f:
        train_texts.append(f.read())
  random.seed(seed)
  random.shuffle(train_texts)
  return train_texts

import psycopg2
import sys

def load_data_database(database,user,password,host,port,table_name):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    conn = psycopg2.connect(database = database, user = user, password = password, host = host, port = port)
    cur=conn.cursor()
    names = []
    srn = []
    train_texts = []
    cur.execute("SELECT sr,uuid, content, title from {} ORDER BY sr".format(table_name))
    rows = cur.fetchall()
    for row in rows:
        srn.append(row[0])
        names.append(row[1])
        t1 = row[2].translate(non_bmp_map)
        t2 = row[3].translate(non_bmp_map)
        text = t1 + t2
        #print(text)
        train_texts.append(text)
    return srn,names,train_texts
#srn,label,train = load_data_database(database,user,post_password,host,port,table_name)
#print(label)

