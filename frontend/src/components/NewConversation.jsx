import { useState } from "react"
import { createNewConversation } from "../services/conversationService"

function NewConversation({onConversationCreated}) {
    const [newConversationTitle,setnewConversationTitle] = useState("")    


    async function handleConversationCreation(){
        if(!newConversationTitle){
            alert("Please enter a title")
            return
        }
        const data = await createNewConversation(newConversationTitle)
        onConversationCreated(data)
        newConversationTitle("")
        }

    return(
        <div className="new-conversation">
              <input placeholder="Conversation title" value={newConversationTitle} type="text" onChange={(e)=>setnewConversationTitle(e.target.value)}/> 
              <button onClick={handleConversationCreation}>Create</button>
        </div>
    )
}

export default NewConversation