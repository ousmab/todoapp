import React from 'react'
import AuthWrapper from './base/AuthWrapper'
import Button from './base/Button'
import { HiOutlineHome } from "react-icons/hi";
import { TfiReload } from "react-icons/tfi";

function ErrorPage() {

  console.log(process.env.PUBLIC_URL)

  return (
    <AuthWrapper
        img={process.env.PUBLIC_URL+"/img/errorPage.svg"}
        alt="Erreur"
        text=""
    >

    <div className="mt-72">
        <h1 className='text-red-800 font-bold text-center mb-10'>Oups une erreur est survenue !</h1>
        <div className='grid grid-cols-2'>
                
                <Button
                    icon={<HiOutlineHome size={30} className=' text-cyan-900'/>}
                    to={"/"}
                    text={"Revenir à l'accueil"}
                    outline={true}
                    />
                
                <Button
                    icon={<TfiReload size={30}   className='ml-10 text-cyan-900'/>}
                    text={"Récharger la page"}
                    type={"button"}
                    outline={true}
                    />
        </div>
    </div>
    </AuthWrapper>
  )
}

export default ErrorPage
