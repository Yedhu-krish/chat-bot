import { apiFetch } from "./api"

export async function signin(username,email,password) {
    
    const response = await apiFetch(
        "http://127.0.0.1:8000/register",{
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

    const response = await apiFetch("http://127.0.0.1:8000/login",{
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