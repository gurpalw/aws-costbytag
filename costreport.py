import boto3
import datetime

costexplorer = boto3.client('ce')

now = datetime.datetime.utcnow()



response = costexplorer.get_cost_and_usage(
    TimePeriod={
        'Start': 'string',
        'End': 'string'
    },
    Granularity='DAILY'|'MONTHLY'|'HOURLY',
    Filter={
        'Or': [
            {'... recursive ...'},
        ],
        'And': [
            {'... recursive ...'},
        ],
        'Not': {'... recursive ...'},
        'Dimensions': {
            'Key': 'AZ'|'INSTANCE_TYPE'|'LINKED_ACCOUNT'|'OPERATION'|'PURCHASE_TYPE'|'REGION'|'SERVICE'|'USAGE_TYPE'|'USAGE_TYPE_GROUP'|'RECORD_TYPE'|'OPERATING_SYSTEM'|'TENANCY'|'SCOPE'|'PLATFORM'|'SUBSCRIPTION_ID'|'LEGAL_ENTITY_NAME'|'DEPLOYMENT_OPTION'|'DATABASE_ENGINE'|'CACHE_ENGINE'|'INSTANCE_TYPE_FAMILY'|'BILLING_ENTITY'|'RESERVATION_ID',
            'Values': [
                'string',
            ]
        },
        'Tags': {
            'Key': 'string',
            'Values': [
                'string',
            ]
        }
    },
    Metrics=[
        'string',
    ],
    GroupBy=[
        {
            'Type': 'DIMENSION'|'TAG',
            'Key': 'string'
        },
    ],
    NextPageToken='string'
)