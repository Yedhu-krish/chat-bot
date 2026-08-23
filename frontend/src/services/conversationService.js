import { apiFetch } from "./api"
const API_URL = import.meta.env.VITE_API_URL;


export async function getConversations() {
    const response = await apiFetch(
        `${API_URL}/all-user-conversations`,{
            method:"GET",
            headers:{
                "Content-Type":"application/json",
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            }
        }
    )
    const data = await response.json()
    if(!response.ok){
        throw Error(data.error || "Conversation loading failed")
    }
    
    return data
}

export async function getConversationMessages(selectedConversationId){
    const response = await apiFetch(
        `${API_URL}/conversation/${selectedConversationId}/messages`,{
            method:"GET",
            headers:{
                "Content-Type":"application/json",
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            }
        }
    )
    const data = await response.json()
    if(!response.ok){
        throw Error(data.error || "Message fetching failed for this conversation")
    }
    return data
}

export async function createNewConversation(title) {
    const response = await apiFetch(
        `${API_URL}/new-conversation`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            },
            body:JSON.stringify({
                title:title
            })
        }
    )
    const data = await response.json()
    if(!response.ok){
        throw Error(data.error || "Conversation creation failed")
    }
    return data
}

export async function DeleteConversation(conversationId) {

    const response = await apiFetch(`${API_URL}/conversation/${conversationId}`,{
        method:"DELETE"
    }
    )
    const data = await response.json()
    if(!response.ok){
        throw Error(data.error || "Delete action failed")
    }
    return data
    
}

export async function getConversationDocuments(conversationId) {
    const response = await apiFetch(`${API_URL}/documents/${conversationId}`,{
        method:"GET"
    }
    )
    const data = await response.json()
    if(!response.ok){
        throw Error(data.error || "Document fetch failed.")
    }
    return data
}