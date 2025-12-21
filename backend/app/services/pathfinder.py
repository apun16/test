"""
Pathfinder service using BFS algorithm.

Finds shortest paths between words in the word graph.
"""

from collections import deque
from typing import List, Optional, Set
from app.models.word_graph import WordGraph


class Pathfinder:
    """
    BFS-based pathfinding for word associations.
    
    Finds optimal paths between any two words in the graph.
    """
    
    MAX_PATH_LENGTH = 6
    
    def __init__(self, graph: WordGraph):
        """
        Initialize pathfinder with word graph.
        
        Args:
            graph: WordGraph instance for traversal
        """
        self.graph = graph
    
    def find_shortest_path(
        self, 
        start: str, 
        end: str, 
        max_length: int = MAX_PATH_LENGTH
    ) -> Optional[List[str]]:
        """
        Find shortest path between two words using BFS.
        
        Args:
            start: Starting word
            end: Target word
            max_length: Maximum path length allowed
            
        Returns:
            List of words forming path, or None if no path exists
        """
        start = start.upper()
        end = end.upper()
        
        # Validate words exist
        if not self.graph.has_word(start) or not self.graph.has_word(end):
            return None
        
        # Same word edge case
        if start == end:
            return [start]
        
        # BFS with path tracking
        queue: deque = deque([(start, [start])])
        visited: Set[str] = {start}
        
        while queue:
            current, path = queue.popleft()
            
            # Check path length constraint
            if len(path) > max_length:
                continue
            
            # Explore neighbors
            for neighbor in self.graph.get_neighbors(current):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def validate_path(self, path: List[str]) -> bool:
        """
        Validate that a path is valid in the graph.
        
        A valid path:
        - Contains only words in the graph
        - Each consecutive pair is connected
        - No repeated words
        - Maximum 6 words
        
        Args:
            path: List of words to validate
            
        Returns:
            True if path is valid
        """
        if not path or len(path) > self.MAX_PATH_LENGTH + 1:
            return False
        
        # Check for duplicates
        if len(path) != len(set(word.upper() for word in path)):
            return False
        
        # Check each word exists
        for word in path:
            if not self.graph.has_word(word):
                return False
        
        # Check consecutive connections
        for i in range(len(path) - 1):
            if not self.graph.are_connected(path[i], path[i + 1]):
                return False
        
        return True
    
    def validate_step(self, from_word: str, to_word: str) -> bool:
        """
        Validate a single step in a path.
        
        Args:
            from_word: Current word
            to_word: Next word
            
        Returns:
            True if step is valid
        """
        return (
            self.graph.has_word(to_word) and 
            self.graph.are_connected(from_word, to_word)
        )
    
    def get_path_length(self, start: str, end: str) -> int:
        """
        Get the length of shortest path (number of edges).
        
        Args:
            start: Starting word
            end: Target word
            
        Returns:
            Path length or -1 if no path exists
        """
        path = self.find_shortest_path(start, end)
        return len(path) - 1 if path else -1
    
    def path_exists(self, start: str, end: str) -> bool:
        """
        Check if any path exists between words.
        
        Args:
            start: Starting word
            end: Target word
            
        Returns:
            True if path exists
        """
        return self.find_shortest_path(start, end) is not None

