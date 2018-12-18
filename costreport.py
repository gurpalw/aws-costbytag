import boto3
import datetime
from var import *

costexplorer = boto3.client('ce')
auth = boto3.client('sts')

now = datetime.datetime.utcnow()
start = (now - datetime.timedelta(days=61)).strftime('%Y-%m-%d')
end = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

response = auth.assume_role(
    RoleArn=arn,
    RoleSessionName="assumerole"
)

ec2costresponse = costexplorer.get_cost_and_usage(
    TimePeriod={
        'Start': start,
        'End': end
    },
    Granularity='MONTHLY',
    Filter={
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': [
                'Amazon Elastic Compute Cloud - Compute',
            ]
        }
    },
     Metrics=[
         'BlendedCost',
     ]
    # GroupBy=[
    #     {
    #         'Type': 'DIMENSION'|'TAG',
    #         'Key': 'string'
    #     },
    # ],
    # NextPageToken='string'
)

if ec2costresponse.get("ResponseMetadata").get("HTTPStatusCode") == 200:
    firsthalf = (ec2costresponse['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
    secondhalf = (ec2costresponse['ResultsByTime'][1]['Total']['BlendedCost']['Amount'])
    totalcost = float(firsthalf) + float(secondhalf)
    print("Start Date: " + start)
    print("End Date: " + end)
    print("Total Cost: $" + str(int(totalcost)))
else:
    print(ec2costresponse.get("ResponseMetadata"))
