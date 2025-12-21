import { useState, useRef } from 'react'
import html2canvas from 'html2canvas'
import styles from './Results.module.css'

/**
 * Game results display.
 * Shows score, comparison with optimal path, and share option.
 */
function Results({ result, onPlayAgain }) {
  const [copied, setCopied] = useState(false)
  const [sharing, setSharing] = useState(false)
  const shareCardRef = useRef(null)
  
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
    setSharing(true)
    
    try {
      // Generate image from the share card
      if (shareCardRef.current) {
        const canvas = await html2canvas(shareCardRef.current, {
          backgroundColor: '#1a1814',
          scale: 2,
        })
        
        // Convert to blob
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'))
        
        // Try native share with image
        if (navigator.share && navigator.canShare) {
          const file = new File([blob], '6degrees-result.png', { type: 'image/png' })
          const shareData = { 
            files: [file],
            text: generateShareText()
          }
          
          if (navigator.canShare(shareData)) {
            await navigator.share(shareData)
            setSharing(false)
            return
          }
        }
        
        // Fallback: copy text to clipboard
        await navigator.clipboard.writeText(generateShareText())
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      }
    } catch (err) {
      // Final fallback
      try {
        await navigator.clipboard.writeText(generateShareText())
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      } catch {
        console.error('Share failed:', err)
      }
    }
    
    setSharing(false)
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

  // Generate visual chain squares
  const getChainSquares = () => {
    const maxSteps = 6
    const squares = []
    
    for (let i = 0; i < maxSteps; i++) {
      let colorClass = styles.squareEmpty
      if (i < player_length) {
        if (!isValid) {
          colorClass = styles.squareRed
        } else if (beatAlgorithm) {
          colorClass = styles.squarePurple
        } else if (player_length === optimal_length) {
          colorClass = styles.squareGreen
        } else if (i < optimal_length) {
          colorClass = styles.squareYellow
        } else {
          colorClass = styles.squareOrange
        }
      }
      squares.push(<div key={i} className={`${styles.square} ${colorClass}`} />)
    }
    return squares
  }

  return (
    <div className={styles.results}>
      {/* Hidden share card for image generation */}
      <div className={styles.shareCardWrapper}>
        <div ref={shareCardRef} className={styles.shareCard}>
          <div className={styles.shareCardHeader}>
            <span className={styles.shareCardLogo}>6°</span>
            <span className={styles.shareCardTitle}>DEGREES</span>
          </div>
          <div className={styles.shareCardPuzzle}>
            {start_word} → {end_word}
          </div>
          <div className={styles.shareCardSquares}>
            {getChainSquares()}
          </div>
          <div className={styles.shareCardStats}>
            <span className={styles.shareCardScore}>{score}</span>
            <span className={styles.shareCardLabel}>{getScoreLabel()}</span>
          </div>
          <div className={styles.shareCardSteps}>
            {isValid ? `${player_length}/${optimal_length} steps` : 'Not connected'}
          </div>
        </div>
      </div>

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

      {/* Visual chain display */}
      <div className={styles.chainVisual}>
        {getChainSquares()}
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
          disabled={sharing}
        >
          {sharing ? '...' : copied ? '✓ copied!' : '📤 share'}
        </button>
        <button className="btn btn--primary" onClick={onPlayAgain}>
          play again
        </button>
      </div>
    </div>
  )
}

export default Results
