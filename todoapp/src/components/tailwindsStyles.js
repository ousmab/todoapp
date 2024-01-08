const styles = {

    input:{
        wrapper:"px-5",
        normalLabel:"display py-3 block text-cyan-800 font-bold text-sm",
        erroLabel :"display py-3 block text-red-700 font-bold text-sm",
        normalInput :"block py-2.5 px-3 w-full bg-cyan-50 text-sm text-gray-900 focus-visible:bg-cyan-100  border-0 border-b-[1px] border-cyan-700 focus:outline-none  focus:border-cyan-600 ",
        errorInput:"block py-2.5 px-3 w-full bg-red-50 text-sm text-gray-900 focus-visible:bg-red-100  border-0 border-b-[1px] border-red-700     focus:outline-none  focus:border-red-600 ",
        errorMessage :"py-3 px-3 block text-red-700 font-bold text-xs"
    },
    checkbox:"hover:text-blue-800  text-sm text-blue-900",

    button:{
        normalButton : "bg-cyan-900 h-10 px-5  rounded-full p-2 text-white mb-3 mt-6 block mx-auto active:bg-cyan-800 hover:bg-cyan-700 disabled:bg-gray-400 hover:cursor-pointer disabled:cursor-not-allowed",
        outlineButton:"font-bold hover:text-blue-800 mx-auto block text-sm text-blue-900 hover:cursor-pointer"
    },
    authWrapper:{
        wrapper :"container lg:w-4/6 mx-auto pt-10 grid grid-cols-2",
        textBox:'hidden md:block lg:block',
        text:"text-cyan-900 text-4xl font-bold pb-4",
        content:"mx-auto w-4/5 col-span-2 md:col-span-1 lg:col-span-1"
    },
    form:{
        content :'bg-white space-y-2 rounded-lg pb-4',
        title : "text-cyan-900 font-bold pt-2 text-center text-3xl"
    },
    home:{
        wrapper:"container bg-white first-line:bg-white lg:w-3/5 mx-auto p-10 mt-2",
        header:"grid grid-cols-2",
        title:"text-cyan-900 text-4xl font-bold",
        addTodoBox:{
            box:"text-right mb-20",
            button: "mx-0 bg-gray-100 p-10 rounded-lg"
        },
        content:"mt-10"

    }
   

}

export default styles;