import { apiFetch } from "./api"

export async function sendMessage(message,selectedConversationId){
    const response = await apiFetch("http://127.0.0.1:8000/chat",{
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