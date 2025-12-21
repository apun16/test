"""
Word Graph for Six Degrees game.

Represents the semantic word network as a graph structure.
"""

from collections import defaultdict
from typing import Dict, Set, List, Optional
from app.models.database import Database


class WordGraph:
    """
    Graph representation of word associations.
    
    Words are nodes, semantic connections are edges.
    Supports efficient BFS pathfinding.
    """
    
    def __init__(self, database: Database):
        """
        Initialize word graph from database.
        
        Args:
            database: Database instance for data access
        """
        self.db = database
        self._adjacency: Dict[str, Set[str]] = defaultdict(set)
        self._words: Set[str] = set()
        self._loaded = False
    
    def load(self) -> None:
        """Load graph from database into memory."""
        if self._loaded:
            return
            
        # Load all words
        words = self.db.execute("SELECT word FROM words")
        self._words = {row["word"].upper() for row in words}
        
        # Load all connections
        connections = self.db.execute("""
            SELECT w1.word as word1, w2.word as word2
            FROM connections c
            JOIN words w1 ON c.word1_id = w1.id
            JOIN words w2 ON c.word2_id = w2.id
        """)
        
        for conn in connections:
            word1 = conn["word1"].upper()
            word2 = conn["word2"].upper()
            self._adjacency[word1].add(word2)
            self._adjacency[word2].add(word1)
        
        self._loaded = True
    
    def has_word(self, word: str) -> bool:
        """
        Check if word exists in graph.
        
        Args:
            word: Word to check
            
        Returns:
            True if word exists
        """
        self.load()
        return word.upper() in self._words
    
    def get_neighbors(self, word: str) -> Set[str]:
        """
        Get all words connected to given word.
        
        Args:
            word: Word to find neighbors for
            
        Returns:
            Set of connected words
        """
        self.load()
        return self._adjacency.get(word.upper(), set())
    
    def are_connected(self, word1: str, word2: str) -> bool:
        """
        Check if two words are directly connected.
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            True if words share an edge
        """
        self.load()
        return word2.upper() in self._adjacency.get(word1.upper(), set())
    
    def get_all_words(self) -> List[str]:
        """
        Get all words in graph.
        
        Returns:
            List of all words
        """
        self.load()
        return list(self._words)
    
    def word_count(self) -> int:
        """
        Get total word count.
        
        Returns:
            Number of words in graph
        """
        self.load()
        return len(self._words)
    
    def connection_count(self) -> int:
        """
        Get total connection count.
        
        Returns:
            Number of edges in graph
        """
        self.load()
        return sum(len(neighbors) for neighbors in self._adjacency.values()) // 2
    
    def add_word(self, word: str, category: Optional[str] = None) -> None:
        """
        Add a word to the graph.
        
        Args:
            word: Word to add
            category: Optional category
        """
        word = word.upper()
        if word not in self._words:
            self.db.insert(
                "INSERT OR IGNORE INTO words (word, category) VALUES (?, ?)",
                (word, category)
            )
            self._words.add(word)
    
    def add_connection(self, word1: str, word2: str, strength: float = 1.0) -> None:
        """
        Add connection between two words.
        
        Args:
            word1: First word
            word2: Second word  
            strength: Connection strength (default 1.0)
        """
        word1 = word1.upper()
        word2 = word2.upper()
        
        # Get word IDs
        w1 = self.db.execute_one("SELECT id FROM words WHERE word = ?", (word1,))
        w2 = self.db.execute_one("SELECT id FROM words WHERE word = ?", (word2,))
        
        if w1 and w2:
            self.db.insert(
                "INSERT OR IGNORE INTO connections (word1_id, word2_id, strength) VALUES (?, ?, ?)",
                (w1["id"], w2["id"], strength)
            )
            self._adjacency[word1].add(word2)
            self._adjacency[word2].add(word1)

