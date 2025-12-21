"""
Pytest configuration and shared fixtures.
"""

import pytest
import tempfile
import os
from app import create_app
from app.models.database import Database


@pytest.fixture
def app():
    """Create test application."""
    app = create_app("testing")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    
    db = Database(path)
    db.init_schema()
    
    yield db
    
    # Cleanup
    os.unlink(path)

