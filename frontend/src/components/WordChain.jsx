import styles from './WordChain.module.css'

/**
 * Visual representation of the word chain.
 * Shows the path from start to end word.
 */
function WordChain({ startWord, endWord, chain, onRemoveWord }) {
  const allWords = [startWord, ...chain]
  
  return (
    <div className={styles.chain}>
      {allWords.map((word, index) => (
        <div key={`${word}-${index}`} className={styles.step}>
          <div 
            className={`${styles.word} ${index === 0 ? styles.startWord : styles.chainWord}`}
            onClick={index > 0 && index === allWords.length - 1 ? onRemoveWord : undefined}
            role={index > 0 && index === allWords.length - 1 ? 'button' : undefined}
            tabIndex={index > 0 && index === allWords.length - 1 ? 0 : undefined}
            title={index > 0 && index === allWords.length - 1 ? 'Click to remove' : undefined}
          >
            {word}
            {index > 0 && index === allWords.length - 1 && (
              <span className={styles.removeHint}>×</span>
            )}
          </div>
          
          {index < allWords.length - 1 && (
            <div className={styles.connector}>
              <div className={styles.line} />
              <span className={styles.stepNumber}>{index + 1}</span>
            </div>
          )}
        </div>
      ))}
      
      {/* Show target word as ghost */}
      {chain.length > 0 && (
        <>
          <div className={styles.step}>
            <div className={styles.connector}>
              <div className={styles.lineDashed} />
              <span className={styles.stepNumber}>?</span>
            </div>
          </div>
          <div className={styles.step}>
            <div className={`${styles.word} ${styles.targetWord}`}>
              {endWord}
            </div>
          </div>
        </>
      )}
      
      {/* Empty state */}
      {chain.length === 0 && (
        <div className={styles.empty}>
          <span className={styles.emptyText}>your chain will appear here</span>
        </div>
      )}
    </div>
  )
}

export default WordChain

