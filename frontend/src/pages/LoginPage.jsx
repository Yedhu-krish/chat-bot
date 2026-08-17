import { useState } from "react";
import { login } from "../services/authService";

function LoginPage({setToken,setShowLogin}){
    const [username,setUsername] = useState("")
    const [password,setPassword] = useState("")

    async function handleLogin(){
        const response = await login(username,password)

        localStorage.setItem("access_token",response.access_token)
        setToken(response.access_token)
    }

    return(
        <div className="auth-page">
            <div className="auth-card">
                <h2>Login</h2>
                <input type="text" value={username} onChange={(e)=>setUsername(e.target.value)}/>
                <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
                <button onClick={handleLogin}>Login</button>
                <h3>New User ?</h3>
                <button onClick={()=>setShowLogin(false)}>Create Account</button>
            </div>
        </div>
    )
}

export default LoginPage