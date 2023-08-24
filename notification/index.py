import os
import json
import psycopg2
import boto3

# Initialize SQS client
sqs = boto3.client('sqs')

# SQS Queue URLs mapped by channel ID
sqs_queue_urls = {
    1: os.environ['SQS_QUEUE_URL_1'],  # Set these environment variables in your Lambda function
    2: os.environ['SQS_QUEUE_URL_2'],
    3: os.environ['SQS_QUEUE_URL_3']
}

# Database connection parameters
db_params = {
    'dbname': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT']
}


def lambda_handler(event, context):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)

    try:
        # Create a new database cursor
        cur = conn.cursor()

        # SQL query to fetch records with 'PENDING' delivery_status
        sql_query = "SELECT id, id_message, id_channel FROM delivery_schedule WHERE delivery_status = 'PENDING';"

        # Execute the SQL query
        cur.execute(sql_query)

        # Fetch all rows
        rows = cur.fetchall()

        for row in rows:
            delivery_id = row[0]
            message_id = row[1]
            channel_id = row[2]

            # Get the SQS Queue URL based on channel ID
            sqs_queue_url = sqs_queue_urls.get(channel_id, None)

            if sqs_queue_url is None:
                print(f"Unknown channel ID: {channel_id}. Skipping.")
                continue

            # Prepare the message for SQS
            message_body = json.dumps({
                'delivery_id': delivery_id,
                'message_id': message_id
            })

            # Send the message to the appropriate SQS queue
            sqs.send_message(
                QueueUrl=sqs_queue_url,
                MessageBody=message_body
            )

            print(f"Sent message for delivery_id: {delivery_id}, message_id: {message_id} to channel: {channel_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database cursor and connection
        cur.close()
        conn.close()
