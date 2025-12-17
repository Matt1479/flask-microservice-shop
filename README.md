# flask-microservice-shop

A **microservice-based system** written in **Python and Flask**, consisting of multiple independent services communicating through an **API gateway**, with a **client web application** used to interact with the system.

This project is a continuation of my previous project: [Flask-Microservice](https://github.com/Matt1479/flask-microservice).

The goal of this project was to better understand **microservices**, **API gateways**, **authentication/authorization** with **JWT**, and **containerized development** using Docker and Docker Compose.

## Table of Contents

- [Overview](#overview)
- [What I Learned](#what-i-learned)
- [System Components](#system-components)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Ports](#ports)
- [Setup & Run](#setup--run)
- [API Overview](#api-overview)
- [Security & Authentication](#security--authentication)
- [References](#references)
- [License](#license)

## Overview

The system consists of five independent components:
- 3 microservices (auth, products, logs)
- API gateway (single entry point)
- Client web application

All components are:
- Written in Python and Flask
- Developed in virtual environments
- Fully containerized
- Run with Docker Compose

The client communicates **only with the API gateway**, never directly with the microservices.

```
Client -> API Gateway -> Internal Services
```

Key ideas:
- API gateway handles routing, authentication, and user identity extraction/forwarding
- Microservices are isolated at the network level
- Authentication is based on JWT stored in cookies
- User identity is extracted by the API gateway and forwarded to internal services via headers  (`X-User-Id`, `X-User-Role`)

## What I Learned

This project helped me understand and practice:

- Building a system composed of microservices
- Implementing and connecting an API gateway
- Building independent Flask microservices
- Designing a REST API
- Working with virtual environments
- Implementing a JWT-based authentication and role-based authorization
- Using Postman to test APIs
- Containerizing services with Docker
- Running multi-container systems with docker-compose
- Building a larger Flask project
- Fetching data from a public API ([dummyjson](https://dummyjson.com/))

## System Components

1. Products Service (Microservice - CRUD)
    - REST API for product management
    - Full CRUD operations
    - Permissions:
        - Admin users: create, update, delete
        - Regular users: read-only access
    - Initial product data fetched from:
        - https://dummyjson.com/
2. Authentication Service (Microservice)
    - User login (JWT-based), logout
    - JWT generation and validation
    - User roles (`admin`, `user`)
    - User database stored in a JSON file (`users.json`)
    - JWT stored in cookies
3. Logs Service (Microservice)
    - Records user/system actions:
        - login
        - logout
        - CRUD operations
    - Stores:
        - id
        - user ID
        - role
        - HTTP method
        - endpoint
        - payload (optional)
        - timestamp
    - Logs can be viewed by admin users only
    - Logs are stored in memory and reset on service restart
4. API Gateway
    - Central point of communication between client and services
    - Single API Entrypoint: the API gateway receives HTTP requests from the client and routes them to the appropriate microservice
    - Responsibilities:
        - Request routing
        - JWT verification
        - Extracting user identity from JWT and forwarding it via headers (`X-User-Id`, `X-User-Role`)
        - Forwarding requests to microservices
    - Prevents direct access to services by exposing only the gateway outside the Docker (private) network
5. Client Application
    - Flask-based web UI
    - Allows:
        - Login / logout
        - Authorized CRUD operations
        - Viewing logs (admin only)
    - Communicates with services through the API gateway
    - Uses server-side sessions (`Flask-Session`)

## Tech Stack

- Python
- Flask
- JWT (PyJWT)
- Docker
- Docker Compose
- Postman
- Requests

## Project Structure

```bash
flask-microservice-shop/
 ├── auth/      # Authentication microservice
 ├── logs/      # Logs microservice
 ├── products/  # Products CRUD microservice
 ├── gateway/   # API gateway
 ├── client/    # Client web application
 ├── docker-compose.yml
 └── README.md
```

## Ports

```json
{
    "client":           3000,
    "gateway":          5000,
    "auth":             5001,
    "products":         5002,
    "logs":             5003
}
```

> Note: Only the client and gateway ports are exposed to the host
> Internal service ports are accessible only within the Docker network

## Setup & Run

### Requirements

- Docker
- Docker Compose

### Clone this Repository

1. Clone the repository:
    ```bash
    git clone https://github.com/Matt1479/flask-microservice-shop
    cd flask-microservice-shop
    ```

2. (Optional) Change Git remote URL to avoid pushing to the original:
    ```bash
    git remote set-url origin <your_repo_url>
    git remote -v # confirm the change
    ```

### Environment Variables

Create a `.env` file in the project root and set the `SECRET_KEY`:

```env
SECRET_KEY=your-secret-key
```

- The `SECRET_KEY` is used for JWT encoding and decoding
- It should be a sufficiently long (e.g. 24+ characters), random string
- The same value is shared between the API gateway and auth service

### Build & Run

```bash
docker-compose up --build
```

After startup:
- Client: http://localhost:3000
- Gateway: http://localhost:5000

## API Overview

### Auth Service

- `POST /api/auth/login`
- `DELETE /api/auth/logout`

### Products Service

- `GET /api/products`
- `GET /api/products/<id>`
- `POST /api/products/add` (admin only)
- `PUT /api/products/update` (admin only)
- `DELETE /api/products/delete/<id>` (admin only)

### Logs Service

- `POST /api/logs`
- `GET /api/logs` (admin only)

All API calls are routed through the API gateway.

## Security & Authentication

- JWT stored in cookies
- JWT verified only in the API gateway
- Gateway extracts user identity from JWT and forwards it via headers
- Services rely on identity headers provided by the API gateway
- Services are not publicly accessible and are reachable only inside a private Docker network
- Role-based access control enforced per service

## References

Articles that helped me understand microservices, API gateways, and containerization:
- https://kinsta.com/blog/python-microservices/
- https://medium.com/@shaliamekh/api-gateway-for-your-microservices-98a779808550

HTTP status codes reference:
- https://http.cat/

## License

[MIT](LICENSE)
