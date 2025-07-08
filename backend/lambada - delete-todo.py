import json
import boto3
import logging

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'todos'

def lambda_handler(event, context):
    logger.info("Lambda invoked to delete a todo item")

    try:
        logger.debug("Event received: %s", json.dumps(event))

        # Extract todoId from path parameters
        todo_id = event['pathParameters']['todoId']
        logger.info("Extracted todoId: %s", todo_id)

        # Extract user ID from Cognito token claims
        user_id = event['requestContext']['authorizer']['jwt']['claims']['sub']
        logger.info("Extracted userId from token: %s", user_id)

        # Attempt to delete item from DynamoDB
        response = dynamodb.delete_item(
            TableName=TABLE_NAME,
            Key={
                'userId': {'S': user_id},
                'todoId': {'S': todo_id}
            },
            ConditionExpression='attribute_exists(todoId)'  # Ensure item exists
        )

        logger.info("Todo %s deleted successfully for user %s", todo_id, user_id)
        logger.debug("DynamoDB delete_item response: %s", response)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Todo {todo_id} deleted successfully'})
        }

    except dynamodb.exceptions.ConditionalCheckFailedException:
        logger.warning("Todo %s not found for user %s", todo_id, user_id)
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Todo not found'})
        }

    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
