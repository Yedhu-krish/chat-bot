import { useState } from "react"
import ChatInput from "./components/ChatInput";
import MessageList from "./components/MessageList";
import ChatPage from "./pages/ChatPage";
import LoginPage from "./pages/LoginPage";
import SignInPage from "./pages/SignInPage";
import "./App.css"

function App(){
  const [token,setToken] = useState(localStorage.getItem("access_token"))
  const [showLogin,setShowLogin] = useState(true)
  console.log("=====",showLogin,"======")
  console.log(localStorage)
  // localStorage.clear()

  if(!token){
    if(!showLogin){
      return(
        <div>
          <SignInPage setShowLogin={setShowLogin}/>
        </div>        
      )}
    return(
      <div>
        <LoginPage setToken={setToken} setShowLogin={setShowLogin}/>
      </div>
    )
  }

  return(
    <div>
      <ChatPage setToken={setToken}/>

    </div>
  )
}
  


export default App