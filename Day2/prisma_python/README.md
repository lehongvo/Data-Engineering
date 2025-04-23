# FastAPI Blockchain Data Sync

A modern backend application built with FastAPI, Prisma, and PostgreSQL that synchronizes and stores Ethereum blockchain transaction data while providing REST API endpoints for data access.

![Project Architecture](https://i.imgur.com/YourImage.png)

## Features

- 🚀 **FastAPI** - High-performance web framework
- 🗃️ **Prisma** - Next-generation ORM for Python
- 🐘 **PostgreSQL** - Robust relational database
- ⛓️ **Web3** - Ethereum blockchain integration
- ⏰ **APScheduler** - Automated blockchain data synchronization
- 🔐 **Environment Configuration** - Secure configuration management
- 📚 **Swagger/ReDoc** - Interactive API documentation

## Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js (for Prisma)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:
```bash
deactivate && python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Generate Prisma client:
```bash
prisma generate
```

6. Create database and apply migrations:
```bash
prisma db push
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Blockchain Configuration
ETH_RPC_URL="https://eth.llamarpc.com"

# PostgreSQL Configuration
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="your_password"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
POSTGRES_DB="prisma_db"
POSTGRES_SCHEMA="public"
POSTGRES_SSL="false"
POSTGRES_POOL_SIZE="20"

# Application Configuration
APP_ENV="development"
DEBUG_MODE="true"
LOG_LEVEL="INFO"
```

## Database Schema

The application uses three main models:

### User
- `id`: Int (Primary Key, Auto-increment)
- `email`: String (Unique)
- `name`: String (Optional)
- `posts`: Relation to Post model
- `createdAt`: DateTime
- `updatedAt`: DateTime

### Post
- `id`: Int (Primary Key, Auto-increment)
- `title`: String
- `content`: String (Optional)
- `published`: Boolean
- `author`: Relation to User model
- `authorId`: Int (Foreign Key)
- `createdAt`: DateTime
- `updatedAt`: DateTime

### Transaction
- `id`: Int (Primary Key, Auto-increment)
- `hash`: String (Unique)
- `blockNumber`: BigInt
- `fromAddr`: String
- `to`: String
- `value`: String (Wei value)
- `gasPrice`: String
- `gas`: String
- `timestamp`: DateTime
- `status`: Boolean
- `createdAt`: DateTime
- `updatedAt`: DateTime

## API Endpoints

### Users
- `GET /users` - List all users
- `POST /users` - Create a new user
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Posts
- `GET /posts` - List all posts
- `POST /posts` - Create a new post
- `GET /posts/{id}` - Get post by ID
- `PUT /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Transactions
- `GET /transactions` - List all transactions
- `GET /transactions/{hash}` - Get transaction by hash

## Running the Application

1. Start the application:
```bash
pip install setuptools && uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Background Tasks

The application includes an automated blockchain data synchronization task that runs every 12 seconds to fetch and store new transaction data from the Ethereum network.

## Development

### Project Structure
```
.
├── main.py              # FastAPI application and routes
├── prisma/             
│   └── schema.prisma   # Database schema
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── README.md          # Project documentation
```

### Adding New Features

1. Update the Prisma schema in `prisma/schema.prisma`
2. Generate the Prisma client: `prisma generate`
3. Apply database changes: `prisma db push`
4. Implement new routes in `main.py`
5. Update documentation as needed

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 