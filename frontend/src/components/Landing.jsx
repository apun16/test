import { useState, useEffect } from 'react'
import styles from './Landing.module.css'

// Example word pairs with their paths
const EXAMPLES = [
  { start: 'SUN', end: 'MONEY', path: ['LIGHT', 'DAY', 'WORK'] },
  { start: 'OCEAN', end: 'CASTLE', path: ['WAVE', 'BEACH', 'SAND'] },
  { start: 'MUSIC', end: 'SKY', path: ['SONG', 'BIRD', 'FLY'] },
  { start: 'HEART', end: 'HOUSE', path: ['LOVE', 'FAMILY', 'HOME'] },
  { start: 'STAR', end: 'OCEAN', path: ['NIGHT', 'MOON', 'TIDE'] },
  { start: 'FIRE', end: 'SPACE', path: ['HEAT', 'SUN', 'STAR'] },
]

/**
 * Landing page with intro and play button.
 */
function Landing({ onPlay }) {
  const [isVisible, setIsVisible] = useState(false)
  const [exampleIndex, setExampleIndex] = useState(0)
  const [isTransitioning, setIsTransitioning] = useState(false)
  
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 100)
    return () => clearTimeout(timer)
  }, [])

  // Cycle through examples
  useEffect(() => {
    const interval = setInterval(() => {
      setIsTransitioning(true)
      setTimeout(() => {
        setExampleIndex(prev => (prev + 1) % EXAMPLES.length)
        setIsTransitioning(false)
      }, 400)
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  const currentExample = EXAMPLES[exampleIndex]

  return (
    <div className={`${styles.landing} ${isVisible ? styles.visible : ''}`}>
      {/* Ambient background */}
      <div className={styles.ambient}>
        <div className={styles.glow} style={{ '--x': '20%', '--y': '30%', '--size': '400px', '--delay': '0s' }} />
        <div className={styles.glow} style={{ '--x': '80%', '--y': '60%', '--size': '300px', '--delay': '2s' }} />
        <div className={styles.glow} style={{ '--x': '50%', '--y': '80%', '--size': '350px', '--delay': '4s' }} />
      </div>

      {/* Floating particles */}
      <div className={styles.particles}>
        {[...Array(12)].map((_, i) => (
          <div 
            key={i} 
            className={styles.particle}
            style={{ 
              '--x': `${10 + (i * 7) % 80}%`,
              '--y': `${15 + (i * 11) % 70}%`,
              '--duration': `${20 + (i * 3)}s`,
              '--delay': `${i * 0.5}s`
            }}
          />
        ))}
      </div>

      <div className={styles.content}>
        {/* Logo section */}
        <div className={styles.logoSection}>
          <div className={styles.logoWrapper}>
            <div className={styles.logoRing} />
            <div className={styles.logoRing} style={{ '--delay': '0.5s', '--size': '120%' }} />
            <span className={styles.logoNumber}>6</span>
            <span className={styles.logoDegree}>°</span>
          </div>
          <h1 className={styles.logoText}>degrees</h1>
        </div>

        {/* Tagline */}
        <div className={styles.taglineSection}>
          <p className={styles.tagline}>
            Connect any two words
          </p>
          <p className={styles.taglineSub}>
            in six steps or fewer
          </p>
        </div>

        {/* Live example preview */}
        <div className={`${styles.exampleSection} ${isTransitioning ? styles.transitioning : ''}`}>
          <div className={styles.exampleLabel}>example</div>
          <div className={styles.examplePath}>
            <span className={styles.exampleWord + ' ' + styles.startWord}>
              {currentExample.start}
            </span>
            {currentExample.path.map((word, i) => (
              <span key={i} className={styles.exampleStep}>
                <span className={styles.exampleArrow}>→</span>
                <span className={styles.exampleWord}>{word}</span>
              </span>
            ))}
            <span className={styles.exampleStep}>
              <span className={styles.exampleArrow}>→</span>
              <span className={styles.exampleWord + ' ' + styles.endWord}>
                {currentExample.end}
              </span>
            </span>
          </div>
          <div className={styles.exampleDots}>
            {EXAMPLES.map((_, i) => (
              <button 
                key={i} 
                className={`${styles.dot} ${i === exampleIndex ? styles.activeDot : ''}`}
                onClick={() => {
                  setIsTransitioning(true)
                  setTimeout(() => {
                    setExampleIndex(i)
                    setIsTransitioning(false)
                  }, 200)
                }}
                aria-label={`Example ${i + 1}`}
              />
            ))}
          </div>
        </div>

        {/* Play button */}
        <button className={styles.playBtn} onClick={onPlay}>
          <span className={styles.playBg} />
          <span className={styles.playContent}>
            <span className={styles.playIcon}>▶</span>
            <span className={styles.playLabel}>Start Playing</span>
          </span>
        </button>

        {/* Footer hint */}
        <p className={styles.footerHint}>
          No login required · New puzzle every game
        </p>
      </div>
    </div>
  )
}

export default Landing
