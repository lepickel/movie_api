# Movie API with Serverless Functions

## Project Overview
This project is a serverless application that provides an API to retrieve movie information stored in a DynamoDB table. The API has two serverless functions: 
1. `GetMovies`: Returns all movies in the database.
2. `GetMoviesByYear`: Returns a list of movies released in a specified year.

Each movie has associated metadata such as its title, genre, rating, and a URL to its cover image hosted in S3 cloud storage.

## Related Projects

If you want to upload movie cover images to an S3 bucket, you can use the file upload functionality from one of my previous projects. 

**[S3 File Upload Project](https://github.com/lepickel/s3upload)**  
This is a simple Bash script that uploads a local file to an AWS S3 bucket.

## Features
- **NoSQL Database (DynamoDB):** Stores movie metadata including title, year, genre, rating, and a cover image URL.
- **Cloud Storage (S3):** Stores cover images for each movie.
- **Serverless Functions (Lambda):** Functions to fetch all movies or movies by a specified year.
- **API Gateway:** Exposes the Lambda functions as a publicly accessible API.

## Architecture
The project uses the following AWS services:
- **DynamoDB** for storing movie metadata.
- **S3** for storing movie cover images.
- **Lambda** for handling API requests.
- **API Gateway** for routing requests to Lambda functions.

## Data Structure
The DynamoDB table (`Movies`) contains the following attributes:
- **year** (Partition Key) – String
- **title** (Sort Key) – String
- **genre** – String
- **rating** – String
- **cover_url** – String (S3 URL for the movie's cover image)

### Example Movie Data
```json
{
    "year": "1993",
    "title": "Jurassic Park",
    "genre": "Adventure/Sci-fi",
    "rating": "8.2",
    "cover_url": "https://python-project-jp-movie-posters.s3.amazonaws.com/jp1.jpg"
}
```

## API Endpoints

### 1. Get All Movies

**URL:** `/movies`  
**Method:** `GET`  
**Description:** Returns a JSON list of all movies in the database.

#### Response Example:
```json
[
    {
        "year": "1993",
        "title": "Jurassic Park",
        "genre": "Adventure/Sci-fi",
        "rating": "8.2",
        "cover_url": "https://python-project-jp-movie-posters.s3.amazonaws.com/jp1.jpg"
    },
    {
        "year": "1997",
        "title": "The Lost World: Jurassic Park",
        "genre": "Sci-fi/Action",
        "rating": "6.6",
        "cover_url": "https://python-project-jp-movie-posters.s3.amazonaws.com/jp2.jpg"
    }
]
```

### 2. Get Movies By Year

**URL:** `/movies?year={year}`  
**Method:** `GET`  
**Description:** Returns a list of movies released in a specific year. The year is provided as a query parameter.

#### Query Parameter:
- **year** (required) – The release year of the movies.

#### Response Example:
```json
[
    {
        "title": "Jurassic Park",
        "year": "1993",
        "genre": "Adventure/Sci-fi",
        "rating": "8.2",
        "cover_url": "https://python-project-jp-movie-posters.s3.amazonaws.com/jp1.jpg"
    }
]
```

#### Error Handling:
- If the `year` parameter is missing or empty, the API returns a `400 Bad Request` response:
  ```json
  {
      "error": "Year parameter is required and cannot be blank."
  }
  ```

- If no movies are found for the given year, the API returns a `404 Not Found` response:
  ```json
  {
      "message": "No movies found for the year {year}."
  }
  ```

## How to Run the Project

### Prerequisites
- AWS CLI installed and configured.
- Boto3 installed: `pip install boto3`.
- DynamoDB table and S3 bucket set up.

### Setup

1. **DynamoDB Setup**  
   Run the `dynamodb_setup.py` script to create the DynamoDB table and populate it with movie data:
   ```bash
   python dynamodb_setup.py
   ```

2. **Deploy Lambda Functions**  
   Deploy the Lambda functions for `GetMovies` and `GetMoviesByYear` through the AWS Lambda Console or using the AWS CLI.

3. **API Gateway**  
   Set up API Gateway to expose the Lambda functions as API endpoints.

## API Gateway Setup

To make the Lambda functions accessible via HTTP requests, you'll need to set up an API Gateway. Here's how you can do it:

### Steps to Set Up API Gateway

1. **Create a New API**  
   - Log in to your AWS Management Console.
   - Go to **API Gateway** and click **Create API**.
   - Choose **HTTP API** for a simpler setup or **REST API** for more features (the setup is similar for both).

2. **Configure API Routes**
   - Add a route for the `GetMovies` function:
     - HTTP method: `GET`
     - Path: `/movies`
   - Add a route for the `GetMoviesByYear` function:
     - HTTP method: `GET`
     - Path: `/movies?year={year}`

3. **Integrate API with Lambda Functions**
   - For each route, specify the integration type as **Lambda Function**.
   - Choose the appropriate Lambda function (`GetMovies` or `GetMoviesByYear`).
   - Ensure that you grant API Gateway permission to invoke your Lambda function by adding the appropriate role or policy.

4. **Deploy the API**
   - Click **Deploy** and give your deployment a stage name, like `dev` or `prod`.
   - After deployment, you'll get an API endpoint URL that can be used to access your Lambda functions.

5. **Testing the API**
   - Open a browser or use a tool like `curl` to test the API.
     - Example request for all movies:  
       ```bash
       curl -X GET "https://your-api-id.execute-api.region.amazonaws.com/dev/movies"
       ```
     - Example request for movies by year:  
       ```bash
       curl -X GET "https://your-api-id.execute-api.region.amazonaws.com/dev/movies?year=1993"
       ```

### Optional: Secure the API
To add an extra layer of security, you can integrate API Gateway with AWS IAM, Lambda authorizers, or API keys to restrict access to your API.

## Future Enhancements
- Add additional search functionality, such as querying an AI API for movie summaries.
- Integrate user authentication for secured access to the API.

## License
This project is licensed under the MIT License.
