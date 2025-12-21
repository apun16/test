import styles from './Header.module.css'

/**
 * App header with logo and controls.
 */
function Header({ onHelpClick, onNewGame }) {
  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <button 
          className={styles.iconBtn} 
          onClick={onHelpClick}
          aria-label="How to play"
        >
          ?
        </button>
        
        <div className={styles.logo}>
          <div className={styles.logoIcon}>
            <div className={styles.node} style={{ '--delay': '0s' }} />
            <div className={styles.node} style={{ '--delay': '0.1s' }} />
            <div className={styles.node} style={{ '--delay': '0.2s' }} />
            <div className={styles.node} style={{ '--delay': '0.3s' }} />
            <div className={styles.node} style={{ '--delay': '0.4s' }} />
            <div className={styles.node} style={{ '--delay': '0.5s' }} />
            <svg className={styles.connections} viewBox="0 0 40 40">
              <path d="M20 4 L36 20 L20 36 L4 20 Z" />
              <line x1="20" y1="4" x2="20" y2="36" />
              <line x1="4" y1="20" x2="36" y2="20" />
            </svg>
          </div>
          {/* <h1 className={styles.title}>
            <span className={styles.six}>6</span>
            <span className={styles.degrees}>degrees</span>
          </h1> */}
        </div>
        
        <button 
          className={styles.iconBtn} 
          onClick={onNewGame}
          aria-label="New game"
        >
          ↻
        </button>
      </div>
    </header>
  )
}

export default Header
