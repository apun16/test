import { useState, useCallback, useEffect } from 'react'
import { gameAPI } from '../services/api'

/**
 * Game state management hook.
 * Handles puzzle loading, word validation, and submission.
 */
export function useGame() {
  const [puzzle, setPuzzle] = useState(null)
  const [chain, setChain] = useState([])
  const [gameState, setGameState] = useState('loading') // loading, playing, results
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [hint, setHint] = useState(null)
  const [hintsUsed, setHintsUsed] = useState(0)
  const [currentStepHints, setCurrentStepHints] = useState(0) // Hints for current word position

  /**
   * Load a new puzzle from the API.
   */
  const loadPuzzle = useCallback(async (difficulty = 'medium') => {
    setIsLoading(true)
    setError(null)
    
    try {
      const newPuzzle = await gameAPI.newGame(difficulty)
      setPuzzle(newPuzzle)
      setChain([])
      setResult(null)
      setGameState('playing')
    } catch (err) {
      setError('Failed to load puzzle. Please try again.')
      console.error('Error loading puzzle:', err)
    } finally {
      setIsLoading(false)
    }
  }, [])

  /**
   * Add a word to the chain.
   */
  const addWord = useCallback(async (word) => {
    if (!puzzle || !word.trim()) return false
    
    setIsLoading(true)
    setError(null)
    
    // Build current chain including start word
    const currentChain = chain.length > 0 
      ? chain 
      : [puzzle.start_word]
    
    try {
      const validation = await gameAPI.validateWord(word.trim(), currentChain)
      
      if (validation.valid) {
        setChain(prev => [...prev, validation.word])
        return true
      } else {
        setError(validation.message || 'Invalid word')
        return false
      }
    } catch (err) {
      setError('Failed to validate word. Please try again.')
      console.error('Error validating word:', err)
      return false
    } finally {
      setIsLoading(false)
    }
  }, [puzzle, chain])

  /**
   * Remove the last word from the chain.
   */
  const removeLastWord = useCallback(() => {
    setChain(prev => prev.slice(0, -1))
    setError(null)
  }, [])

  /**
   * Submit the current solution.
   */
  const submitSolution = useCallback(async () => {
    if (!puzzle) return
    
    setIsLoading(true)
    setError(null)
    
    try {
      const gameResult = await gameAPI.submitSolution(
        puzzle.start_word,
        puzzle.end_word,
        chain
      )
      setResult(gameResult)
      setGameState('results')
    } catch (err) {
      setError('Failed to submit solution. Please try again.')
      console.error('Error submitting solution:', err)
    } finally {
      setIsLoading(false)
    }
  }, [puzzle, chain])

  /**
   * Start a new game.
   */
  const startNewGame = useCallback((difficulty = 'medium') => {
    loadPuzzle(difficulty)
    setHint(null)
    setHintsUsed(0)
    setCurrentStepHints(0)
  }, [loadPuzzle])

  /**
   * Get a hint for the current puzzle.
   * Each call reveals one more letter (progressive hints).
   */
  const getHint = useCallback(async () => {
    if (!puzzle) return
    
    setIsLoading(true)
    
    // Next hint level is current + 1
    const nextHintLevel = currentStepHints + 1
    
    try {
      const hintData = await gameAPI.getHint(
        puzzle.start_word,
        puzzle.end_word,
        chain,
        nextHintLevel
      )
      setHint(hintData)
      setHintsUsed(prev => prev + 1)
      setCurrentStepHints(nextHintLevel)
    } catch (err) {
      setError('Failed to get hint.')
      console.error('Error getting hint:', err)
    } finally {
      setIsLoading(false)
    }
  }, [puzzle, chain, currentStepHints])

  /**
   * Clear the current hint.
   */
  const clearHint = useCallback(() => {
    setHint(null)
  }, [])

  // Load initial puzzle on mount
  useEffect(() => {
    loadPuzzle()
  }, [loadPuzzle])

  // Reset hint state when chain changes (new word added/removed)
  useEffect(() => {
    setHint(null)
    setCurrentStepHints(0) // Reset progressive hints for new position
  }, [chain.length])

  return {
    puzzle,
    chain,
    gameState,
    result,
    error,
    isLoading,
    hint,
    hintsUsed,
    addWord,
    removeLastWord,
    submitSolution,
    startNewGame,
    getHint,
    clearHint,
  }
}

