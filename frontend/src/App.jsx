import { useState, useCallback, useEffect } from 'react'
import { Analytics } from '@vercel/analytics/react'
import Landing from './components/Landing'
import Header from './components/Header'
import Game from './components/Game'
import Results from './components/Results'
import HowToPlay from './components/HowToPlay'
import { useGame } from './hooks/useGame'
import { getTotalGames } from './services/supabase'
import styles from './App.module.css'

/**
 * Main application component.
 * Manages game state and view transitions.
 */
function App() {
  const [showLanding, setShowLanding] = useState(true)
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

  // Fetch total games from Supabase on mount and after each game
  useEffect(() => {
    const fetchStats = async () => {
      const count = await getTotalGames()
      if (count !== null) {
        setTotalGames(count)
      }
    }
    fetchStats()
  }, [gameState]) // Refetch when game state changes (after submission)

  const handlePlay = useCallback(() => {
    setShowLanding(false)
    startNewGame()
  }, [startNewGame])

  const handleToggleHelp = useCallback(() => {
    setShowHelp(prev => !prev)
  }, [])

  const handleNewGame = useCallback(() => {
    startNewGame()
    setShowHelp(false)
  }, [startNewGame])

  // Show landing page
  if (showLanding) {
    return (
      <>
        <Landing onPlay={handlePlay} />
        <Analytics />
      </>
    )
  }

  return (
    <>
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
              {totalGames.toLocaleString()} game{totalGames !== 1 ? 's' : ''} played
            </span>
          )}
          <div className={styles.footerMeta}>
            <span className={styles.copyright}>© 2025</span>
            <a 
              href="https://github.com/apun16/test" 
              target="_blank" 
              rel="noopener noreferrer"
              className={styles.githubLink}
              aria-label="View source on GitHub"
            >
              <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
              </svg>
            </a>
          </div>
        </footer>
      </div>
      <Analytics />
    </>
  )
}

export default App

