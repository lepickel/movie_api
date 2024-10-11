import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Create a DynamoDB table
def create_movie_table():
	table = dynamodb.create_table(
		TableName='Movies',
		KeySchema=[
			{
				'AttributeName': 'year',
				'KeyType': 'HASH' # Partition Key
			},
			{
				'AttributeName': 'title',
				'KeyType': 'RANGE' # Sort key
			}
		],
		AttributeDefinitions=[
			{
				'AttributeName': 'year',
				'AttributeType': 'S'
			},
			{
				'AttributeName': 'title',
				'AttributeType': 'S'
			}
		],
		ProvisionedThroughput={
			'ReadCapacityUnits': 10,
			'WriteCapacityUnits': 10
		}
	)
	# Wait until the table exists.
	table.meta.client.get_waiter('table_exists').wait(TableName='Movies')
	print(f"Table status: {table.table_status}")

# Add a movie
def add_movie(year, title, genre, rating, cover_url):
	table = dynamodb.Table('Movies')
	table.put_item(
		Item={
			'year': year,
			'title': title,
			'genre': genre,
			'rating': rating,
			'cover_url': cover_url
		}
	)

if __name__== "__main__":
	create_movie_table()
	add_movie('1993', 'Jurassic Park', 'Adventure/Sci-fi', '8.2', 'https://python-project-jp-movie-posters.s3.amazonaws.com/jp1.jpg')
	add_movie('1997', 'The Lost World: Jurassic Park', 'Sci-fi/Action', '6.6', 'https://python-project-jp-movie-posters.s3.amazonaws.com/jp2.jpg')
	add_movie('2001', 'Jurassic Park III', 'Sci-fi/Action', '5.9', 'https://python-project-jp-movie-posters.s3.amazonaws.com/jp3.jpg')
	add_movie('2015', 'Jurassic World', 'Action/Sci-fi', '6.9', 'https://python-project-jp-movie-posters.s3.amazonaws.com/jw1.jpg')
	add_movie('2018', 'Jurassic World: Fallen Kingdom', 'Action/Sci-fi', '6.1', 'https://python-project-jp-movie-posters.s3.amazonaws.com/jw2.png')
	add_movie('2022', 'Jurassic World Dominion', 'Action/Sci-Fi', '5.6', 'https://puthon-project-jp-movie-posters.s3.amazonaws.com/jw3.jpeg')
