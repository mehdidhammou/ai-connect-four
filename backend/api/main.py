import os
from contextlib import asynccontextmanager

from api.schemas.api_response import ApiResponse
from api.schemas.board_request import BoardRequest
from api.schemas.model import Model
from api.schemas.response import Response
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.board import ConnectFourBoard
from src.game import Game
from src.game.game_state import GameState
from src.heuristic import (
    CountPiecesHeuristic,
    CountPositionsHeuristic,
    HeuristicFactory,
)
from src.model import MistralModelProvider, ModelProviderFactory
from src.solver import MinimaxAlphaBetaPruningSolver
from src.types.heuristic_enum import HeuristicEnum

from backend.api.schemas.move import Move


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    HeuristicFactory.register(HeuristicEnum.PIECES, CountPiecesHeuristic, id=1)
    HeuristicFactory.register(HeuristicEnum.POSITIONS, CountPositionsHeuristic, id=2)
    ModelProviderFactory.register(
        "mistral",
        MistralModelProvider,
        api_key=os.environ["MISTRAL_API_KEY"],
    )
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/heuristics", response_model=ApiResponse[list[HeuristicEnum]])
async def get_heuristics():
    return ApiResponse(data=list(HeuristicEnum))


@app.get("/")
async def index():
    return ConnectFourBoard().state


@app.get("/models/{provider}", response_model=ApiResponse[list[Model]])
async def get_provider_models(provider: str):
    try:
        model_provider = ModelProviderFactory.create(provider)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ApiResponse(data=model_provider.get_models())


@app.get("/ping", response_model=ApiResponse[dict])
async def ping():
    return ApiResponse(data={"message": "pong"})


@app.post("/get_move")
async def get_move(data: BoardRequest):
    try:
        heuristic = HeuristicFactory.create(name=data.heuristic)
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
        heuristic = HeuristicFactory.create(name=data.heuristic)
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
