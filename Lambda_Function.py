import json
import boto3
from decimal import Decimal

# Initialize the boto3 DynamoDB client and resource
client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")

# Define the DynamoDB table
table = dynamodb.Table('SecurityControls')

def lambda_handler(event, context):
    print(event)
    # Initialize the response body and status code
    body = {}
    statusCode = 200

    try:
        # Handle DELETE /items/{mainID} request
        if event['routeKey'] == "DELETE /items/{mainID}":
            # Delete the item with the provided mainID
            table.delete_item(
                Key={'mainID': event['pathParameters']['mainID']})
            body = f'Deleted item {event['pathParameters']['mainID']}'
        
        # Handle GET /items/{mainID} request
        elif event['routeKey'] == "GET /items/{mainID}":
            # Get the item with the provided mainID
            response = table.get_item(
                Key={'mainID': event['pathParameters']['mainID']})
            body = response.get("Item", {})
        
        # Handle GET /items request (fetch all items)
        elif event['routeKey'] == "GET /items":
            # Scan the table and retrieve all items
            response = table.scan()
            body = response.get("Items", [])
        
        # Handle PUT /items request (add a new item)
        elif event['routeKey'] == "PUT /items":
            # Parse the request body from the event
            request_body = json.loads(event['body'])
        
            # Check for required fields
            required_fields = ['mainID', 'mainDescription', 'domain', 'scope']
            missing_fields = [field for field in required_fields if field not in request_body or not request_body[field]]
            
            if missing_fields:
                # If any required fields are missing, return an error response
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": f"Missing required fields: {', '.join(missing_fields)}"})
                }
        
            # Check for duplicate mainID (ignoring case)
            # Convert mainID to lower case for comparison
            main_id_lower = request_body['mainID'].lower()
            
            # Query the table to check if an item with the same mainID exists
            existing_item = table.get_item(
                Key={'mainID': request_body['mainID']}
            ).get('Item', None)
            
            if existing_item and existing_item['mainID'].lower() == main_id_lower:
                # If a duplicate mainID is found, return an error response
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"message": f"Duplicate mainID found: {request_body['mainID']}"})
                }
        
            # If all validations pass, insert a new item in the table
            table.put_item(
                Item={
                    'mainID': request_body['mainID'],
                    'domain': request_body['domain'],
                    'mainDescription': request_body['mainDescription'],
                    'scope': request_body['scope']
                }
            )
            
            # Return success response
            return {
                "statusCode": 201,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(f'Put item {request_body["mainID"]}')
    }

            

        # Handle POST /items/{mainID} request
        elif event['routeKey'] == "POST /items/{mainID}":
            # Parse the request body from the event
            request_body = json.loads(event['body'])
        
            # Extract the mainID from the path parameters
            main_id = event['pathParameters']['mainID']
        
            # Initialize the UpdateExpression and dictionaries
            update_expression = []
            attribute_values = {}
            attribute_names = {}  # Dictionary to map attribute names to placeholders
        
            # Iterate through the keys in request_body
            for key, value in request_body.items():
                # Skip updating mainID as it is part of the key
                if key == 'mainID':
                    continue
        
                # Create a placeholder for attribute names
                placeholder = f"#{key}"
                attribute_names[placeholder] = key
                
                # Add to update_expression and attribute_values
                update_expression.append(f"{placeholder} = :{key}")
                attribute_values[f":{key}"] = value
        
            # Join the update_expression list into a single string
            if update_expression:
                update_expression = "SET " + ", ".join(update_expression)
                
                # Perform the update operation
                table.update_item(
                    Key={'mainID': main_id},
                    UpdateExpression=update_expression,
                    ExpressionAttributeNames=attribute_names,
                    ExpressionAttributeValues=attribute_values
                )
        
                # Set the response body
                body = f'Updated item {main_id}'
            else:
                # No updates to perform
                body = f'No updates for item {main_id}'


    
        # If the route is unsupported, handle the error
        else:
            statusCode = 400
            body = f'Unsupported route: {event["routeKey"]}'
    
    # Handle any other exceptions
    except Exception as e:
        statusCode = 500
        body = f'An error occurred: {str(e)}'

    # Convert the response body to JSON and return the response
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
    return response
