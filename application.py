# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the application on the templates
from flask import Flask, render_template, request, url_for
from flask import Flask
from flask.ext.dynamo import Dynamo
from boto.dynamodb import condition
from boto.dynamodb.layer1 import Layer1
import boto
import time
# Initialize the Flask application
application = Flask(__name__)

# Define a route for the default URL, which loads the form
@application.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@application.route('/hello/', methods=['POST'])
def hello():
    Provider_Name=request.form['Provider_Name']

    conn = boto.dynamodb.connect_to_region('us-west-2',aws_access_key_id='AKIAJ3U5SM4YYULXU3UA',aws_secret_access_key='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')
    
    table = conn.get_table("all_month")
    data = table.scan(scan_filter={'Provider_Name': boto.dynamodb.condition.EQ(Provider_Name)})
    
    start_time = time.clock()
    
    item = []
    for i in data:
        item.append(i)
    
    end_time = time.clock()
    total_time = end_time - start_time
    return render_template('form_action.html', item=item , time=total_time)
    
    
    
# Run the application :)
if __name__ == '__main__':
  application.run( 
        host="0.0.0.0",
        port=int("80")
  )
