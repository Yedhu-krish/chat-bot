import { apiFetch } from "./api"
const API_URL = import.meta.env.VITE_API_URL;


export async function sendMessage(message,selectedConversationId){
    const response = await apiFetch(`${API_URL}/chat`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            },
            body:JSON.stringify({
                message:message,
                conversation_id:selectedConversationId,
                document_id:5
            })
        }
    )
    return(response)
}