from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.classes import (
    ConnectFourBoard,
    Game,
    HeuristicFactory,
    MinimaxAlphaBetaPruningSolver,
    Response,
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BoardRequest(BaseModel):
    heuristic: str
    board: list[list[int]]


@app.get("/")
async def index():
    return ConnectFourBoard().state


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/get_move")
async def get_move(data: BoardRequest):
    try:
        heuristic = HeuristicFactory.create_heuristic(heuristic=data.heuristic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    solver = MinimaxAlphaBetaPruningSolver(heuristic=heuristic, depth=4)
    board = ConnectFourBoard(initial_state=data.board)

    game = Game(
        board=board,
        solver=solver,
        cpu_vs_cpu=True,
    )

    print(heuristic.id)
    game.play(piece=heuristic.id)

    response = Response(
        success=True,
        board=game.board.state,
        state=game.state,
        message=game.state.value,
        sequence=game.board.winning_sequence,
    )

    return JSONResponse(content=response.__dict__)


@app.post("/make_move")
async def make_move(data: BoardRequest):
    try:
        heuristic = HeuristicFactory.create_heuristic(heuristic=data.heuristic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    solver = MinimaxAlphaBetaPruningSolver(heuristic=heuristic, depth=4)
    board = ConnectFourBoard(initial_state=data.board)

    game = Game(
        board=board,
        solver=solver,
        cpu_vs_cpu=False,
    )

    response = Response(
        success=True,
        board=game.board.state,
        state=game.state.name,
        message=game.state.value,
        sequence=game.board.winning_sequence,
    )

    if game.is_over():
        return JSONResponse(content=response.__dict__)

    # Let the bot make its move
    game.play(piece=2)

    response.message = game.state.value
    response.board = game.board.state
    response.state = game.state.name
    response.sequence = game.board.winning_sequence

    return JSONResponse(content=response.__dict__)
