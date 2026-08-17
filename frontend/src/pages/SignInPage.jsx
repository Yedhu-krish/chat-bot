import { useState } from "react"
import { signin } from "../services/authService"

function SignInPage({setShowLogin}){
    const [username,setUsername] = useState("")
    const [email,setEmail] = useState("")
    const [password,setPassword] = useState("")
    const [confirmPassword,setconfirmPassword] = useState("")

    async function handleSignIn(e) {
        e.preventDefault()
        if(password !== confirmPassword){
            alert("Passwords donot match")
            return
        }
        try{
            const response = await signin(username,email,password)
            alert("Account created successfully.")
            setShowLogin(true)
        }catch(error){
            alert(error.message)
        }        
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h2>Register</h2>
    
                <form onSubmit={handleSignIn}>
                    <input required placeholder="Username" type="text" value={username} onChange={(e) => setUsername(e.target.value)}/>    
                    <input required type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>    
                    <input required placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>    
                    <input required placeholder="Re-type password" type="password" value={confirmPassword} onChange={(e) => setconfirmPassword(e.target.value)}/>
                    <button type="submit">Register</button>
                </form>
            </div>
        </div>
    )
}


export default SignInPage