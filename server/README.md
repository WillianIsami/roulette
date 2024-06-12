# Backend with Django

This project is a Django-based application that provides an API for a betting game, specifically a roulette game. It includes functionalities such as user registration, authentication, token management, and spinning the roulette wheel with various types of bets. The API is designed to be used with Django REST Framework and DRF-YASG for Swagger documentation.

## Routes

The application defines several API endpoints:

### Authentication and User Management

- `/api/login`: Allows users to obtain a pair of JWT tokens (access and refresh tokens) upon successful login.
- `/api/logout`: Logs out the user by deleting the access token cookie.
- `/api/is-authenticated`: Checks if the user is authenticated.
- `/api/register`: Registers a new user.

### Betting Game

- `/api/bets`: Retrieves available bets.
- `/api/spin`: Spins the roulette wheel and processes the bets.

### Documentation

- `/swagger`: Provides interactive API documentation using Swagger UI.
- `/redoc`: Provides interactive API documentation using ReDoc.
- `/swagger.<format>`: Provides the raw FORMAT schema for the API.
    - Example: `/swagger.json`: Provides the raw JSON schema for the API.

## Models

- `User`: Represents the user who plays the game.
- `Wallet`: Represents the user's wallet balance.
- `Transaction`: Represents transactions made during the game, including wins and losses.

## Views

- `UserCreateView`: Handles user creation.
- `LogoutView`: Handles logout functionality.
- `IsAuthenticatedView`: Checks if the user is authenticated.
- `BetApiView`: Retrieves available bets.
- `SpinRouletteView`: Processes bets and spins the roulette wheel.
- `CookieTokenObtainPairView`: Obtains a pair of JWT tokens and sets an access token cookie.
- `CookieTokenRefreshView`: Refreshes JWT tokens and sets a new access token cookie.

## Dependencies

- Django
- Django REST Framework
- DRF-YASG
- SimpleJWT

## Setup

To run the project locally, ensure you have Python installed and follow these steps:

1. Clone the repository.
2. Navigate to the backend directory `cd server/api`
3. Install dependencies using `pip install -r requirements.txt`.
4. Create a `.env` file with the corresponding credentials from `.env.example` for database configurations and secret keys.
5. Run migrations with `python manage.py migrate`.
6. Start the development server with `python manage.py runserver`.

## Tests

To run tests `python manage.py test roulette`

## Usage

Use the API endpoints as described above to interact with the betting game. Ensure proper authentication is handled for protected endpoints.
