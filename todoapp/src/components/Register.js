
import AuthWrapper from './base/AuthWrapper'
import InputField from './base/InputField'
import Button from './base/Button'
import Form from './base/Form'



function Register() {
  return (
    <AuthWrapper
        img={"img/register.svg"}
        alt="illustration_taches"
        text="Créer Votre Compte dès maintenant"
        >
        
        <Form 
            title="S'inscrire"
        >
            <InputField 
                value={""}
                placeholder="votre nom d'utilisateur"
                onChange={()=>(console.log("object"))}
                label={"Nom d'utilisateur"}
                hasError={false} 
                errorMessage={"Votre nom d'utilsateur est incorrect"}
                />

            <InputField 
                type={"email"}
                value={""}
                placeholder="Email"
                onChange={()=>(console.log("object"))}
                label={"Nom d'utilisateur"}
                hasError={false} 
                errorMessage={"Votre nom d'utilsateur est incorrect"}
                />

            <InputField 
                hasError={true} 
                errorMessage={"Votre nom d'utilsateur est incorrect"}
                >Mot de passe</InputField>
                <InputField 
                hasError={true} 
                errorMessage={"Votre nom d'utilsateur est incorrect"}
                >Confirmer Mot de Passe</InputField>

            
            
            <Button 
                outline={false}
                type={"submit"}
                text="S'inscrire"
                onClick={()=>console.log("clik")}
                />

        </Form>

               


              
      
    </AuthWrapper>
  )
  
}

export default Register
