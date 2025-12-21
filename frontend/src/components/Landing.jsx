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
  // Left side cluster
  { x: 5, y: 10 },   // 0
  { x: 15, y: 20 },  // 1
  { x: 8, y: 35 },   // 2
  { x: 20, y: 45 },  // 3
  { x: 5, y: 55 },   // 4
  { x: 15, y: 65 },  // 5
  { x: 8, y: 80 },   // 6
  { x: 22, y: 90 },  // 7
  // Right side cluster
  { x: 95, y: 12 },  // 8
  { x: 85, y: 22 },  // 9
  { x: 92, y: 38 },  // 10
  { x: 80, y: 48 },  // 11
  { x: 95, y: 58 },  // 12
  { x: 85, y: 68 },  // 13
  { x: 92, y: 82 },  // 14
  { x: 78, y: 92 },  // 15
  // Top corners
  { x: 35, y: 5 },   // 16
  { x: 65, y: 8 },   // 17
  // Bottom corners
  { x: 40, y: 95 },  // 18
  { x: 58, y: 92 },  // 19
]

// Connections between nodes (indices) - all lines connect node to node
const CONNECTIONS = [
  // Left side chain
  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7],
  // Left side cross connections
  [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7],
  // Right side chain
  [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15],
  // Right side cross connections
  [8, 10], [9, 11], [10, 12], [11, 13], [12, 14], [13, 15],
  // Top connections
  [1, 16], [16, 17], [17, 9],
  // Bottom connections
  [7, 18], [18, 19], [19, 15],
  // Extra diagonal connections
  [0, 16], [8, 17], [6, 18], [14, 19],
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

