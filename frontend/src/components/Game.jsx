import { useState, useCallback } from 'react'
import WordChain from './WordChain'
import WordInput from './WordInput'
import styles from './Game.module.css'

/**
 * Main game component.
 * Displays puzzle, word chain, and input controls.
 */
function Game({ 
  puzzle, 
  chain, 
  error, 
  isLoading,
  hint,
  hintsUsed,
  onAddWord, 
  onRemoveWord, 
  onSubmit,
  onGetHint,
  onClearHint,
}) {
  const [inputValue, setInputValue] = useState('')

  const handleSubmitWord = useCallback(async (e) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return
    
    const success = await onAddWord(inputValue)
    if (success) {
      setInputValue('')
    }
  }, [inputValue, isLoading, onAddWord])

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Backspace' && inputValue === '' && chain.length > 0) {
      onRemoveWord()
    }
  }, [inputValue, chain.length, onRemoveWord])

  // Show loading state
  if (!puzzle) {
    return (
      <div className={styles.loading}>
        <span className={styles.loadingText}>loading puzzle</span>
        <span className={styles.loadingDots}>...</span>
      </div>
    )
  }

  const canSubmit = chain.length > 0
  const stepsUsed = chain.length
  const stepsRemaining = 6 - stepsUsed

  return (
    <div className={styles.game}>
      {/* Puzzle display */}
      <div className={styles.puzzle}>
        <div className={styles.wordContainer}>
          <span className={styles.label}>from</span>
          <span className={styles.word}>{puzzle.start_word}</span>
        </div>
        
        <div className={styles.arrow}>→</div>
        
        <div className={styles.wordContainer}>
          <span className={styles.label}>to</span>
          <span className={styles.word}>{puzzle.end_word}</span>
        </div>
      </div>

      {/* Hint about optimal path */}
      <p className={styles.hint}>
        shortest path: <strong>{puzzle.optimal_length}</strong> steps
      </p>

      {/* Word chain visualization */}
      <WordChain 
        startWord={puzzle.start_word}
        endWord={puzzle.end_word}
        chain={chain}
        onRemoveWord={onRemoveWord}
      />

      {/* Input area */}
      <div className={styles.inputArea}>
        <form onSubmit={handleSubmitWord} className={styles.form}>
          <WordInput
            value={inputValue}
            onChange={setInputValue}
            onKeyDown={handleKeyDown}
            placeholder={chain.length === 0 ? 'type your first word...' : 'add next word...'}
            disabled={isLoading || stepsRemaining <= 0}
            error={error}
          />
          
          <button 
            type="submit" 
            className={`btn ${styles.addBtn}`}
            disabled={isLoading || !inputValue.trim()}
          >
            add
          </button>
        </form>

        {error && (
          <p className={styles.error}>{error}</p>
        )}

        {/* Steps counter */}
        <div className={styles.steps}>
          <span className={stepsRemaining <= 1 ? styles.stepsWarning : ''}>
            {stepsRemaining} step{stepsRemaining !== 1 ? 's' : ''} remaining
          </span>
        </div>
      </div>

      {/* Hint section */}
      {hint && (
        <div className={styles.hintBox}>
          <div className={styles.hintHeader}>
            <span className={styles.hintIcon}>💡</span>
            <span className={styles.hintTitle}>hint #{hint.hint_level || 1}</span>
            <button 
              className={styles.hintClose} 
              onClick={onClearHint}
              aria-label="Close hint"
            >
              ×
            </button>
          </div>
          <p className={styles.hintText}>{hint.hint}</p>
          
          {/* Progressive letter reveal */}
          {hint.masked_word && (
            <div className={styles.maskedWord}>
              {hint.masked_word.split('').map((char, i) => (
                <span 
                  key={i} 
                  className={char === '_' ? styles.hiddenLetter : styles.revealedLetter}
                >
                  {char}
                </span>
              ))}
            </div>
          )}
          
          {hint.word_length && !hint.fully_revealed && (
            <p className={styles.hintMeta}>
              {hint.word_length} letters • click hint again to reveal more
            </p>
          )}
          
          {hint.fully_revealed && (
            <p className={styles.hintRevealed}>
              ✓ Word fully revealed!
            </p>
          )}
          
          {hint.steps_remaining && (
            <p className={styles.hintSteps}>
              {hint.steps_remaining} step{hint.steps_remaining !== 1 ? 's' : ''} to reach target
            </p>
          )}
        </div>
      )}

      {/* Action buttons */}
      <div className={styles.actions}>
        <button
          className={`btn ${styles.hintBtn}`}
          onClick={onGetHint}
          disabled={isLoading || (hint && hint.fully_revealed)}
        >
          💡 {hint ? 'more' : 'hint'} {hintsUsed > 0 && `(${hintsUsed})`}
        </button>
        
        <button
          className={`btn btn--primary ${styles.submitBtn}`}
          onClick={onSubmit}
          disabled={!canSubmit || isLoading}
        >
          submit chain
        </button>
      </div>
    </div>
  )
}

export default Game

