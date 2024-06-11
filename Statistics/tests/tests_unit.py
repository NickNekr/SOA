import pytest
from fastapi.testclient import TestClient

from api.routes import app 
from src.tools.repo_alchemy_linker import get_mono_repos, MonoRepos
from database.model import Views, Likes, LikesStats, ViewsStats

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mono_repo() -> MonoRepos:
    return get_mono_repos()

def test_health_check(client):
    response = client.get("/statistics/health")
    assert response.status_code == 200

def test_get_state_by_entity(mono_repo):
    repo, stats_repo, stats_entity = mono_repo.get_state(Views)
    assert repo is mono_repo.views
    assert stats_repo is mono_repo.views_stats
    assert stats_entity is ViewsStats

    repo, stats_repo, stats_entity = mono_repo.get_state(Likes)
    assert repo is mono_repo.likes
    assert stats_repo is mono_repo.likes_stats
    assert stats_entity is LikesStats