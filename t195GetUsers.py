import json
import frcteam195.database as t195db


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):

    operations = {
        'GET'
    }

    operation = event['httpMethod']
    if operation in operations:
        conn = t195db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users ORDER BY LastName, FirstName")
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        if 0 == len(results):
            return respond('The Users table is empty!')

        return respond(None, results)
    else:
        return respond('Unsupported method "{}"'.format(operation))
