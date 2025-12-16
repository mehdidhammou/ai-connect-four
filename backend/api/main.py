import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api.schemas.api_response import ApiResponse
from api.schemas.model import Model
from api.schemas.response import Response
from src.board import ConnectFourBoard
from src.game import Game
from src.heuristic import (
    CountPiecesHeuristic,
    CountPositionsHeuristic,
    HeuristicFactory,
)
from src.model import MistralModelProvider, ModelProviderFactory
from src.solver import MinimaxAlphaBetaPruningSolver

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    HeuristicFactory.register("pieces", CountPiecesHeuristic, id=1)
    HeuristicFactory.register("positions", CountPositionsHeuristic, id=2)

    ModelProviderFactory.register(
        "mistral",
        MistralModelProvider,
        api_key=os.environ["MISTRAL_API_KEY"],
    )


class BoardRequest(BaseModel):
    heuristic: str
    board: list[list[int]]


@app.get("/")
async def index():
    return ConnectFourBoard().state


@app.get("/models/{provider}", response_model=ApiResponse[list[Model]])
async def get_provider_models(provider: str):
    model_provider = ModelProviderFactory.create(provider)
    return ApiResponse(data=model_provider.get_models())


@app.get("/ping")
async def ping():
    return {"message": "pong"}


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
