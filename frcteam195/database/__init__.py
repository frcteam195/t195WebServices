import boto3
import mysql.connector as mariadb

dynamodb = boto3.resource('dynamodb')

def connect():
    table = dynamodb.Table('frcteam195_database_values')
    response = table.get_item(
        Key={
            'entry_key': 'default'
        }
    )
    item = response['Item']

    conn = mariadb.connect(user=item['user'],
                           passwd=item['cred'],
                           host=item['host'],
                           database=item['database'])

    return conn
