# Connect Four: Human vs AI.

## NEW: Play against LLMs

After a major refactor, the game now supports playing against popular LLMs.

Mistral models are now available to play against.

## Introduction

Play against two of the most unbeatable heuristics in a game of connect four. This project presents a Connect Four game where a human player faces off against an AI opponent implemented using the minimax algorithm with alpha-beta pruning with two heuristics.

## Architecture

The following illustration demonstrates the dependencies between the classes.

![Data Model](docs/data_model.svg)

A Solver is either a heuristic or an LLM provider.

The API primarily interacts with the `Game` class, which manages the game state and logic, the API is stateless which means the board state is passed with each request and is validated on the backend.

API consumers can POST moves with the following payload:

```json

curl -X POST http://localhost:5000/move/{solver}/{name} \
  -H "Content-Type: application/json" \
  -d '
{
  "board": [[...]],
  "starting_player" : "human",
  "player_move": {"col": 3, "row": 5}
}
'
```

Where `solver` is either `heuristic` or `llm`, and `name` is the name of the heuristic or the LLM provider.

the response will be:

```json
{
  "state": "CONTINUE",
  "solver_move": {"col": 2, "row": 4},
  "winning_sequence": [{}...]
}
```

### Setup

#### Run the docker compose file

```bash
docker compose up
```

This will build two images, the frontend and the backend, and run them in two separate containers. The frontend will be available at `http://localhost:8000` and the backend at `http://localhost:5000`.

### Usage

Open the frontend in a web browser at `http://localhost:8000` and simply follow the instructions to play the game.

### Objective

The objective of the game is to connect four of your own discs in a row, either horizontally, vertically, or diagonally, before your opponent does.

### Heuristics

#### 1. Count pieces heuristic

The first heuristic is based on the number of pieces on the board. The AI will try to maximize the number of its pieces on the board while minimizing the number of the human player's pieces.

#### 2. Count winning positions heuristic

The second heuristic is based on the number of winning positions on the board. The AI will try to maximize the number of winning positions it has while minimizing the number of winning positions the human player has.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to open issues or pull requests for bug fixes, improvements, or additional features.

Special thanks for [Ahmed Belloula](https://github.com/Ahmed-dev-code)
