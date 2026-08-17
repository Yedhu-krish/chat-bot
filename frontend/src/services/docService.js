import { apiFetch } from "./api"

export async function uploadFile(selectedConversation,file) {

    const formData = new FormData()
    formData.append("file",file)
    formData.append("conversation_id",selectedConversation.id)

    const response = await apiFetch(
        "http://127.0.0.1:8000/documents/upload",{
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