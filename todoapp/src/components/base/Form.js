import styles from "../tailwindsStyles"

function Form({title, children}) {
  return (
    <form className={styles.form.content}>
            <h1 className={styles.form.title}>{title}</h1>
            {children}
    </form>
  )
}

export default Form
