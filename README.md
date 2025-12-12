# Microservices

## System Components

1. CRUD (Micro) Service - REST API
    - Item catalog
    - CRUD
        - CRUD permissions for authorized users/admins
        - Read-only permission for everyone
2. Authentication (Micro) Service
    - Login and Register
    - Authentication and authorization using JWT
    - User database (`users.json`)
3. Logs (Micro) Service
    - Recording the actions of users/system (e.g. adding an item, logging in)
    - Reading logs
4. API Gateway
    - Central point of communication between client and services
    - Single API Entrypoint: API Gateway receives HTTP requests and routes them to the appropirate microservice
5. Client Application
    - Display operations such as:
        - Login/register
        - Authorized CRUD actions on data
        - Display of logs

## Project Structure

```bash
microservices/
 ├── auth-service/   # Authentication & authorization (JWT)
 ├── crud-service/   # REST API; TODO: Name it
 ├── logs-service/   # Logs (in memory)
 ├── gateway/        # API Gateway
 └── client/         # Client application
```
