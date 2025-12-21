import { useState } from 'react'
import styles from './Results.module.css'

/**
 * Game results display.
 * Shows score, comparison with optimal path, and share option.
 */
function Results({ result, onPlayAgain }) {
  const [copied, setCopied] = useState(false)
  
  const {
    start_word,
    end_word,
    player_path,
    optimal_path,
    player_length,
    optimal_length,
    score,
  } = result

  const isValid = player_length > 0 && score > 0
  const beatAlgorithm = isValid && player_length < optimal_length

  const getScoreLabel = () => {
    if (!isValid) return 'PATH NOT CONNECTED'
    if (score >= 110) return 'YOU BEAT THE ALGORITHM!'
    if (score === 100) return 'PERFECT'
    if (score >= 90) return 'EXCELLENT'
    if (score >= 80) return 'GREAT'
    if (score >= 70) return 'GOOD'
    if (score >= 60) return 'NICE'
    if (score >= 50) return 'COMPLETED'
    return 'TRY AGAIN'
  }

  const getScoreEmoji = () => {
    if (!isValid) return '🔗'
    if (score >= 110) return '🤖💥'
    if (score === 100) return '🎯'
    if (score >= 90) return '⭐'
    if (score >= 80) return '✓'
    if (score >= 70) return '✓'
    if (score >= 60) return '✓'
    if (score >= 50) return '🔗'
    return '🔗'
  }

  const getScoreColor = () => {
    if (!isValid) return 'var(--text-muted)'
    if (score >= 110) return '#ff6b6b'
    if (score >= 90) return 'var(--success)'
    if (score >= 70) return 'var(--accent)'
    if (score >= 50) return 'var(--text-primary)'
    return 'var(--text-muted)'
  }

  const handleShare = async () => {
    const shareText = generateShareText()
    
    if (navigator.share) {
      try {
        await navigator.share({ text: shareText })
        return
      } catch (err) {
        // Fall through to clipboard
      }
    }
    
    try {
      await navigator.clipboard.writeText(shareText)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      const textArea = document.createElement('textarea')
      textArea.value = shareText
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand('copy')
      document.body.removeChild(textArea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const generateShareText = () => {
    // Create visual chain representation
    const maxSteps = 6
    const chainVisual = []
    
    // Build the visual grid
    for (let i = 0; i < maxSteps; i++) {
      if (i < player_length) {
        if (!isValid) {
          chainVisual.push('🟥') // Red for broken path
        } else if (beatAlgorithm) {
          chainVisual.push('🟪') // Purple for beating algorithm
        } else if (player_length === optimal_length) {
          chainVisual.push('🟩') // Green for perfect
        } else if (i < optimal_length) {
          chainVisual.push('🟨') // Yellow for optimal range
        } else {
          chainVisual.push('🟧') // Orange for extra steps
        }
      } else {
        chainVisual.push('⬜') // Empty for unused
      }
    }
    
    // Status line with emoji
    let statusLine = ''
    if (!isValid) {
      statusLine = '❌ Broken chain'
    } else if (beatAlgorithm) {
      statusLine = `🤖💥 Beat the algorithm!`
    } else if (player_length === optimal_length) {
      statusLine = '🎯 Perfect!'
    } else {
      statusLine = `📊 ${player_length}/${optimal_length} steps`
    }
    
    // Build the share text with visual flair
    return `┌─────────────────┐
│  6°  DEGREES    │
└─────────────────┘

${start_word} → ${end_word}

${chainVisual.join('')}

${statusLine}
⭐ Score: ${score}/110

🔗 test-pearl-five-18.vercel.app`
  }

  const getMessage = () => {
    if (!isValid) {
      return "Your chain didn't connect the words. One or more words weren't linked."
    }
    if (beatAlgorithm) {
      const diff = optimal_length - player_length
      return `You found a path ${diff} step${diff > 1 ? 's' : ''} shorter than the algorithm!`
    }
    if (player_length === optimal_length) {
      return "You matched the optimal path."
    }
    const diff = player_length - optimal_length
    return `${diff} step${diff > 1 ? 's' : ''} longer than optimal.`
  }

  return (
    <div className={styles.results}>
      {/* Score display */}
      <div className={styles.scoreSection}>
        <div className={styles.scoreEmoji}>{getScoreEmoji()}</div>
        <div 
          className={styles.score}
          style={{ color: getScoreColor() }}
        >
          {score}
        </div>
        <div className={styles.scoreLabel}>{getScoreLabel()}</div>
      </div>

      {/* Puzzle summary */}
      <div className={styles.puzzle}>
        <span className={styles.word}>{start_word}</span>
        <span className={styles.arrow}>→</span>
        <span className={styles.word}>{end_word}</span>
      </div>

      {/* Status message */}
      <p className={styles.message}>{getMessage()}</p>

      {/* Path comparison */}
      <div className={styles.comparison}>
        <div className={`${styles.pathSection} ${!isValid ? styles.invalidPath : ''}`}>
          <h3 className={styles.pathTitle}>your path {!isValid && '(broken)'}</h3>
          <div className={styles.path}>
            <span className={styles.pathWord}>{start_word}</span>
            {player_path.map((word, i) => (
              <span key={i} className={styles.pathWord}>{word}</span>
            ))}
            <span className={styles.pathWord}>{end_word}</span>
          </div>
          <div className={styles.pathLength}>
            {player_path.length + 1} step{player_path.length !== 0 ? 's' : ''}
          </div>
        </div>

        <div className={styles.pathSection}>
          <h3 className={styles.pathTitle}>working path</h3>
          <div className={`${styles.path} ${styles.optimalPath}`}>
            {optimal_path.map((word, i) => (
              <span key={i} className={styles.pathWord}>{word}</span>
            ))}
          </div>
          <div className={styles.pathLength}>
            {optimal_length} step{optimal_length !== 1 ? 's' : ''}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className={styles.actions}>
        <button 
          className={`btn ${styles.shareBtn} ${copied ? styles.copied : ''}`} 
          onClick={handleShare}
        >
          {copied ? '✓ copied!' : '📋 share'}
        </button>
        <button className="btn btn--primary" onClick={onPlayAgain}>
          play again
        </button>
      </div>
    </div>
  )
}

export default Results
