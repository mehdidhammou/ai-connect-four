# Connect Four: Classic AI vs LLMs.

## Introduction

Test your skills against two generations of AI.

### Good Old-Fashioned AI

Play against two of the most unbeatable heuristics in a game of connect four, using a classic adversarial search algorithm minimax with alpha-beta pruning. with hand-designed explicit rule mapping states to scores.

### Modern LLMs

Play against state-of-the-art LLMs that use in-context learning and few-shot prompting techniques to understand and find the best move to play.

## Setup

### Prerequisites

- Docker and Docker Compose.
- Mistral API key.

### Environment Variables

#### Backend

Create a `.env` file in the `backend` directory

```env
cp ./backend/.env.example ./backend/.env
```

Set your Mistral API key:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

and finally an `.env` file in the `frontend` directory

```env
cp ./frontend/.env.example ./frontend/.env
```

### Start the application

```bash
docker compose up
```

The application will be available at `http://localhost:8000`.
the API docs will be available at `http://localhost:5000/docs`.

## Architecture

The following illustration demonstrates the dependencies between the classes.

![Data Model](docs/data_model.svg)

A Solver is either a heuristic or an LLM provider, both inherit the `Solver` base class.

If you want to add more heuristics, inherit the `Heuristic` class and register it in the `heuristicFactory` in `api/main.py`.

To add more LLM providers, inherit the `ModelProvider` class and register it in the `ModelProviderFactory` in `api/main.py`.

Then add the provider's name to `ModelProviderName` Literal in `backend/src/types/model_provider_name.py`. `SolverType` model then validates the input.

The API primarily interacts with the `Game` class, which manages the game state and logic, the API is stateless which means the board state is passed with each request and is validated on the backend.

## API

API consumers can POST moves with the following payload, where `solver` is either `heuristic` or an LLM provider's name (defined in ModelProviderName), and `name` is the name of the heuristic or the chosen model respectively.

```json

curl -X POST http://localhost:5000/move/{solver}/{name} \
  -H "Content-Type: application/json" \
  -d '
{
  "board": [[...]],
  "player_move": {"col": 3, "row": 5}
}
'
```

**Response**

```json
{
  "state": "CONTINUE",
  "solver_move": {"col": 2, "row": 4},
  "winning_sequence": [{}...]
}
```

When the CPU plays first, request the initial move using the endpoint below.

```json
curl -X GET http://localhost:5000/first-move/{solver}/{name} \
  -H "Content-Type: application/json"
```

**Response**

```json
{
  "data": {
    "col": number,
    "row": number
  }
}
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to open issues or pull requests for bug fixes, improvements, or additional features.
