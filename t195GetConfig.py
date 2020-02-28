import frcteam195.database as t195db
import json


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else json.dumps(res),
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
        payload = event['queryStringParameters']['computerName']
        if None == payload:
            respond('"computerName" not specified in query string')
        conn = t195db.connect()
        print("Database host is {}".format(conn.server_host))
        cursor = conn.cursor()
        cursor.execute("SELECT a.AllianceStation AllianceStation, c.ComputerTypeID ComputerTypeID from AllianceStations a, Computers c " +
                       "WHERE a.AllianceStationID = c.AllianceStationID " +
                       "AND c.ComputerName = '{0}'".format(payload))
        columns = [column[0] for column in cursor.description]
        results = None
        for row in cursor.fetchall():
            results = dict(zip(columns, row))
        if None == results:
            return respond('Not found: computer name "{}"'.format(payload))
        cursor.execute("SELECT EventID, EventName, EventLocation from Events " +
                       "WHERE CurrentEvent = 1")
        columns = [column[0] for column in cursor.description]
        events = None
        for row in cursor.fetchall():
            events = dict(zip(columns, row))
        if None == events:
            return respond('No current event found')
        results.update(events)
        return respond(None, results)
    else:
        return respond('Unsupported method "{}"'.format(operation))
