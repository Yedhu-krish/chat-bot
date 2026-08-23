import { apiFetch } from "./api"
const API_URL = import.meta.env.VITE_API_URL;


export async function signin(username,email,password) {
    
    const response = await apiFetch(
        `${API_URL}/register`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({username,email,password})
        }
    )
    const data = await response.json()
    if(!response.ok){
        throw new Error(data.detail || "SignIn Failed")
    }
    return data
}




export async function login(username,password) {

    const formData = new URLSearchParams()

    formData.append("username",username)
    formData.append("password",password)

    const response = await apiFetch(`${API_URL}/login`,{
        method:"POST",
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        body:formData
    })

    const data = await response.json()
    if(!response.ok){
        throw new Error(data.detail || "Login failed")
    }
    return data
}

export function logout(){
     return localStorage.removeItem("access_token")
}