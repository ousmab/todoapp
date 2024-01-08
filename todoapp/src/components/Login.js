import React from 'react'
import AuthWrapper from './base/AuthWrapper'
import InputField from './base/InputField'
import CheckBox from './base/CheckBox'
import Button from './base/Button'
import Form from './base/Form'


function Login() {
  return (

    <AuthWrapper
        img={"img/task.svg"}
        alt="illustration_taches"
        text="Toutes vos tâches en un seul endroit"
        >
      
        <Form title="Connexion">
                <InputField 
                    value={""}
                    placeholder="votre nom d'utilisateur"
                    onChange={()=>console.log("bonjour")}
                    label={"Nom d'utilisateur"}
                    hasError={false} 
                    errorMessage={"Votre nom d'utilsateur est incorrect"}
                    />

                <InputField 
                    hasError={true} 
                    errorMessage={"Votre nom d'utilsateur est incorrect"}
                    >Mot de passe</InputField>
            

                <CheckBox 
                id="remember"
                label={"Rester Connecter"}
                onChange={()=>console.log("ckeck")}
                />
                
                <Button 
                    outline={false}
                    type={"submit"}
                    text="Se connecter"
                    onClick={()=>console.log("clik")}
                    />


                <Button
                    outline={true}
                    type={"button"}
                    text={"Mot de passe oublié ?"}
                />  

        </Form>
                
         
    </AuthWrapper>
  )
}

export default Login
