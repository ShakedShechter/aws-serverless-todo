import json
import uuid
from datetime import datetime
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    logger.info("Lambda triggered at %s", datetime.utcnow().isoformat())

    # Log full incoming event (avoid in production if payloads are sensitive/large)
    logger.debug("Raw event: %s", json.dumps(event))

    try:
        # Parse request body
        try:
            body = json.loads(event['body'])
            logger.debug("Parsed body: %s", body)
        except (TypeError, json.JSONDecodeError) as parse_err:
            logger.warning("Invalid JSON in request body: %s", str(parse_err))
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid request body"})
            }

        title = body.get('title')
        due_date = body.get('dueDate')

        if not title:
            logger.warning("Validation failed: 'title' is missing")
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing title"})
            }

        # Extract Cognito user ID
        try:
            user_id = event['requestContext']['authorizer']['jwt']['claims']['sub']
            logger.info("Authenticated user: %s", user_id)
        except KeyError as ke:
            logger.error("Missing JWT claim 'sub': %s", str(ke))
            return {
                "statusCode": 403,
                "body": json.dumps({"message": "Unauthorized - invalid token"})
            }

        # Generate todo item
        todo_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        logger.info("Creating todo: %s at %s", todo_id, created_at)

        item = {
            'userId': {'S': user_id},
            'todoId': {'S': todo_id},
            'title': {'S': title},
            'completed': {'BOOL': False},
            'createdAt': {'S': created_at}
        }

        if due_date:
            item['dueDate'] = {'S': due_date}
            logger.info("Added dueDate: %s", due_date)

        # Save to DynamoDB
        logger.info("Saving item to DynamoDB table 'todos'")
        dynamodb.put_item(
            TableName='todos',
            Item=item,
            ConditionExpression="attribute_not_exists(userId) AND attribute_not_exists(todoId)"
        )
        logger.info("Todo %s saved successfully for user %s", todo_id, user_id)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "todoId": todo_id,
                "title": title,
                "completed": False,
                "createdAt": created_at,
                "dueDate": due_date
            })
        }

    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"})
        }
