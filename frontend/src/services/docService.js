import { apiFetch } from "./api"
const API_URL = import.meta.env.VITE_API_URL;

export async function uploadFile(selectedConversation,file) {

    const formData = new FormData()
    formData.append("file",file)
    formData.append("conversation_id",selectedConversation.id)

    const response = await apiFetch(
        `${API_URL}/documents/upload`,{
            method:"POST",
            headers:{
                Authorization:`Bearer ${localStorage.getItem("access_token")}`
            },
            body:formData
        }
    )
    const data = await response.json()
    if(!response.ok){
        throw Error(data.error || "File upload failed.")
    }
    return data
}