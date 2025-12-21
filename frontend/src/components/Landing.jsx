import { useState, useEffect } from 'react'
import styles from './Landing.module.css'

// Example chains that cycle through
const EXAMPLE_CHAINS = [
  'SUN → LIGHT → DAY → WORK → MONEY',
  'OCEAN → WAVE → BEACH → SAND → CASTLE',
  'MUSIC → SONG → BIRD → FLY → SKY',
  'COFFEE → MORNING → SUNRISE → ORANGE → FRUIT',
  'HEART → LOVE → FAMILY → HOME → HOUSE',
  'STAR → NIGHT → MOON → TIDE → OCEAN',
  'BOOK → READ → LEARN → SCHOOL → FRIEND',
  'FIRE → HEAT → SUN → STAR → SPACE',
]

// Network node positions for background (avoiding center where content is)
const NODES = [
  { x: 10, y: 15 }, { x: 25, y: 8 }, { x: 40, y: 20 },
  { x: 55, y: 10 }, { x: 70, y: 18 }, { x: 85, y: 12 },
  { x: 15, y: 35 }, { x: 25, y: 42 }, { x: 8, y: 45 },
  { x: 75, y: 42 }, { x: 80, y: 35 }, { x: 92, y: 40 },
  { x: 8, y: 55 }, { x: 18, y: 60 }, { x: 12, y: 52 },
  { x: 88, y: 58 }, { x: 82, y: 55 }, { x: 92, y: 62 },
  { x: 12, y: 75 }, { x: 28, y: 82 }, { x: 45, y: 78 },
  { x: 60, y: 85 }, { x: 75, y: 72 }, { x: 90, y: 80 },
  { x: 5, y: 90 }, { x: 35, y: 92 }, { x: 62, y: 95 }, { x: 95, y: 88 },
]

// Connections between nodes (indices)
const CONNECTIONS = [
  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
  [0, 6], [1, 7], [2, 8], [3, 9], [4, 10], [5, 11],
  [6, 7], [7, 8], [8, 9], [9, 10], [10, 11],
  [6, 12], [7, 13], [8, 14], [9, 15], [10, 16], [11, 17],
  [12, 13], [13, 14], [14, 15], [15, 16], [16, 17],
  [12, 18], [13, 19], [14, 20], [15, 21], [16, 22], [17, 23],
  [18, 19], [19, 20], [20, 21], [21, 22], [22, 23],
  [18, 24], [20, 25], [21, 26], [23, 27],
  [2, 9], [7, 14], [8, 15], [13, 20], [14, 21], [19, 25],
]

/**
 * Landing page with intro and play button.
 */
function Landing({ onPlay }) {
  const [isVisible, setIsVisible] = useState(false)
  const [chainIndex, setChainIndex] = useState(0)
  const [isFading, setIsFading] = useState(false)
  
  useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 100)
    return () => clearTimeout(timer)
  }, [])

  // Cycle through example chains
  useEffect(() => {
    const interval = setInterval(() => {
      setIsFading(true)
      setTimeout(() => {
        setChainIndex(prev => (prev + 1) % EXAMPLE_CHAINS.length)
        setIsFading(false)
      }, 300)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className={`${styles.landing} ${isVisible ? styles.visible : ''}`}>
      {/* Network graph background */}
      <svg className={styles.network} viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice">
        {/* Connection lines */}
        {CONNECTIONS.map(([from, to], i) => (
          <line
            key={`line-${i}`}
            x1={NODES[from].x}
            y1={NODES[from].y}
            x2={NODES[to].x}
            y2={NODES[to].y}
            className={styles.networkLine}
            style={{ '--delay': `${(i * 0.05)}s` }}
          />
        ))}
        {/* Nodes */}
        {NODES.map((node, i) => (
          <circle
            key={`node-${i}`}
            cx={node.x}
            cy={node.y}
            r="0.8"
            className={styles.networkNode}
            style={{ '--delay': `${(i * 0.03)}s` }}
          />
        ))}
      </svg>

      <div className={styles.content}>
        {/* Logo */}
        <div className={styles.logo}>
          <span className={styles.six}>6</span>
          <span className={styles.degree}>°</span>
        </div>
        
        <h1 className={styles.title}>degrees</h1>
        
        <p className={styles.tagline}>
          connect any two words in six steps
        </p>
        
        <p className={styles.description}>
          every word links to another. find the path.
        </p>

        {/* Play button */}
        <button className={styles.playBtn} onClick={onPlay}>
          <span className={styles.playText}>play</span>
          <span className={styles.playArrow}>→</span>
        </button>
        
        <div className={styles.hint}>
          <span className={styles.hintIcon}>○</span>
          <span className={`${styles.hintText} ${isFading ? styles.fading : ''}`}>
            {EXAMPLE_CHAINS[chainIndex]}
          </span>
          <span className={styles.hintIcon}>○</span>
        </div>
      </div>
    </div>
  )
}

export default Landing

