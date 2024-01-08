import styles from "../tailwindsStyles"
import { Link } from "react-router-dom"

function Button(props) {

 const {to, type, text, children, disabled, onClick, outline=false, icon, className} = props

  const handleClick =(e)=>{
        e.preventDefault()
        onClick()
  }

  const normalButton = (
        <div className={styles.input.wrapper}>
          
            <button  
                type={type} 
                className={styles.button.normalButton+" "+className}
                disabled={disabled}
                onClick={handleClick}
            >{icon} {text || children}</button>

        </div>
  )

  const oultineButton = (
    <div>
      
        <button 
            type={type} 
            className={styles.button.outlineButton+" "+className} 
            disabled={disabled}
            onClick={handleClick}
          >{icon} {text || children } </button>
    </div>

)  


const linkButton = (
  <div>
     
     <Link 
        to={to} 
        className={styles.button.outlineButton+" "+className}  
        disabled={disabled} 
        > {icon} {text || children}</Link>
  </div>

)  

  return outline ? (to ? linkButton : oultineButton) : normalButton
}

export default Button
