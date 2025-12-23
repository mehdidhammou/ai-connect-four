import pytest
from api.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_get_solvers_returns_api_response(client: TestClient):
    """Test that /solvers endpoint returns ApiResponse with correct structure"""
    response = client.get("/solvers")
    assert response.status_code == 200
    assert "data" in response.json()


def test_get_solvers_includes_heuristic_solvers(client: TestClient):
    """Test that /solvers endpoint includes heuristic solvers"""
    response = client.get("/solvers")
    data = response.json()["data"]

    heuristic_solvers = [s for s in data if s.get("type") == "heuristic"]
    assert len(heuristic_solvers) > 0


def test_get_solvers_heuristic_solver_structure(client: TestClient):
    """Test that heuristic solvers have correct structure"""
    response = client.get("/solvers")
    data = response.json()["data"]

    heuristic_solvers = [s for s in data if s.get("type") == "heuristic"]
    for solver in heuristic_solvers:
        assert "type" in solver
        assert "name" in solver
        assert solver["type"] == "heuristic"


def test_get_solvers_includes_llm_solvers(client: TestClient):
    """Test that /solvers endpoint includes LLM solvers"""
    response = client.get("/solvers")
    data = response.json()["data"]

    llm_solvers = [s for s in data if s.get("type") != "heuristic"]
    assert len(llm_solvers) > 0


def test_get_solvers_llm_solver_structure(client: TestClient):
    """Test that LLM solvers have correct structure with provider type"""
    response = client.get("/solvers")
    data = response.json()["data"]

    llm_solvers = [s for s in data if s.get("type") != "heuristic"]
    for solver in llm_solvers:
        assert "type" in solver
        assert "name" in solver
        assert solver["type"] in ["mistral"]  # Add other providers as needed


def test_get_solvers_returns_list(client: TestClient):
    """Test that /solvers endpoint returns a list"""
    response = client.get("/solvers")
    data = response.json()["data"]
    assert isinstance(data, list)
