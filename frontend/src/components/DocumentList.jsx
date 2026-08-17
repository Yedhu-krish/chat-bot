import { useEffect, useState } from "react"
import { getConversationDocuments } from "../services/conversationService"

function DocumentList({conversationId}){
    const [documentList,setDocumentList] = useState([])

    async function loadDocuments() {
        const data = await getConversationDocuments(conversationId)
        setDocumentList(data)
        console.log("%%%%",data,"%%%%%%%%%")
    }

    useEffect(()=>{
        if(conversationId){
            loadDocuments()
        }
    },[conversationId])
   
    return (
        <div className="document-list">
            {documentList.map(document => (
                <div key={document.id} className="document-item">
                    <h2>{document.file_name}</h2>
                    <h3>{ new Date(document.created_at).toLocaleString()}</h3>
                </div>
            ))}
        </div>
    )
}

export default DocumentList