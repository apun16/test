"""
Game Engine for Six Degrees.

Handles game logic, scoring, and puzzle generation.
"""

import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from app.models.database import Database
from app.models.word_graph import WordGraph
from app.services.pathfinder import Pathfinder


@dataclass
class GameResult:
    """Result of a completed game."""
    start_word: str
    end_word: str
    player_path: List[str]
    optimal_path: List[str]
    player_length: int
    optimal_length: int
    score: int
    is_perfect: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass  
class Puzzle:
    """A game puzzle with start and end words."""
    start_word: str
    end_word: str
    optimal_length: int
    difficulty: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class GameEngine:
    """
    Core game engine for Six Degrees.
    
    Manages puzzle generation, validation, and scoring.
    """
    
    # Scoring constants
    SCORE_BEAT_ALGO = 110  # Found a shorter path than the algorithm!
    SCORE_PERFECT = 100    # Matched optimal path
    SCORE_PLUS_ONE = 90    # +1 step
    SCORE_PLUS_TWO = 80    # +2 steps  
    SCORE_PLUS_THREE = 70  # +3 steps
    SCORE_PLUS_FOUR = 60   # +4 steps
    SCORE_COMPLETED = 50   # Completed but longer
    SCORE_FAILED = 0       # Invalid path
    
    # Difficulty settings (optimal path length)
    DIFFICULTY_EASY = (2, 3)
    DIFFICULTY_MEDIUM = (3, 4)
    DIFFICULTY_HARD = (4, 5)
    
    def __init__(self, db_path: str = "data/sixdegrees.db"):
        """
        Initialize game engine.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db = Database(db_path)
        self.graph = WordGraph(self.db)
        self.pathfinder = Pathfinder(self.graph)
    
    def generate_puzzle(self, difficulty: str = "medium") -> Puzzle:
        """
        Generate a new puzzle with appropriate difficulty.
        
        Args:
            difficulty: easy, medium, or hard
            
        Returns:
            Puzzle with start and end words
        """
        # Get difficulty range
        if difficulty == "easy":
            min_len, max_len = self.DIFFICULTY_EASY
        elif difficulty == "hard":
            min_len, max_len = self.DIFFICULTY_HARD
        else:
            min_len, max_len = self.DIFFICULTY_MEDIUM
        
        words = self.graph.get_all_words()
        
        # Try to find a valid puzzle
        max_attempts = 100
        for _ in range(max_attempts):
            start = random.choice(words)
            end = random.choice(words)
            
            if start == end:
                continue
            
            path = self.pathfinder.find_shortest_path(start, end)
            if path and min_len <= len(path) - 1 <= max_len:
                return Puzzle(
                    start_word=start,
                    end_word=end,
                    optimal_length=len(path) - 1,
                    difficulty=difficulty
                )
        
        # Fallback: return any valid puzzle
        for start in words:
            for end in words:
                if start != end:
                    path = self.pathfinder.find_shortest_path(start, end)
                    if path:
                        return Puzzle(
                            start_word=start,
                            end_word=end,
                            optimal_length=len(path) - 1,
                            difficulty="unknown"
                        )
        
        raise ValueError("Could not generate puzzle - check word database")
    
    def validate_word(self, word: str, current_chain: List[str]) -> Dict[str, Any]:
        """
        Validate a word addition to the chain.
        
        Args:
            word: Word to validate
            current_chain: Current chain of words
            
        Returns:
            Validation result with details
        """
        word = word.upper()
        
        # Check chain length first - no point validating if limit reached
        if len(current_chain) >= 6:
            return {
                "valid": False,
                "error": "max_length",
                "message": "Maximum chain length (6) reached"
            }
        
        # Check word exists
        if not self.graph.has_word(word):
            return {
                "valid": False,
                "error": "word_not_found",
                "message": f"'{word}' is not in our word database"
            }
        
        # Check for duplicates
        if word in [w.upper() for w in current_chain]:
            return {
                "valid": False,
                "error": "duplicate_word",
                "message": f"'{word}' has already been used"
            }
        
        # Check connection to last word
        if current_chain:
            last_word = current_chain[-1].upper()
            if not self.graph.are_connected(last_word, word):
                return {
                    "valid": False,
                    "error": "not_connected",
                    "message": f"'{word}' is not connected to '{last_word}'"
                }
        
        return {
            "valid": True,
            "word": word,
            "connections": list(self.graph.get_neighbors(word))[:10]  # Sample connections
        }
    
    def calculate_score(self, player_length: int, optimal_length: int) -> int:
        """
        Calculate score based on path lengths.
        
        If player finds a shorter path than the algorithm, they get bonus points!
        
        Args:
            player_length: Number of steps in player's path
            optimal_length: Number of steps in optimal path
            
        Returns:
            Score value
        """
        if player_length <= 0:
            return self.SCORE_FAILED
        
        difference = player_length - optimal_length
        
        if difference < 0:
            return self.SCORE_BEAT_ALGO  # 110 - beat the algorithm!
        elif difference == 0:
            return self.SCORE_PERFECT  # 100
        elif difference == 1:
            return self.SCORE_PLUS_ONE  # 90
        elif difference == 2:
            return self.SCORE_PLUS_TWO  # 80
        elif difference == 3:
            return self.SCORE_PLUS_THREE  # 70
        elif difference == 4:
            return self.SCORE_PLUS_FOUR  # 60
        else:
            return self.SCORE_COMPLETED  # 50
    
    def submit_solution(
        self, 
        start_word: str, 
        end_word: str, 
        player_path: List[str]
    ) -> GameResult:
        """
        Submit and score a player's solution.
        
        Args:
            start_word: Starting word of puzzle
            end_word: Target word of puzzle
            player_path: Player's submitted chain
            
        Returns:
            GameResult with scoring details
        """
        start_word = start_word.upper()
        end_word = end_word.upper()
        player_path = [w.upper() for w in player_path]
        
        # Validate the full path
        full_path = [start_word] + player_path + [end_word]
        is_valid = self.pathfinder.validate_path(full_path)
        
        # Get optimal path
        optimal_path = self.pathfinder.find_shortest_path(start_word, end_word) or []
        optimal_length = len(optimal_path) - 1 if optimal_path else -1
        
        # Calculate score
        if is_valid:
            player_length = len(full_path) - 1
            score = self.calculate_score(player_length, optimal_length)
        else:
            player_length = -1
            score = self.SCORE_FAILED
        
        result = GameResult(
            start_word=start_word,
            end_word=end_word,
            player_path=player_path,
            optimal_path=optimal_path,
            player_length=player_length,
            optimal_length=optimal_length,
            score=score,
            is_perfect=score == self.SCORE_PERFECT
        )
        
        # Save to history
        self._save_game(result)
        
        return result
    
    def get_hint(
        self, 
        start_word: str, 
        end_word: str, 
        current_chain: List[str],
        hint_level: int = 1
    ) -> Dict[str, Any]:
        """
        Get a hint for the current puzzle state.
        
        Progressive hints reveal more letters each time:
        - Level 1: First letter
        - Level 2: First two letters
        - Level 3+: More letters revealed
        
        Args:
            start_word: Starting word
            end_word: Target word
            current_chain: Current chain (excluding start/end)
            hint_level: How many hints used (1-based), reveals that many letters
            
        Returns:
            Hint information
        """
        # Determine current position
        if current_chain:
            current_word = current_chain[-1].upper()
        else:
            current_word = start_word.upper()
        
        # Find path from current to end
        remaining_path = self.pathfinder.find_shortest_path(current_word, end_word.upper())
        
        if remaining_path and len(remaining_path) > 1:
            next_word = remaining_path[1]
            word_length = len(next_word)
            
            # Calculate how many letters to reveal (progressive)
            letters_to_reveal = min(hint_level, word_length)
            revealed_letters = next_word[:letters_to_reveal]
            
            # Create masked word display (e.g., "WA__" for WAVE with 2 hints)
            hidden_count = word_length - letters_to_reveal
            masked_word = revealed_letters + "_" * hidden_count
            
            # Vary the hint message based on level
            if hint_level == 1:
                hint_msg = f"Try a word connected to '{current_word}'"
            elif hint_level == 2:
                hint_msg = f"The word starts with '{revealed_letters}...'"
            elif letters_to_reveal >= word_length:
                hint_msg = f"The word is '{next_word}'!"
            else:
                hint_msg = f"Getting warmer... '{masked_word}'"
            
            return {
                "type": "next_word",
                "hint": hint_msg,
                "steps_remaining": len(remaining_path) - 1,
                "revealed_letters": revealed_letters,
                "masked_word": masked_word,
                "word_length": word_length,
                "hint_level": hint_level,
                "fully_revealed": letters_to_reveal >= word_length
            }
        
        return {
            "type": "no_path",
            "hint": "Consider backtracking - this path may be a dead end",
            "hint_level": hint_level
        }
    
    def _save_game(self, result: GameResult) -> None:
        """Save game result to database and log it."""
        import logging
        
        self.db.insert(
            """
            INSERT INTO games 
            (start_word, end_word, player_path, optimal_path, 
             player_length, optimal_length, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.start_word,
                result.end_word,
                ",".join(result.player_path),
                ",".join(result.optimal_path),
                result.player_length,
                result.optimal_length,
                result.score
            )
        )
        
        # Log the submission for monitoring
        total = self.get_total_games()
        logging.info(
            f"[GAME #{total}] {result.start_word} → {result.end_word} | "
            f"Score: {result.score} | Path: {result.player_length}/{result.optimal_length} steps | "
            f"Chain: {' → '.join([result.start_word] + result.player_path + [result.end_word])}"
        )
    
    def get_total_games(self) -> int:
        """Get total number of games played."""
        result = self.db.execute_one("SELECT COUNT(*) as count FROM games")
        return result["count"] if result else 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive game statistics.
        
        Returns:
            Dictionary of statistics
        """
        # Get total count
        total_result = self.db.execute_one("SELECT COUNT(*) as count FROM games")
        total_games = total_result["count"] if total_result else 0
        
        if total_games == 0:
            return {
                "total_games": 0,
                "average_score": 0,
                "perfect_games": 0,
                "beat_algorithm_games": 0,
                "completed_games": 0,
                "failed_games": 0,
                "average_path_length": 0,
                "score_distribution": {},
                "recent_games": []
            }
        
        # Get aggregate stats
        agg = self.db.execute_one("""
            SELECT 
                AVG(score) as avg_score,
                AVG(CASE WHEN player_length > 0 THEN player_length END) as avg_length,
                SUM(CASE WHEN score = 110 THEN 1 ELSE 0 END) as beat_algo,
                SUM(CASE WHEN score = 100 THEN 1 ELSE 0 END) as perfect,
                SUM(CASE WHEN score >= 50 AND score < 100 THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN score = 0 THEN 1 ELSE 0 END) as failed
            FROM games
        """)
        
        # Score distribution
        score_dist = self.db.execute("""
            SELECT score, COUNT(*) as count 
            FROM games 
            GROUP BY score 
            ORDER BY score DESC
        """)
        
        # Recent games
        recent = self.db.execute(
            "SELECT * FROM games ORDER BY completed_at DESC LIMIT 10"
        )
        
        return {
            "total_games": total_games,
            "average_score": round(agg["avg_score"] or 0, 1),
            "beat_algorithm_games": agg["beat_algo"] or 0,
            "perfect_games": agg["perfect"] or 0,
            "completed_games": agg["completed"] or 0,
            "failed_games": agg["failed"] or 0,
            "success_rate": round(((total_games - (agg["failed"] or 0)) / total_games * 100), 1) if total_games else 0,
            "average_path_length": round(agg["avg_length"] or 0, 1),
            "score_distribution": {
                str(s["score"]): s["count"] for s in score_dist
            },
            "recent_games": [
                {
                    "id": g["id"],
                    "start": g["start_word"],
                    "end": g["end_word"],
                    "score": g["score"],
                    "player_length": g["player_length"],
                    "optimal_length": g["optimal_length"],
                    "player_path": g["player_path"].split(",") if g["player_path"] else [],
                    "completed_at": g["completed_at"]
                }
                for g in recent
            ]
        }

