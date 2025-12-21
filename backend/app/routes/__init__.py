"""API route blueprints for Six Degrees."""

from app.routes.game_routes import game_bp
from app.routes.stats_routes import stats_bp

__all__ = ["game_bp", "stats_bp"]

