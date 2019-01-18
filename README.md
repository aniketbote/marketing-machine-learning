# marketing-machine-learning

### Database - postgresDB
Install postgres in your system

### For Creating the table in postgres
#### Steps To be folowed: 
Copy the code from CREATE.txt into the postgres terminal.


### Main file = project.py
#### Steps to be followed for executing this file.

1. In the file fill your own values for the important variables section which include:
   database = Name of the databse       
   user = Name of the user in DB              
   post_password = Password used for Database     
   host = Host address of Db server      
   port = Port at which the postgres is active      
   username = Email id from which the articles has to be extracted       
   password = Password for the Email id      
   table_name = Name of your table       
   threshold = Threshold value for selecting intersection of clusters       

2. In middle of execution a graph will pop up. Input the value of k (integer) after studying the graph.
   The graph is elbow-curve graph for selecting optimum k value in K-means.
   
## Note:
1. While creating table make sure to change the table name according to your database and table in all query statements.
   Files which need changes :               
   project.py - line 21, line 46, line 66, line 141, line 145, line 151      
   Extract.py - line 355     
   
   
## Requirement
### Extra libraries:
#### Use following command on cmd:
1. pip install psycopg2    
2. pip install numpy      
3. pip install sklearn      
4. pip install h5py      
5. pip install nltk     
6. pip install goose3     
7. pip install bs4      
8. pip install pickle      
