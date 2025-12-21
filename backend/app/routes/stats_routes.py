"""
Statistics API routes for Six Degrees.

Provides game statistics and history.
"""

from flask import Blueprint, jsonify
from app.services.game_engine import GameEngine

stats_bp = Blueprint("stats", __name__)

# Share engine instance
_engine = None


def get_engine() -> GameEngine:
    """Get or create game engine instance."""
    global _engine
    if _engine is None:
        _engine = GameEngine()
    return _engine


@stats_bp.route("/", methods=["GET"])
def get_stats():
    """
    Get overall game statistics.
    
    Returns:
        Statistics dictionary
    """
    engine = get_engine()
    stats = engine.get_statistics()
    return jsonify(stats)


@stats_bp.route("/graph", methods=["GET"])
def get_graph_info():
    """
    Get word graph information.
    
    Returns:
        Graph statistics
    """
    engine = get_engine()
    
    return jsonify({
        "total_words": engine.graph.word_count(),
        "total_connections": engine.graph.connection_count()
    })

