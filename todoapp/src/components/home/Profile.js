import Button from "../base/Button"
import HomeWrapper from "./HomeWrapper"
import { FaClipboardList } from "react-icons/fa6";
import { IoLockClosedOutline } from "react-icons/io5";
import { BiEdit } from "react-icons/bi";


function Profile() {
  return (
   <HomeWrapper
      title="Profil"
      backTo="../dashboard"
      >

       <div className="">
            <div className="grid grid-cols-2">
                <div className="mb-10">
                    <label className="relative cursor-pointer left-32">
                        <input type="file" className="hidden" /> <BiEdit size={25} className="text-cyan-700"/>
                    </label>
                    <img
                      src={process.env.PUBLIC_URL+"/img/profil.jpg"}
                      alt="user_profile_image"
                      className="rounded-full w-36"
                    />
                </div>

                <div className="mb-10 -ml-36 pt-10">
                    <span className="block font-bold mb-3">Username</span>
                    <span className="block text-gray-400">Email@gmail.com</span>
                </div>

            </div>


            <div className="grid grid-cols-2">
                <Button
                    icon={<FaClipboardList size={25} className="inline"/>}
                    text={"Modifier mes informations"}
                    outline
                    className="mx-0"
                />

              <Button
                    icon={<IoLockClosedOutline size={25} className="inline"/>}
                    text={"Modifier mon mot de passe"}
                    outline
                    className="mx-0"
                />

            </div>

       </div>
    </HomeWrapper>
  )
}

export default Profile
