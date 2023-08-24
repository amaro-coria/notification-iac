import os
import json
import psycopg2
import boto3

sqs = boto3.client('sqs')
sqs_queue_url = os.environ['SQS_QUEUE_URL_1']

db_params = {
    'dbname': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT']
}


def lambda_handler(event, context):
    conn = psycopg2.connect(**db_params)

    try:
        cur = conn.cursor()

        response = sqs.receive_message(
            QueueUrl=sqs_queue_url,
            MaxNumberOfMessages=10
        )

        if 'Messages' in response:
            messages = response['Messages']
            for message in messages:
                message_body = json.loads(message['Body'])

                delivery_id = message_body['delivery_id']
                message_id = message_body['message_id']

                # TODO: Handle SMS/Email and similar sending here, Define a function and lambda for each type of delivery

                sql_query = f"UPDATE delivery_schedule SET delivery_status = 'SENT' WHERE id = {delivery_id};"
                cur.execute(sql_query)
                conn.commit()

                sqs.delete_message(
                    QueueUrl=sqs_queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )

                print(f"Updated delivery_status for delivery_id: {delivery_id}, message_id: {message_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cur.close()
        conn.close()
