import sys
from copy import deepcopy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import src.app as app_module  # noqa: E402

@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy(app_module.activities)
    yield
    app_module.activities = deepcopy(original_activities)

@pytest.fixture
def client():
    return TestClient(app_module.app)
