"""
Game API routes for Six Degrees.

Handles puzzle generation, validation, and submission.
"""

from flask import Blueprint, jsonify, request
from app.services.game_engine import GameEngine

game_bp = Blueprint("game", __name__)

# Initialize game engine (singleton pattern)
_engine = None


def get_engine() -> GameEngine:
    """Get or create game engine instance."""
    global _engine
    if _engine is None:
        _engine = GameEngine()
    return _engine


@game_bp.route("/new", methods=["GET"])
def new_game():
    """
    Generate a new puzzle.
    
    Query params:
        difficulty: easy, medium, hard (default: medium)
    
    Returns:
        Puzzle with start/end words
    """
    difficulty = request.args.get("difficulty", "medium")
    
    if difficulty not in ["easy", "medium", "hard"]:
        return jsonify({"error": "Invalid difficulty"}), 400
    
    try:
        engine = get_engine()
        puzzle = engine.generate_puzzle(difficulty)
        return jsonify(puzzle.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 500


@game_bp.route("/validate", methods=["POST"])
def validate_word():
    """
    Validate a word addition to the chain.
    
    Body:
        word: Word to validate
        chain: Current chain of words
    
    Returns:
        Validation result
    """
    data = request.get_json()
    
    if not data or "word" not in data:
        return jsonify({"error": "Missing 'word' in request"}), 400
    
    word = data["word"]
    chain = data.get("chain", [])
    
    engine = get_engine()
    result = engine.validate_word(word, chain)
    
    return jsonify(result)


@game_bp.route("/submit", methods=["POST"])
def submit_solution():
    """
    Submit a completed solution.
    
    Body:
        start_word: Puzzle start word
        end_word: Puzzle end word
        path: Player's word chain (excluding start/end)
    
    Returns:
        Game result with score
    """
    data = request.get_json()
    
    required = ["start_word", "end_word", "path"]
    if not data or not all(key in data for key in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400
    
    engine = get_engine()
    result = engine.submit_solution(
        start_word=data["start_word"],
        end_word=data["end_word"],
        player_path=data["path"]
    )
    
    return jsonify(result.to_dict())


@game_bp.route("/hint", methods=["POST"])
def get_hint():
    """
    Get a hint for current puzzle state.
    
    Body:
        start_word: Puzzle start word
        end_word: Puzzle end word
        chain: Current chain (excluding start/end)
        hint_level: Number of hints used (1-based), reveals that many letters
    
    Returns:
        Hint information with progressively revealed letters
    """
    data = request.get_json()
    
    required = ["start_word", "end_word"]
    if not data or not all(key in data for key in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400
    
    engine = get_engine()
    hint = engine.get_hint(
        start_word=data["start_word"],
        end_word=data["end_word"],
        current_chain=data.get("chain", []),
        hint_level=data.get("hint_level", 1)
    )
    
    return jsonify(hint)


@game_bp.route("/check-connection", methods=["POST"])
def check_connection():
    """
    Check if two words are connected.
    
    Body:
        word1: First word
        word2: Second word
    
    Returns:
        Connection status
    """
    data = request.get_json()
    
    if not data or "word1" not in data or "word2" not in data:
        return jsonify({"error": "Missing word1 or word2"}), 400
    
    engine = get_engine()
    connected = engine.graph.are_connected(data["word1"], data["word2"])
    
    return jsonify({
        "word1": data["word1"].upper(),
        "word2": data["word2"].upper(),
        "connected": connected
    })

