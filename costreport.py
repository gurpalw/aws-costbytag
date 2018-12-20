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
print("Start Date: " + start)
print("End Date: " + end)
global allprojectscostlist
allprojectscostlist = []
global allteamcostlist
allteamcostlist = []
global keys
keys = ["team", "project"]


def get_valid_tags():
    global teamvalues
    global projectvalues
    teamvalues = []
    projectvalues = []

    for key in keys:
        tags = costexplorer.get_tags(
            TimePeriod={
                'Start': start,
                'End': end
            },
            TagKey=key,
        )
        for tag in tags.get("Tags"):
            if len(tag) > 0:
                if key == "team":
                    teamvalues.append(tag)
                    # print("Adding " + tag + " to team tags")
                else:
                    projectvalues.append(tag)
                    # print("Adding " + tag + " to project tags")


def get_cost(tag_name, tag_value):
    ec2costresponse = costexplorer.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='MONTHLY',
        Filter={
            "And": [
                {
                    'Dimensions': {
                        'Key': 'SERVICE',
                        'Values': [
                            'Amazon Relational Database Service'
                        ]
                    }
                },
                {
                    'Tags': {
                        'Key': tag_name,
                        'Values': [
                            tag_value
                        ]
                    }
                }
            ],
        },
        Metrics=[
            'BlendedCost',
        ]
    )

    if ec2costresponse.get("ResponseMetadata").get("HTTPStatusCode") == 200:
        firsthalf = (ec2costresponse['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
        secondhalf = (ec2costresponse['ResultsByTime'][1]['Total']['BlendedCost']['Amount'])

        global totalcost

        totalcost = float(firsthalf) + float(secondhalf)


        if tag_name == "team":
            print("Total Cost of RDS for " + tv + " team: $ " + str(int(totalcost)))
        elif tag_name == "project":
            print("Total Cost of RDS for " + tv + " project: $ " + str(int(totalcost)))

        return totalcost
    else:
        print(ec2costresponse.get("ResponseMetadata"))


get_valid_tags()

for tn in keys:
    if tn == "team":
        for tv in teamvalues:
            allteamcostlist.append(get_cost(tn, tv))
    elif tn == "project":
        for tv in projectvalues:
            allprojectscostlist.append(get_cost(tn, tv))


allteamcost = sum(allteamcostlist)
allprojectcost = sum(allprojectscostlist)

print("The total cost of RDS across all tagged projects is: $" + str(allprojectcost))
print("The total cost of RDS across all tagged teams is: $" + str(allteamcost))
