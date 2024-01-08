import { Link } from "react-router-dom"

function Menu (){

return (

    <nav className='bg-cyan-900 text-white h-14 py-4 w-full sticky top-0 z-1000'>
        <div className='float-right'>
            <Link className='mr-10' to="/register">S'inscrire</Link>
            <Link className='mr-10' to="/login">Se Connecter</Link>
        </div>
    </nav>

    )
}


export default Menu