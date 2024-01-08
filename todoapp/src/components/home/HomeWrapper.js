import styles from "../tailwindsStyles"
import Button from "../base/Button"
import { MdOutlineKeyboardBackspace } from "react-icons/md";
import { FaPlus } from "react-icons/fa6";


function HomeWrapper(props) {


 const {
        children, 
        content,
        title,
        backTo,
        buttonBoxEnable
    } = props


const backButton = (
        <Button 
        to={backTo}
        outline={true}
        text="retour" 
        icon={<MdOutlineKeyboardBackspace size={20} className="inline"/>}

         />
)

const addButton = (
    <div >
        <Button outline className={styles.home.addTodoBox.button}>
            <FaPlus size={25} />
        </Button>
    </div>
)
 
  return (
    <div className={styles.home.wrapper}>
          <div className={styles.home.header}>
            <h1 className={styles.home.title}>{ title} </h1>
            <div className={styles.home.addTodoBox.box}>
                {backTo && backButton }
            </div>
                {buttonBoxEnable &&  addButton}
          </div>

          <div className={styles.home.content}>
                {children || content}
          </div>
    </div>
  )
}

export default HomeWrapper
