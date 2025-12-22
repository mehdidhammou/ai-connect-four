import os
from contextlib import asynccontextmanager
from typing import get_args

from api.schemas.api_response import ApiResponse
from api.schemas.auto_move_request import AutoMoveRequest
from api.schemas.board_request import BoardRequest
from api.schemas.model import Model
from api.schemas.move_request import MoveRequest
from api.schemas.move_response import MoveResponse
from api.schemas.response import Response
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.board import ConnectFourBoard
from src.game import Game
from src.heuristic import (
    CountPiecesHeuristic,
    CountPositionsHeuristic,
    HeuristicFactory,
)
from src.model import MistralModelProvider, ModelProviderFactory
from src.solver import MinimaxAlphaBetaPruningSolver
from src.solver.llm_based_solver import LLMBasedSolver
from src.types.heuristic_enum import HeuristicEnum
from src.types.model_provider_enum import ModelProviderEnum
from src.types.solver_type import SolverType
from src.utils import get_solver


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    HeuristicFactory.register(HeuristicEnum.PIECES, CountPiecesHeuristic)
    HeuristicFactory.register(HeuristicEnum.POSITIONS, CountPositionsHeuristic)
    ModelProviderFactory.register(
        ModelProviderEnum.MISTRAL,
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


@app.get("/")
async def index():
    return ConnectFourBoard().state


@app.get("/ping", response_model=ApiResponse[dict])
async def ping():
    return ApiResponse(data={"message": "pong"})


@app.get("/solvers", response_model=ApiResponse[list[SolverType]])
async def get_solvers():
    solvers = [
        solver(type=type_literal, name=name)
        for solver in get_args(SolverType)
        for type_literal in solver.model_fields["type"].annotation.__args__
        for name in solver.model_fields["name"].annotation
    ]

    return ApiResponse(data=solvers)


@app.get("/models/{provider}", response_model=ApiResponse[list[Model]])
async def get_provider_models(provider: ModelProviderEnum):
    try:
        model_provider = ModelProviderFactory.create(provider)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ApiResponse(data=model_provider.get_models())


@app.post("/get_move")
async def get_move(data):
    try:
        heuristic = HeuristicFactory.create(name=data.heuristic)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    solver = MinimaxAlphaBetaPruningSolver(heuristic=heuristic, depth=4)
    board = ConnectFourBoard(initial_state=data.board)

    game = Game(
        board=board,
        solver=solver,
        auto=True,
    )

    print(heuristic.id)
    game.get_solver_move(piece=heuristic.id)

    response = Response(
        board=game.board.state,
        state=game.state,
        message=game.state.value,
        sequence=game.get_winning_sequence(),
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
        auto=False,
    )

    response = Response(
        board=game.board.state,
        state=game.state.name,
        message=game.state.value,
        sequence=game.board.winning_sequence,
    )

    if game.is_over():
        return JSONResponse(content=response.__dict__)

    # Let the bot make its move
    game.get_solver_move(piece=2)

    response.message = game.state.value
    response.board = game.board.state
    response.state = game.state.name
    response.sequence = game.board.winning_sequence

    return JSONResponse(content=response.__dict__)


# TODO: it's possible to merge /move and /auto_move endpoints into one by making combining player and solver types
@app.post("/move", response_model=ApiResponse[MoveResponse])
async def move(data: MoveRequest):
    try:
        solver = get_solver(data.solver)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    board = ConnectFourBoard(initial_state=data.board)

    game = Game(
        board=board,
        solver=solver,
        auto=False,
    )

    try:
        # play the player's move first
        game.make_move(move=data.player_move, piece=data.player_piece)

        best_move = None
        if not game.is_over():
            best_move = game.get_solver_move(piece=data.solver_piece)
            if best_move is not None:
                game.make_move(move=best_move, piece=data.solver_piece)

        return ApiResponse(
            data=MoveResponse(
                state=game.state,
                move=best_move,
                sequence=game.get_winning_sequence(),
            )
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auto_move", response_model=ApiResponse[MoveResponse])
async def auto_move(data: AutoMoveRequest):
    try:
        solver_one = get_solver(data.solver_one)
        solver_two = get_solver(data.solver_two)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    board = ConnectFourBoard(initial_state=data.board)
    game = Game(
        board=board,
        solver=solver_one,
        auto=True,
    )
    try:
        best_move = game.get_solver_move(piece=data.current_piece)
        if best_move is not None:
            game.make_move(move=best_move, piece=data.current_piece)

        if not game.is_over():
            game.solver = solver_two
            best_move = game.get_solver_move(piece=3 - data.current_piece)
            if best_move is not None:
                game.make_move(move=best_move, piece=3 - data.current_piece)

        return ApiResponse(
            data=MoveResponse(
                state=game.state,
                move=best_move,
                sequence=game.get_winning_sequence(),
            )
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
