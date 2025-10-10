# Todo App Backend

This is the backend API for the Todo application built with Python Flask and MongoDB.

## Features

- RESTful API for todo management
- MongoDB database integration with environment configuration
- CRUD operations (Create, Read, Update, Delete)
- Toggle todo completion status
- Search todos by title or description
- Cross-Origin Resource Sharing (CORS) enabled
- Health check endpoint
- Environment-based configuration

## API Endpoints

### Base URL

```
http://localhost:5000
```

### Endpoints

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| GET    | `/`                     | Home endpoint           |
| GET    | `/health`               | Health check            |
| GET    | `/api/todos`            | Get all todos           |
| POST   | `/api/todos`            | Create a new todo       |
| GET    | `/api/todos/:id`        | Get a specific todo     |
| PUT    | `/api/todos/:id`        | Update a todo           |
| DELETE | `/api/todos/:id`        | Delete a todo           |
| PATCH  | `/api/todos/:id/toggle` | Toggle todo completion  |
| GET    | `/api/todos/search?q=`  | Search todos by keyword |

## Setup and Installation

### Prerequisites

- Python 3.7+
- MongoDB (local installation or MongoDB Atlas)

### Installation Steps

1. Navigate to the backend directory:

```bash
cd backend
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

5. Set up environment variables:

Copy the example environment file and configure it:

```bash
copy .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/todoapp
# For MongoDB Atlas: MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/todoapp

# Database Configuration
DATABASE_NAME=todoapp
COLLECTION_NAME=todos

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

6. Ensure MongoDB is running:

- **Local MongoDB**: Start your local MongoDB service
- **MongoDB Atlas**: Ensure your cluster is active and connection string is correct

7. Run the application:

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Example API Usage

### Create a Todo

```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "description": "Build a todo app with Flask and MongoDB"}'
```

### Get All Todos

```bash
curl http://localhost:5000/api/todos
```

### Search Todos

```bash
curl "http://localhost:5000/api/todos/search?q=Flask"
```

### Update a Todo

```bash
curl -X PUT http://localhost:5000/api/todos/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask Framework", "completed": true}'
```

### Toggle Todo Status

```bash
curl -X PATCH http://localhost:5000/api/todos/507f1f77bcf86cd799439011/toggle
```

### Delete a Todo

```bash
curl -X DELETE http://localhost:5000/api/todos/507f1f77bcf86cd799439011
```

## Database Configuration

This application uses MongoDB as the database. You have two options:

### Option 1: Local MongoDB

1. Install MongoDB locally
2. Start MongoDB service
3. Use connection string: `mongodb://localhost:27017/todoapp`

### Option 2: MongoDB Atlas (Cloud)

1. Create a free MongoDB Atlas account
2. Create a cluster
3. Get your connection string
4. Update MONGO_URI in `.env` file:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/todoapp?retryWrites=true&w=majority
   ```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

| Variable          | Description                       | Default                             |
| ----------------- | --------------------------------- | ----------------------------------- |
| `FLASK_ENV`       | Flask environment mode            | `development`                       |
| `FLASK_DEBUG`     | Enable Flask debug mode           | `True`                              |
| `SECRET_KEY`      | Flask secret key for sessions     | Required in production              |
| `MONGO_URI`       | MongoDB connection string         | `mongodb://localhost:27017/todoapp` |
| `DATABASE_NAME`   | MongoDB database name             | `todoapp`                           |
| `COLLECTION_NAME` | MongoDB collection name for todos | `todos`                             |
| `HOST`            | Server host address               | `0.0.0.0`                           |
| `PORT`            | Server port number                | `5000`                              |

## Development

The application now uses MongoDB for persistent storage. Features include:

- **Automatic Database Indexing**: Optimized queries with created_at and text search indexes
- **Error Handling**: Comprehensive error handling for database operations
- **Logging**: Detailed logging for debugging and monitoring
- **Data Validation**: Input validation and sanitization
- **Search Functionality**: Text search across todo titles and descriptions

## Project Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py              # MongoDB Todo model
│   ├── routes/
│   │   ├── __init__.py
│   │   └── todo_routes.py       # API endpoints with MongoDB integration
│   ├── database.py              # MongoDB connection and management
│   └── __init__.py              # Flask app factory with database setup
├── config.py                    # Environment-based configuration
├── app.py                       # Main application entry point
├── requirements.txt             # Python dependencies including MongoDB
├── .env.example                 # Environment variables template
├── .env                         # Environment variables (not in git)
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## Troubleshooting

### MongoDB Connection Issues

1. **Local MongoDB**: Ensure MongoDB service is running
2. **MongoDB Atlas**: Check cluster status and connection string
3. **Network Issues**: Verify firewall settings and IP whitelist
4. **Authentication**: Ensure username/password are correct

### Environment Issues

1. Ensure `.env` file exists and has correct values
2. Check that `python-dotenv` is installed
3. Verify environment variables are loaded correctly

### Dependency Issues

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
