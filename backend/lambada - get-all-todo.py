import json
import boto3
import logging

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')
TABLE_NAME = "todos"

def lambda_handler(event, context):
    logger.info("Lambda invoked to retrieve all todos")

    try:
        # Extract Cognito user ID
        user_id = event['requestContext']['authorizer']['jwt']['claims']['sub']
        logger.info("Authenticated user: %s", user_id)

        # Query DynamoDB for user's todos
        logger.info("Querying DynamoDB for todos of user %s", user_id)
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression='userId = :uid',
            ExpressionAttributeValues={
                ':uid': {'S': user_id}
            }
        )

        items = response.get('Items', [])
        logger.debug("DynamoDB returned %d items", len(items))

        # Transform DynamoDB records to JSON-friendly todos
        todos = []
        for item in items:
            todo = {
                'todoId': item['todoId']['S'],
                'title': item['title']['S'],
                'completed': item['completed']['BOOL'],
                'createdAt': item['createdAt']['S']
            }

            if 'dueDate' in item:
                todo['dueDate'] = item['dueDate']['S']

            todos.append(todo)

        logger.info("Returning %d todos for user %s", len(todos), user_id)

        return {
            'statusCode': 200,
            'body': json.dumps(todos)
        }

    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error'})
        }
