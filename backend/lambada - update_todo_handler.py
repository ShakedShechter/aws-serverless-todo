import json
import boto3
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'todos'

def lambda_handler(event, context):
    try:
        logger.info("Event received: %s", json.dumps(event))

        # Extract the todo ID from the path
        todo_id = event['pathParameters']['todoId']
        logger.info(f"Todo ID: {todo_id}")

        # Get the user ID from the Cognito JWT claims
        user_id = event['requestContext']['authorizer']['jwt']['claims']['sub']
        logger.info(f"User ID: {user_id}")

        # Parse the JSON request body
        body = json.loads(event['body'])
        logger.info("Request body parsed: %s", body)

        # Prepare parts of the update expression
        set_exprs = []
        remove_exprs = []
        expression_values = {}

        if 'title' in body:
            set_exprs.append('title = :title')
            expression_values[':title'] = {'S': body['title']}
            logger.info("Title update set")

        if 'completed' in body:
            set_exprs.append('completed = :completed')
            expression_values[':completed'] = {'BOOL': body['completed']}
            logger.info("Completed status update set")

        if 'dueDate' in body:
            if body['dueDate']:
                set_exprs.append('dueDate = :dueDate')
                expression_values[':dueDate'] = {'S': body['dueDate']}
                logger.info("Due date set")
            else:
                remove_exprs.append('dueDate')
                logger.info("Due date marked for removal")

        if not set_exprs and not remove_exprs:
            logger.warning("No valid fields to update")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No valid fields to update'})
            }

        update_expr = ''
        if set_exprs:
            update_expr += 'SET ' + ', '.join(set_exprs)
        if remove_exprs:
            if update_expr:
                update_expr += ' '
            update_expr += 'REMOVE ' + ', '.join(remove_exprs)

        logger.info("Final UpdateExpression: %s", update_expr)

        update_args = {
            'TableName': TABLE_NAME,
            'Key': {
                'userId': {'S': user_id},
                'todoId': {'S': todo_id}
            },
            'UpdateExpression': update_expr,
            'ConditionExpression': 'attribute_exists(todoId)'
        }

        if expression_values:
            update_args['ExpressionAttributeValues'] = expression_values
            logger.info("ExpressionAttributeValues: %s", expression_values)

        logger.info("Updating item in DynamoDB...")
        dynamodb.update_item(**update_args)

        logger.info(f"Todo {todo_id} updated successfully")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Todo {todo_id} updated successfully'})
        }

    except dynamodb.exceptions.ConditionalCheckFailedException:
        logger.warning(f"Todo {todo_id} not found for user {user_id}")
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
