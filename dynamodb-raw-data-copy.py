import boto3
import json
import decimal
import base64
import os
import sys

if len(sys.argv) != 3:
    print 'Usage: %s <source_table_name>' \
        ' <destination_table_name>' % sys.argv[0]
    sys.exit(1)

src_table = sys.argv[1]
dst_table = sys.argv[2]

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

src=dynamodb.Table(src_table)
dest=dynamodb.Table(dst_table)

response = src.scan()

for i in response['Items']:
    json.dumps(i,cls=DecimalEncoder)
    new_item = {}
    for f in i.keys():
        if f != "courseCode":
            new_item[f] = i[f]
    dest.put_item(Item=new_item)

while 'LastEvaluatedKey' in response:
    response = src.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    for i in response['items']:
        print (json.dumps(i, cls=DecimalEncoder))
