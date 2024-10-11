import boto3
import json

# Initialize DynamoDB boto3 object
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Movies')

def lambda_handler(event, context):
    # Get query string parameters
    query_params = event.get('queryStringParameters', {})

    # Check if the year parameter is missing or blank
    if 'year' not in query_params or not query_params['year'].strip():
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Year parameter is required and cannot be blank.'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    search_year = query_params['year']

    # Query DynamoDB for movies with the specified year
    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('year').eq(search_year)
        )

        # Get items from the response
        movies = response.get('Items', [])

        # If no movies were found, return a message
        if not movies:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'No movies found for the year {search_year}.'}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        # Format the movies for the response
        formatted_movies = [{
            "title": movie.get('title', 'Unknown Title'),
            "year": movie.get('year', 'Unknown Year'),
            "genre": movie.get('genre', 'Unknown Genre'),
            "rating": movie.get('rating', 'Unknown Rating'),
            "cover_url": movie.get('cover_url', 'No URL')
        } for movie in movies]

        # Return the formatted movies
        return {
            'statusCode': 200,
            'body': json.dumps(formatted_movies, indent=4),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
