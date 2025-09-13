# Medical Personal Account API

A RESTful API for a medical personal account system that allows users to manage their profiles and lab results.

## Features

- User profile management (username, age, gender)
- Lab results upload and management
- History of lab results retrieval
- Swagger documentation
- SQLite database (with ability to switch to PostgreSQL)

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd medapi
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Running Locally

Start the application with:

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`.

### Running with Docker

#### Using the Deployment Script

The project includes a deployment script that simplifies Docker operations:

```bash
# Make the script executable
chmod +x deploy.sh

# Start the application with SQLite
./deploy.sh start

# Start the application with PostgreSQL
./deploy.sh start-postgres

# Stop the application
./deploy.sh stop

# View logs
./deploy.sh logs

# Rebuild the Docker image
./deploy.sh rebuild
```

#### Manual Docker Commands

1. Build and start the Docker containers:

```bash
docker-compose up -d
```

2. To stop the containers:

```bash
docker-compose down
```

3. To view logs:

```bash
docker-compose logs -f
```

### API Documentation

- API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Users

- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get list of users
- `GET /api/v1/users/{user_id}` - Get user details
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Lab Results

- `POST /api/v1/results/` - Upload a new lab result
- `GET /api/v1/results/` - Get all lab results
- `GET /api/v1/results/user/{user_id}` - Get lab results for a specific user
- `GET /api/v1/results/{result_id}` - Get lab result details
- `PUT /api/v1/results/{result_id}` - Update lab result
- `DELETE /api/v1/results/{result_id}` - Delete lab result

## Database Configuration

The application uses SQLite by default. To switch to PostgreSQL:

### Using Environment Variables

1. Set the following environment variables:
   - `DB_TYPE=postgresql`
   - `POSTGRES_SERVER`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`

### Using Docker Compose

Option 1: Using the provided PostgreSQL configuration
```bash
docker-compose -f docker-compose.postgres.yml up -d
```

Option 2: Modify the default docker-compose.yml
1. Uncomment the PostgreSQL service in `docker-compose.yml`
2. Set the environment variable for the API service:
   ```yaml
   environment:
     - DB_TYPE=postgresql
     - POSTGRES_SERVER=db
     - POSTGRES_USER=postgres
     - POSTGRES_PASSWORD=postgres
     - POSTGRES_DB=medapi
   ```
3. Add the depends_on configuration to the API service:
   ```yaml
   depends_on:
     - db
   ```
4. Uncomment the volumes section
5. Restart the containers with `docker-compose up -d`

## Frontend Integration

The API is designed to work with a React frontend and includes CORS middleware to enable cross-origin requests.

## License

[MIT License](LICENSE)
