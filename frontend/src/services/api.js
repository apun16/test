/**
 * API service for Six Degrees game.
 * Handles all communication with the Flask backend.
 */

const API_BASE = '/api'

/**
 * Generic fetch wrapper with error handling.
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise<object>} Response data
 */
async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  }

  const response = await fetch(url, config)
  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || 'API request failed')
  }

  return data
}

/**
 * Game API methods.
 */
export const gameAPI = {
  /**
   * Start a new game with a random puzzle.
   * @param {string} difficulty - easy, medium, or hard
   * @returns {Promise<{start_word: string, end_word: string, optimal_length: number}>}
   */
  async newGame(difficulty = 'medium') {
    return fetchAPI(`/game/new?difficulty=${difficulty}`)
  },

  /**
   * Validate a word addition to the chain.
   * @param {string} word - Word to validate
   * @param {string[]} chain - Current chain of words
   * @returns {Promise<{valid: boolean, error?: string, message?: string}>}
   */
  async validateWord(word, chain) {
    return fetchAPI('/game/validate', {
      method: 'POST',
      body: JSON.stringify({ word, chain }),
    })
  },

  /**
   * Submit the final solution.
   * @param {string} startWord - Puzzle start word
   * @param {string} endWord - Puzzle end word
   * @param {string[]} path - Player's word chain
   * @returns {Promise<GameResult>}
   */
  async submitSolution(startWord, endWord, path) {
    return fetchAPI('/game/submit', {
      method: 'POST',
      body: JSON.stringify({
        start_word: startWord,
        end_word: endWord,
        path,
      }),
    })
  },

  /**
   * Get a hint for the current puzzle state.
   * Progressive hints reveal more letters each time.
   * @param {string} startWord - Puzzle start word
   * @param {string} endWord - Puzzle end word
   * @param {string[]} chain - Current chain
   * @param {number} hintLevel - How many hints used (reveals that many letters)
   * @returns {Promise<{type: string, hint: string, masked_word: string}>}
   */
  async getHint(startWord, endWord, chain, hintLevel = 1) {
    return fetchAPI('/game/hint', {
      method: 'POST',
      body: JSON.stringify({
        start_word: startWord,
        end_word: endWord,
        chain,
        hint_level: hintLevel,
      }),
    })
  },
}

/**
 * Stats API methods.
 */
export const statsAPI = {
  /**
   * Get overall game statistics.
   * @returns {Promise<object>}
   */
  async getStats() {
    return fetchAPI('/stats/')
  },

  /**
   * Get word graph info.
   * @returns {Promise<{total_words: number, total_connections: number}>}
   */
  async getGraphInfo() {
    return fetchAPI('/stats/graph')
  },
}

