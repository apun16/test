"""
Six Degrees - Flask Application Factory

A word association game where players connect two words in minimal steps.
"""

import logging
from flask import Flask
from flask_cors import CORS


def create_app(config_name: str = "development") -> Flask:
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_name: Configuration environment (development/testing/production)
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configuration
    app.config.update(
        SECRET_KEY="dev-secret-key-change-in-production",
        DATABASE="data/sixdegrees.db",
        TESTING=config_name == "testing",
    )
    
    # Enable CORS for frontend (allow all localhost ports in development)
    # In production, update this to your actual domain
    CORS(app, origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:3000", 
        "http://127.0.0.1:5173", 
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        # Add your production domain here when deploying
        # "https://yourdomain.com",
    ])
    
    # Register blueprints
    from app.routes.game_routes import game_bp
    from app.routes.stats_routes import stats_bp
    
    app.register_blueprint(game_bp, url_prefix="/api/game")
    app.register_blueprint(stats_bp, url_prefix="/api/stats")
    
    # Health check endpoint
    @app.route("/api/health")
    def health_check():
        from app.services.game_engine import GameEngine
        engine = GameEngine()
        total_games = engine.get_total_games()
        return {
            "status": "healthy", 
            "game": "Six Degrees",
            "total_games_played": total_games
        }
    
    return app

