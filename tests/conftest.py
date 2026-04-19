"""VibeFlow test configuration and shared fixtures."""
import sys
import os

import pytest

# Ensure project root is on the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def sample_gate_data() -> dict:
    """Provides a sample gate occupancy dataset for testing."""
    return {
        "North Gate": 45,
        "South Gate": 82,
        "East Gate": 60,
        "West Gate": 20,
    }


@pytest.fixture
def sample_food_data() -> dict:
    """Provides a sample concession wait time dataset for testing."""
    return {
        "The Grill": 8,
        "Sushi Bar": 22,
        "Vegan Eats": 14,
    }
