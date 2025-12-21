import { useState, useCallback, useEffect } from 'react'
import Header from './components/Header'
import Game from './components/Game'
import Results from './components/Results'
import HowToPlay from './components/HowToPlay'
import { useGame } from './hooks/useGame'
import { statsAPI } from './services/api'
import styles from './App.module.css'

/**
 * Main application component.
 * Manages game state and view transitions.
 */
function App() {
  const [showHelp, setShowHelp] = useState(false)
  const [totalGames, setTotalGames] = useState(null)
  
  const {
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
  } = useGame()

  // Fetch total games on mount and after each game
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const stats = await statsAPI.getStats()
        setTotalGames(stats.total_games)
      } catch (err) {
        console.error('Failed to fetch stats:', err)
      }
    }
    fetchStats()
  }, [gameState]) // Refetch when game state changes (after submission)

  const handleToggleHelp = useCallback(() => {
    setShowHelp(prev => !prev)
  }, [])

  const handleNewGame = useCallback(() => {
    startNewGame()
    setShowHelp(false)
  }, [startNewGame])

  return (
    <div className={styles.app}>
      <Header onHelpClick={handleToggleHelp} onNewGame={handleNewGame} />
      
      <main className={styles.main}>
        {showHelp ? (
          <HowToPlay onClose={handleToggleHelp} />
        ) : gameState === 'results' && result ? (
          <Results result={result} onPlayAgain={handleNewGame} />
        ) : (
          <Game
            puzzle={puzzle}
            chain={chain}
            error={error}
            isLoading={isLoading}
            hint={hint}
            hintsUsed={hintsUsed}
            onAddWord={addWord}
            onRemoveWord={removeLastWord}
            onSubmit={submitSolution}
            onGetHint={getHint}
            onClearHint={clearHint}
          />
        )}
      </main>
      
      <footer className={styles.footer}>
        <span className={styles.footerText}>
          connect two words in 6 steps or fewer
        </span>
        {totalGames !== null && (
          <span className={styles.gameCount}>
            {totalGames.toLocaleString()} total game{totalGames !== 1 ? 's' : ''} played on this site!!!
          </span>
        )}
      </footer>
    </div>
  )
}

export default App

