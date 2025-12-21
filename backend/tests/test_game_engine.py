"""
Tests for the Game Engine.

Validates puzzle generation, scoring, and game logic.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.game_engine import GameEngine, GameResult, Puzzle


class TestScoring:
    """Test scoring logic."""
    
    @pytest.fixture
    def engine(self):
        """Create game engine with mocked dependencies."""
        with patch('app.services.game_engine.Database'), \
             patch('app.services.game_engine.WordGraph'), \
             patch('app.services.game_engine.Pathfinder'):
            return GameEngine()
    
    def test_score_beat_algorithm(self, engine):
        """Test bonus score for beating the algorithm."""
        score = engine.calculate_score(player_length=2, optimal_length=4)
        assert score == 110
    
    def test_score_perfect(self, engine):
        """Test perfect score calculation."""
        score = engine.calculate_score(player_length=3, optimal_length=3)
        assert score == 100
    
    def test_score_plus_one(self, engine):
        """Test +1 extra word score."""
        score = engine.calculate_score(player_length=4, optimal_length=3)
        assert score == 90
    
    def test_score_plus_two(self, engine):
        """Test +2 extra words score."""
        score = engine.calculate_score(player_length=5, optimal_length=3)
        assert score == 80
    
    def test_score_plus_three(self, engine):
        """Test +3 extra words score."""
        score = engine.calculate_score(player_length=6, optimal_length=3)
        assert score == 70
    
    def test_score_plus_four(self, engine):
        """Test +4 extra words score."""
        score = engine.calculate_score(player_length=7, optimal_length=3)
        assert score == 60
    
    def test_score_completed_longer(self, engine):
        """Test score for longer but valid path."""
        score = engine.calculate_score(player_length=8, optimal_length=3)
        assert score == 50
    
    def test_score_failed(self, engine):
        """Test score for failed attempt."""
        score = engine.calculate_score(player_length=0, optimal_length=3)
        assert score == 0
        
        score = engine.calculate_score(player_length=-1, optimal_length=3)
        assert score == 0


class TestGameResult:
    """Test GameResult dataclass."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = GameResult(
            start_word="OCEAN",
            end_word="KEYBOARD",
            player_path=["WAVE", "SOUND"],
            optimal_path=["WAVE", "SOUND"],
            player_length=3,
            optimal_length=3,
            score=100,
            is_perfect=True
        )
        
        d = result.to_dict()
        
        assert d["start_word"] == "OCEAN"
        assert d["end_word"] == "KEYBOARD"
        assert d["score"] == 100
        assert d["is_perfect"] is True


class TestPuzzle:
    """Test Puzzle dataclass."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        puzzle = Puzzle(
            start_word="CAT",
            end_word="DOG",
            optimal_length=4,
            difficulty="medium"
        )
        
        d = puzzle.to_dict()
        
        assert d["start_word"] == "CAT"
        assert d["end_word"] == "DOG"
        assert d["optimal_length"] == 4
        assert d["difficulty"] == "medium"


class TestWordValidation:
    """Test word validation logic."""
    
    @pytest.fixture
    def engine_with_graph(self):
        """Create engine with mock graph."""
        with patch('app.services.game_engine.Database'), \
             patch('app.services.game_engine.WordGraph') as MockGraph, \
             patch('app.services.game_engine.Pathfinder'):
            
            engine = GameEngine()
            
            # Configure mock graph
            valid_words = {"OCEAN", "WAVE", "WATER", "FISH"}
            connections = {
                "OCEAN": {"WAVE", "FISH"},
                "WAVE": {"OCEAN", "WATER"},
                "WATER": {"WAVE"},
                "FISH": {"OCEAN"},
            }
            
            engine.graph.has_word = lambda w: w.upper() in valid_words
            engine.graph.are_connected = lambda w1, w2: w2.upper() in connections.get(w1.upper(), set())
            engine.graph.get_neighbors = lambda w: connections.get(w.upper(), set())
            
            return engine
    
    def test_validate_word_success(self, engine_with_graph):
        """Test successful word validation."""
        result = engine_with_graph.validate_word("WAVE", ["OCEAN"])
        
        assert result["valid"] is True
        assert result["word"] == "WAVE"
    
    def test_validate_word_not_found(self, engine_with_graph):
        """Test validation with unknown word."""
        result = engine_with_graph.validate_word("UNKNOWN", ["OCEAN"])
        
        assert result["valid"] is False
        assert result["error"] == "word_not_found"
    
    def test_validate_word_duplicate(self, engine_with_graph):
        """Test validation with duplicate word."""
        result = engine_with_graph.validate_word("OCEAN", ["WAVE", "OCEAN"])
        
        assert result["valid"] is False
        assert result["error"] == "duplicate_word"
    
    def test_validate_word_not_connected(self, engine_with_graph):
        """Test validation with unconnected word."""
        result = engine_with_graph.validate_word("FISH", ["WAVE"])  # FISH not connected to WAVE
        
        assert result["valid"] is False
        assert result["error"] == "not_connected"
    
    def test_validate_word_max_length(self, engine_with_graph):
        """Test validation when max length reached."""
        chain = ["W1", "W2", "W3", "W4", "W5", "W6"]  # 6 words = max reached
        result = engine_with_graph.validate_word("WAVE", chain)
        
        assert result["valid"] is False
        assert result["error"] == "max_length"


class TestHints:
    """Test hint generation."""
    
    @pytest.fixture
    def engine_with_pathfinder(self):
        """Create engine with mock pathfinder."""
        with patch('app.services.game_engine.Database'), \
             patch('app.services.game_engine.WordGraph'), \
             patch('app.services.game_engine.Pathfinder') as MockPathfinder:
            
            engine = GameEngine()
            
            # Configure mock pathfinder
            engine.pathfinder.find_shortest_path = Mock(
                return_value=["WAVE", "WATER", "RAIN", "CLOUD"]
            )
            
            return engine
    
    def test_hint_provides_next_step(self, engine_with_pathfinder):
        """Test that hints provide useful next step info."""
        hint = engine_with_pathfinder.get_hint(
            start_word="OCEAN",
            end_word="CLOUD",
            current_chain=["WAVE"]
        )
        
        assert hint["type"] == "next_word"
        assert "steps_remaining" in hint
        assert "revealed_letters" in hint  # Progressive hints reveal letters
        assert "masked_word" in hint
        assert hint["hint_level"] == 1

