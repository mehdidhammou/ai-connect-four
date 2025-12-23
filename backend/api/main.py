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
from fastapi import Depends, FastAPI, HTTPException
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
from src.types.heuristic_name import HeuristicName
from src.types.model_provider_name import ModelProviderName
from src.types.solver_type import SolverType, HeuristicSolverType, LLMSolverType
from src.utils import get_solver, validate_solver_type


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    HeuristicFactory.register("pieces", CountPiecesHeuristic)
    HeuristicFactory.register("positions", CountPositionsHeuristic)
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


@app.get("/ping", response_model=ApiResponse[dict])
async def ping():
    return ApiResponse(data={"message": "pong"})


@app.get("/solvers", response_model=ApiResponse[list[SolverType]])
async def get_solvers():
    solvers = []

    # Add heuristic solvers
    for name in get_args(HeuristicName):
        solvers.append(HeuristicSolverType(type="heuristic", name=name))

    # Add LLM solvers
    for provider in get_args(ModelProviderName):
        provider_instance = ModelProviderFactory.create(provider)
        for model in provider_instance.get_models():
            solvers.append(LLMSolverType(type=provider, name=model.name))

    return ApiResponse(data=solvers)


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


@app.post("/move/{solver}/{name}", response_model=ApiResponse[MoveResponse])
async def move(
    data: MoveRequest,
    solver_type: SolverType = Depends(validate_solver_type),
):
    try:
        solver = get_solver(solver_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    board = ConnectFourBoard(initial_state=data.board)

    game = Game(
        board=board,
        solver=solver,
        auto=False,
    )

    try:
        # handle case where cpu starts first
        if data.starting_player == "cpu" and game.board.is_empty():
            best_move = game.get_solver_move(piece=data.solver_piece)
            if best_move is not None:
                game.make_move(move=best_move, piece=data.solver_piece)

        else:
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
