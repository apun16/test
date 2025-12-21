"""
Database connection and management for Six Degrees.

Handles SQLite connections and provides a clean interface for data operations.
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class Database:
    """
    SQLite database manager with context management support.
    
    Provides connection pooling and clean query interfaces.
    """
    
    def __init__(self, db_path: str = "data/sixdegrees.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            SQLite connection with row factory
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a query and return results as dictionaries.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """
        Execute a query and return single result.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Single result dictionary or None
        """
        results = self.execute(query, params)
        return results[0] if results else None
    
    def insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute an insert and return the last row id.
        
        Args:
            query: SQL insert statement
            params: Insert parameters
            
        Returns:
            ID of inserted row
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid
    
    def init_schema(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            conn.executescript("""
                -- Words table
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE NOT NULL,
                    category TEXT
                );
                
                -- Word connections (edges in graph)
                CREATE TABLE IF NOT EXISTS connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word1_id INTEGER NOT NULL,
                    word2_id INTEGER NOT NULL,
                    strength REAL DEFAULT 1.0,
                    FOREIGN KEY (word1_id) REFERENCES words(id),
                    FOREIGN KEY (word2_id) REFERENCES words(id),
                    UNIQUE(word1_id, word2_id)
                );
                
                -- Game history
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_word TEXT NOT NULL,
                    end_word TEXT NOT NULL,
                    player_path TEXT,
                    optimal_path TEXT,
                    player_length INTEGER,
                    optimal_length INTEGER,
                    score INTEGER,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Create indexes for performance
                CREATE INDEX IF NOT EXISTS idx_words_word ON words(word);
                CREATE INDEX IF NOT EXISTS idx_conn_word1 ON connections(word1_id);
                CREATE INDEX IF NOT EXISTS idx_conn_word2 ON connections(word2_id);
            """)

