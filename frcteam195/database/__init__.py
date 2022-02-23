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


def put(cmd):
    logging.debug(str(datetime.datetime.now()) + " Executing update command: cmd={0}".format(cmd))
    ret = "failure"
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(cmd)
        conn.commit()
        logging.debug(str(datetime.datetime.now()) + " {0} records were updated: cmd={1}".format(cursor.rowcount, cmd))
        ret = "success"
    except MySQLError as merr:
        logging.error(str(datetime.datetime.now()) + " Unexpected error occurred {0}".format(merr))
        pass
    except ValueError as verr:
        logging.error(str(datetime.datetime.now()) + " Unexpected error occurred {0}".format(verr))
        pass
    except:
        logging.error(str(datetime.datetime.now()) + " Unexpected error occurred {0}".format(sys.exc_info()[0]))
        pass
    finally:
        if conn:
            conn.close()
    return(ret)