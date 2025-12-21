"""
Tests for the Pathfinder service.

Validates BFS algorithm and path validation logic.
"""

import pytest
from unittest.mock import Mock, MagicMock
from app.services.pathfinder import Pathfinder


class TestPathfinder:
    """Test suite for Pathfinder class."""
    
    @pytest.fixture
    def mock_graph(self):
        """Create a mock word graph for testing."""
        graph = Mock()
        
        # Define a simple test graph:
        # A -- B -- C -- D
        #      |
        #      E -- F
        adjacency = {
            "A": {"B"},
            "B": {"A", "C", "E"},
            "C": {"B", "D"},
            "D": {"C"},
            "E": {"B", "F"},
            "F": {"E"},
        }
        
        words = set(adjacency.keys())
        
        graph.has_word = lambda w: w.upper() in words
        graph.get_neighbors = lambda w: adjacency.get(w.upper(), set())
        graph.are_connected = lambda w1, w2: w2.upper() in adjacency.get(w1.upper(), set())
        graph.load = Mock()
        
        return graph
    
    @pytest.fixture
    def pathfinder(self, mock_graph):
        """Create pathfinder with mock graph."""
        return Pathfinder(mock_graph)
    
    def test_find_shortest_path_direct_connection(self, pathfinder):
        """Test finding path between directly connected words."""
        path = pathfinder.find_shortest_path("A", "B")
        assert path == ["A", "B"]
    
    def test_find_shortest_path_two_steps(self, pathfinder):
        """Test finding path with one intermediate word."""
        path = pathfinder.find_shortest_path("A", "C")
        assert path == ["A", "B", "C"]
    
    def test_find_shortest_path_longer(self, pathfinder):
        """Test finding longer paths."""
        path = pathfinder.find_shortest_path("A", "D")
        assert path == ["A", "B", "C", "D"]
        assert len(path) == 4
    
    def test_find_shortest_path_branch(self, pathfinder):
        """Test path through branch."""
        path = pathfinder.find_shortest_path("A", "F")
        assert path == ["A", "B", "E", "F"]
    
    def test_find_shortest_path_same_word(self, pathfinder):
        """Test path from word to itself."""
        path = pathfinder.find_shortest_path("A", "A")
        assert path == ["A"]
    
    def test_find_shortest_path_nonexistent_word(self, pathfinder):
        """Test with word not in graph."""
        path = pathfinder.find_shortest_path("A", "Z")
        assert path is None
    
    def test_validate_path_valid(self, pathfinder):
        """Test validation of a valid path."""
        assert pathfinder.validate_path(["A", "B", "C"]) is True
    
    def test_validate_path_invalid_connection(self, pathfinder):
        """Test validation with missing connection."""
        # A and C are not directly connected
        assert pathfinder.validate_path(["A", "C"]) is False
    
    def test_validate_path_duplicate_words(self, pathfinder):
        """Test validation with duplicate words."""
        assert pathfinder.validate_path(["A", "B", "A"]) is False
    
    def test_validate_path_too_long(self, pathfinder):
        """Test validation with path exceeding max length."""
        # Path with 8 elements (7 steps) should fail
        long_path = ["A", "B", "C", "D", "C", "B", "A", "B"]
        assert pathfinder.validate_path(long_path) is False
    
    def test_validate_path_empty(self, pathfinder):
        """Test validation of empty path."""
        assert pathfinder.validate_path([]) is False
    
    def test_validate_step_valid(self, pathfinder):
        """Test single step validation - valid."""
        assert pathfinder.validate_step("A", "B") is True
    
    def test_validate_step_invalid(self, pathfinder):
        """Test single step validation - invalid."""
        assert pathfinder.validate_step("A", "C") is False
    
    def test_get_path_length(self, pathfinder):
        """Test path length calculation."""
        assert pathfinder.get_path_length("A", "B") == 1
        assert pathfinder.get_path_length("A", "C") == 2
        assert pathfinder.get_path_length("A", "D") == 3
    
    def test_get_path_length_no_path(self, pathfinder):
        """Test path length when no path exists."""
        assert pathfinder.get_path_length("A", "Z") == -1
    
    def test_path_exists_true(self, pathfinder):
        """Test path existence check - exists."""
        assert pathfinder.path_exists("A", "D") is True
    
    def test_path_exists_false(self, pathfinder):
        """Test path existence check - doesn't exist."""
        assert pathfinder.path_exists("A", "Z") is False


class TestPathfinderMaxLength:
    """Test max path length constraints."""
    
    @pytest.fixture
    def long_graph(self):
        """Create a graph with a long chain."""
        graph = Mock()
        
        # Chain: A-B-C-D-E-F-G-H-I-J (10 nodes)
        adjacency = {
            "A": {"B"},
            "B": {"A", "C"},
            "C": {"B", "D"},
            "D": {"C", "E"},
            "E": {"D", "F"},
            "F": {"E", "G"},
            "G": {"F", "H"},
            "H": {"G", "I"},
            "I": {"H", "J"},
            "J": {"I"},
        }
        
        words = set(adjacency.keys())
        
        graph.has_word = lambda w: w.upper() in words
        graph.get_neighbors = lambda w: adjacency.get(w.upper(), set())
        graph.are_connected = lambda w1, w2: w2.upper() in adjacency.get(w1.upper(), set())
        graph.load = Mock()
        
        return graph
    
    def test_respects_max_length(self, long_graph):
        """Test that pathfinder respects max length constraint."""
        pathfinder = Pathfinder(long_graph)
        
        # A to G is 6 steps - should work
        path = pathfinder.find_shortest_path("A", "G", max_length=6)
        assert path is not None
        
        # A to J is 9 steps - should fail with max 6
        path = pathfinder.find_shortest_path("A", "J", max_length=6)
        assert path is None

