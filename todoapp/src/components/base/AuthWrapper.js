import styles from "../tailwindsStyles"


function AuthWrapper(props) {

  const {text, img, alt, children } = props
  return (
    <div className={styles.authWrapper.wrapper}>
    {/** image box */}
      <div className={styles.authWrapper.textBox}>
          <h1 className={styles.authWrapper.text}>{text}</h1>
          <img src={img} alt={alt}/>
      </div>

      {/** form box */}
      <div className={styles.authWrapper.content}>
         {children}
      </div>
  </div>
  )
}

export default AuthWrapper
