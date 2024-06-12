# Vue Frontend README

This Vue.js frontend is designed to complement the backend API for a betting game, providing a user interface for players to interact with the game. It utilizes Vue Router for navigation, Vuex for state management, Vuelidate for form validation, Axios for HTTP requests, Bootstrap for styling, and ESLint & Prettier for code quality and formatting.

## Features

- **Authentication**: Users can log in and register through dedicated views.
- **Gameplay**: Players can view available bets and place bets on the roulette wheel.
- **Informational Pages**: Includes home, about, and FAQ pages.

## Routing

The application uses Vue Router to handle navigation between different components:

- **Home (`/`)**: Displays the landing page.
- **About (`/about`)**: Shows information about the game.
- **Bets (`/bets`)**: Lists available bets for the game.
- **FAQ (`/faq`)**: Contains frequently asked questions about the game.
- **Login (`/login`)**: Allows users to log in.
- **Register (`/register`)**: Enables new users to sign up.

## Navigation Guard

A global beforeEach guard is implemented to check if a route requires authentication. If a user tries to navigate to a protected route without being authenticated, they are redirected to the login page.

## Store

Vuex is used for state management, allowing components to access shared state across the application. This includes checking if a user is authenticated.

## Validation

Vuelidate is integrated for form validation, ensuring that user inputs meet the necessary criteria before submission.

## Styling

Bootstrap is utilized for styling the application, providing a responsive and modern design.

## Development Tools

- **ESLint**: Ensures code quality and enforces coding standards.
- **Prettier**: Automatically formats code to maintain consistency.

## Getting Started

To run the frontend locally, follow these steps:

1. Clone the repository.
2. Navigate to the frontend directory: `cd frontend`
3. Create a `.env` file with the corresponding credentials from `.env.example` to connect with django api.
4. Install dependencies using `npm install` or `yarn`.
5. Start the development server with `npm run serve` or `yarn serve`.
