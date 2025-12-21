import { useState, useEffect } from 'react'
import styles from './Landing.module.css'

/**
 * Landing page with intro and play button.
 */
function Landing({ onPlay }) {
  const [isVisible, setIsVisible] = useState(false)
  
  useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className={`${styles.landing} ${isVisible ? styles.visible : ''}`}>
      {/* Floating orbs background */}
      <div className={styles.orbs}>
        <div className={styles.orb} style={{ '--delay': '0s', '--x': '20%', '--y': '30%' }} />
        <div className={styles.orb} style={{ '--delay': '2s', '--x': '80%', '--y': '20%' }} />
        <div className={styles.orb} style={{ '--delay': '4s', '--x': '60%', '--y': '70%' }} />
        <div className={styles.orb} style={{ '--delay': '1s', '--x': '30%', '--y': '80%' }} />
        <div className={styles.orb} style={{ '--delay': '3s', '--x': '70%', '--y': '50%' }} />
        <div className={styles.orb} style={{ '--delay': '5s', '--x': '15%', '--y': '60%' }} />
      </div>
      
      {/* Connection lines */}
      <svg className={styles.connections} viewBox="0 0 400 400">
        <line x1="80" y1="120" x2="320" y2="80" className={styles.line} style={{ '--delay': '0.5s' }} />
        <line x1="320" y1="80" x2="240" y2="280" className={styles.line} style={{ '--delay': '0.7s' }} />
        <line x1="240" y1="280" x2="120" y2="320" className={styles.line} style={{ '--delay': '0.9s' }} />
        <line x1="120" y1="320" x2="280" y2="200" className={styles.line} style={{ '--delay': '1.1s' }} />
        <line x1="280" y1="200" x2="60" y2="240" className={styles.line} style={{ '--delay': '1.3s' }} />
        <line x1="60" y1="240" x2="80" y2="120" className={styles.line} style={{ '--delay': '1.5s' }} />
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
          <span className={styles.hintText}>SUN → LIGHT → DAY → WORK → MONEY</span>
          <span className={styles.hintIcon}>○</span>
        </div>
      </div>
    </div>
  )
}

export default Landing

