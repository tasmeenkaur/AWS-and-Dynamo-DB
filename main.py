import os
import csv
import urllib2
import MySQLdb
import boto
import sys
import csv
import time
import urllib2
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import hashlib
import memcache
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import boto.dynamodb


def create_table():
    conn = boto.dynamodb.connect_to_region('us-west-2',aws_access_key_id='AKIAJ3U5SM4YYULXU3UA',aws_secret_access_key='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')
    myschema=conn.create_schema(hash_key_name='id', range_key_name = 'data',range_key_proto_value='S',hash_key_proto_value='S');
    table=conn.create_table(name='all_month', schema=myschema, read_units=10, write_units=50);
    
def load_to_dynamo():
    conn = boto.dynamodb.connect_to_region('us-west-2',aws_access_key_id='AKIAJ3U5SM4YYULXU3UA',aws_secret_access_key='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')
    
    url = 'https://s3.amazonaws.com/tasmeenbuck9189/data1.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    table = conn.get_table('all_month')
    start_time = time.clock()
    rangekey = "All key range"
    hash_id = 1
    count = 1
    for row in cr:
        count += 1
        id = str(hash_id)
        
        user_data={'DRG_Definition' : row[0] , 'Provider_Id' : row[1] , 'Provider_Name' : row [2] , 'Address': row[3] , 'City' : row[4] , 'State' : row [5] , 'Zip' : row[6] , 'Region' : row[7] , 'Total_discharge' : row[8] , 'Average_Covered_Charges' : row[9] , 'Average_Total_Payments' : row [10] , 'Average_Medicare_Payments' : row[11] }
        user=table.new_item(hash_key = id,range_key = rangekey, attrs=user_data)
        user.put()
        hash_id += 1
        print count
    end_time = time.clock()
    total_time = end_time - start_time
    print total_time

    
def main(argv):
    
    while (True):
        print "menu \n"
        print "1.create table. 2 . upload file to dynamo db  3. retrieve data 4. tuple queries 5. memcache 6. EXIT "
        option = raw_input("enter option")
        if (option == '1'):
            create_table()
        elif (option == '2'):
            load_to_dynamo()
        
        
         
        elif(option== '6'):
            sys.exit(0)

        
if __name__ == '__main__':
  main(sys.argv)
