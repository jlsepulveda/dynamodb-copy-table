import boto3
import json
import decimal
import base64

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

src=dynamodb.Table('devDiagnosticPerformance')

dest=dynamodb.Table('devDiagnosticPerformanceK5')

response = src.scan()

for i in response['Items']:
    print (json.dumps(i,cls=DecimalEncoder))
    print "Here is what it is"
    new_item = {}
    for f in i.keys():
        new_item[f] = i[f]
    new_item['classroomCourseUUID'] = base64.b64encode(i['classroomId'] + '|0')
    dest.put_item(Item=new_item)

while 'LastEvaluatedKey' in response:
    response = src.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    for i in response['items']:
        print (json.dumps(i, cls=DecimalEncoder))



