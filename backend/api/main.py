import os
from contextlib import asynccontextmanager
from typing import get_args

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.board import ConnectFourBoard
from src.game import Game
from src.heuristic import (
    CountPiecesHeuristic,
    CountPositionsHeuristic,
    HeuristicFactory,
)
from src.model import MistralModelProvider, ModelProviderFactory
from src.types.heuristic_name import HeuristicName
from src.types.model_provider_name import ModelProviderName
from src.types.piece_enum import PieceEnum
from src.types.solver_type import HeuristicSolverType, LLMSolverType, SolverType
from src.utils import get_solver, validate_solver_type

from api.schemas.api_response import ApiResponse
from api.schemas.move_request import MoveRequest
from api.schemas.move_response import MoveResponse


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
            best_move = game.get_solver_move(piece=PieceEnum.CPU)
            if best_move is not None:
                game.make_move(move=best_move, piece=PieceEnum.CPU)

        else:
            # play the player's move first
            game.make_move(move=data.player_move, piece=PieceEnum.HUMAN)

            best_move = None
            if not game.is_over():
                best_move = game.get_solver_move(piece=PieceEnum.CPU)
                if best_move is not None:
                    game.make_move(move=best_move, piece=PieceEnum.CPU)

        return ApiResponse(
            data=MoveResponse(
                state=game.state,
                solver_move=best_move,
                winning_sequence=game.get_winning_sequence(),
            )
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
