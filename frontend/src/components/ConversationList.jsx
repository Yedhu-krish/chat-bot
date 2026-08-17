import { useState } from "react"
import { DeleteConversation } from "../services/conversationService"
import DocumentList from "./DocumentList"

function ConversationList({conversations,selectedConversation,onSelectConversation,onDeleteConversation}){
    const [expandedConversationId, setExpandedConversationId] = useState(null)

    async function handleDelete(conversationId) {
        const response = await DeleteConversation(conversationId)
        onDeleteConversation(conversationId)
    }
    return( 
        <div>{
            conversations.map(conversation =>(
                // <div className="conversation-item" key={conversation.id}>
                //     <span onClick={() => onSelectConversation(conversation)} >{conversation.title}</span>
                //     <button onClick={() =>setExpandedConversationId(expandedConversationId === conversation.id? null : conversation.id)}>
                //         {expandedConversationId === conversation.id ? "▾" : "▸"}
                //     </button>
                //     <button className="delete-button" onClick={()=>handleDelete(conversation.id)}>Delete</button>
                //     {expandedConversationId === conversation.id && (
                //         <DocumentList conversationId={conversation.id} />
                //     )}
                // </div>
                <div className="conversation-item" key={conversation.id}>
                    <div className="conversation-header">

                        <span className="conversation-title" onClick={() => onSelectConversation(conversation)}>
                            {conversation.title}
                        </span>

                        <button
                            className="expand-button"
                            onClick={() =>
                                setExpandedConversationId(
                                    expandedConversationId === conversation.id
                                        ? null
                                        : conversation.id
                                )
                            }
                        >
                            {expandedConversationId === conversation.id ? "⌄" : "›"}
                        </button>

                        <button className="delete-button" onClick={() => handleDelete(conversation.id)}>Delete</button>

                    </div>

                    {expandedConversationId === conversation.id && (
                        <DocumentList conversationId={conversation.id} />
                    )}

                </div>
            ))}
        </div>
    )
}


export default ConversationList