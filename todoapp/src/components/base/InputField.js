import styles from "../tailwindsStyles"

function InputField(props) {



 const {
            hasError, 
            errorMessage, 
            label, 
            children, 
            type="text", 
            placeholder, 
            onChange,
            value

        
        } = props

  return (
        <div className={styles.input.wrapper}>
            <label 
                className={hasError ?  styles.input.erroLabel : styles.input.normalLabel  }
                >{children || label}</label>
            
            <input   
                value={value}
                onChange={onChange}
                className={ hasError ? styles.input.errorInput : styles.input.normalInput} 
                type={type}
                placeholder={placeholder}
                />
           { hasError &&  <span className={styles.input.errorMessage }>{ errorMessage } </span>  }
        </div>
  )
}

export default InputField
 