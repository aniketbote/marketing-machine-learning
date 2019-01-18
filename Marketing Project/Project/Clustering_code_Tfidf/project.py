from pprint import pprint
import numpy as np
import Extract as e
from dependencies import Load_data as l
from dependencies import Elbow as el
from sklearn.cluster import KMeans
import psycopg2
from sklearn.metrics.pairwise import cosine_similarity
import h5py
from dependencies import Vector as v


#IMPORTANT VARIABLES
database = "testdb"
threshold = 0.4
user = 'postgres'
post_password = '1234'
host = "127.0.0.1"
port = "5432"
username ='feeds@gladiris.com'
password = 'Abcde@12345'
table_name = 'complete4'

print('----------------------------1---------------------------')

#Connection to Database
conn = psycopg2.connect(database = database, user = user, password = post_password, host = host, port = port)
cur=conn.cursor()


#ADD into the Database
ani = e.unread_emails(username,password,table_name)
print('----------------------------2---------------------------')


#Create Dataset
srn,label,train = l.load_data_database(database,user,post_password,host,port,table_name)

print('----------------------------3---------------------------')

#Create tfidf vector
tfidf_matrix = v.tfid_vector_train(train)
print(tfidf_matrix.shape)

#Delete the previous values from the table
cur.execute("UPDATE complete4 SET sim_cluster=''");


#Plot the Elbow curve
el.elbow_curve(1,10,tfidf_matrix)
K_value = int(input("Enter the Value of K After seeing the Elbow-curve Graph  :\n"))


#Clustering Algorithm
#K_value =   4   #Write the optimum K-value after seeing the Elbow Graph
km = KMeans(n_clusters = K_value, n_init = 2000, max_iter = 6000, precompute_distances = 'auto' )
clusters = km.fit_predict(tfidf_matrix)
clusters = list(clusters)

print('----------------------------4---------------------------')

#Update the cluster values
for i in range(len(label)):
    n = label[i]
    c = int(clusters[i])
    cur.execute("UPDATE complete4 SET cluster_no=%s WHERE uuid = %s ",(c,n));
conn.commit();


#Cosine Similarity Matrix
dist = cosine_similarity(tfidf_matrix)
sim=np.array(dist)
#print('dist done')
print('----------------------------5---------------------------')

#Uncomment to create File
'''
#Create a file for tfidf matrix AND cluster
with h5py.File('tfidf.hdf5', 'w') as f:
    dset = f.create_dataset("default", data=dist)

with h5py.File('cluster.hdf5', 'w') as f:
    dset = f.create_dataset("default", data=clusters)
print('----------------------------over')


#Read the Created file
with h5py.File('cluster.hdf5', 'r') as f:
   data = f['default'][:]
   clusters = data

with h5py.File('tfidf.hdf5', 'r') as f:
   data = f['default'][:]
   sim = np.array(data)
'''

#load the labels in lists
All_uuids = []
uuid_cluster =[]
for k in range(K_value):
    for i in range(len(srn)):
        if k==clusters[i]:
            uuid_cluster.append(srn[i]-1)
    All_uuids.append(uuid_cluster)
    uuid_cluster=[]

print('----------------------------6---------------------------')

#Finding The Intersection between Clusters
all_sim = []
cor = ()
all_cor = []
all_cor1 = []
for i in range(K_value):
    for j in range(i+1,K_value):
        flag = 1
        x = All_uuids[i]
        y = All_uuids[j]
        for r in x:
            for c in y:
                if (sim[r,c] > threshold): #Change The threshold value if needed 
                    all_cor.append(r+1)
                    all_cor.append(c+1)
        if(flag==1):
                    all_cor=list(set(all_cor))
                    print(i,j)
                    print(all_cor)
                    print('---------------')
                    all_cor1.append(all_cor)
                    all_cor=[]
                    flag+=1

print('----------------------------7---------------------------')

#Updating the Documents common between the cluster
count=0
for i in range(K_value):
    for j in range(i+1,K_value):
        if(len(all_cor1[count])>0):
            for cor in all_cor1[count]:
                cur.execute("SELECT sim_cluster from complete4 WHERE sr ={}".format(cor));
                zi="{},{}".format(i,j)
                rows = cur.fetchall()
                if(rows[0][0] == None):
                    cur.execute("UPDATE complete4 SET sim_cluster=%s WHERE sr = %s ",(zi,cor));
                else:
                    if zi==rows[0][0]:
                        continue
                    else:
                        zii=rows[0][0]+':'+zi
                        cur.execute("UPDATE complete4 SET sim_cluster=%s WHERE sr = %s ",(zii,cor));
        count+=1    
conn.commit()
print('----------------------------8---------------------------')




