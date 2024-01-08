import styles from "../tailwindsStyles"

function CheckBox(props) {

 const { onChange , label, children, id} = props
 
  return (
    <div className={styles.input.wrapper}>
        <input 
            onChange={onChange}
            type="checkbox" 
            id={id}/>
        <label htmlFor={id} className={styles.checkbox}>{label || children}</label>
    </div>
  )
}

export default CheckBox
