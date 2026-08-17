import { useEffect, useState } from "react";
import ChatInput from "../components/ChatInput";
import MessageList from "../components/MessageList";
import { sendMessage } from "../services/chatService"
import { logout } from "../services/authService";
import { getConversations } from "../services/conversationService";
import { getConversationMessages } from "../services/conversationService";
import { createNewConversation } from "../services/conversationService";
import UploadDocument from "../components/UploadDocument";
import ConversationList from "../components/ConversationList";
import NewConversation from "../components/NewConversation";
import DocumentList from "../components/DocumentList";

function ChatPage({setToken}){
    const [messages,setMessages] = useState([])
    const [conversations,setConversations] = useState([])
    const [selectedConversation,setSelectedConversation] = useState(null)
    const [showNewConversation,setshowNewConversation] = useState(false)
    

    async function loadMessages(conversationId){
      const data = await getConversationMessages(conversationId)
      setMessages(data)
    }

    useEffect(()=>{
      if(selectedConversation){
        loadMessages(selectedConversation?.id)
      }
    },[selectedConversation])

    async function loadConversations(){
      const data = await getConversations()
      console.log(data)
      setConversations(data)
      const updated = data.find(c=>c.id === selectedConversation?.id)
      setSelectedConversation(updated)
    }

    useEffect(()=>{
      loadConversations()
    },[])

    function handleLogout() {
      logout()
      setToken(null)
    }
    async function handleSend(message){
      if(!selectedConversation){
        alert("Please select a conversation first!")
        return
      }
      const assistantId = crypto.randomUUID()
      setMessages(prev=>[
        ...prev,
        {
          id: crypto.randomUUID(),
          role:"user",
          content:message
        },
        {
          id:assistantId,
          role:"assistant",
          content:""
        }
      ])
        const response = await sendMessage(message,selectedConversation?.id)
        console.log("=======",response,"========")
        const reader = response.body.getReader()
        let fullText = ""
        let result
        const decoder = new TextDecoder()
    
        do{
          result = await reader.read()
          if(result.value){
            const text = decoder.decode(result.value)

          setMessages(prev=>prev.map(message=>
            message.id === assistantId?{
                ...message,
                content: message.content + text
              } :  message
          ))
        }
          
        }while(!result.done)
      }

      function handleConversationDelete(conversationId){
        setConversations(prev=>prev.filter(conversation => conversation.id !== conversationId))
        if(selectedConversation?.id === conversationId){
          setSelectedConversation(null)
          setMessages([])
        }
      }

      return(
        <div className="chat-layout">
          <aside className="sidebar">
            <h2>AI Document Chat</h2>
                <div className="sidebar-top">
                    <button onClick={()=>setshowNewConversation(true)}>+ New Conversation</button>
                    {showNewConversation && (
                      <NewConversation onConversationCreated={(conversation)=>{setConversations(prev=>[...prev,conversation])
                        setSelectedConversation(conversation)
                      setshowNewConversation(false)}} />
                    )}
                    <ConversationList conversations={conversations} selectedConversation={selectedConversation} onSelectConversation={setSelectedConversation} onDeleteConversation={handleConversationDelete} />
                    {selectedConversation &&(
                      <DocumentList selectedConversation={selectedConversation}/>
                    )}
                </div>
                <button className="logout-button" onClick={handleLogout}>LOGOUT</button>
          </aside>
          
          <main className="chat-area">
                {selectedConversation ? (
                    <>
                      <div className="chat-header">
                          <h2>{selectedConversation.title}</h2>
                            <UploadDocument selectedConversation={selectedConversation} onUploadSuccess={loadConversations}/>
                        </div>

                        {selectedConversation.doc_count === 0 ? (
                            <div className="chat-empty">
                                <h2>Upload a document to get started</h2>
                                <p>
                                    Upload a PDF to this conversation before asking questions.
                                </p>
                            </div>
                        ) : messages.length === 0 ? (
                            <div className="chat-empty">
                                <h2>Ready to chat</h2>
                                <p>Ask a question about your uploaded documents.</p>
                            </div>
                        ) : (
                            <MessageList messages={messages} />
                        )}
                        <ChatInput onSend={handleSend} disabled={selectedConversation.doc_count === 0}/>
                    </>
                ) : (
                    <div className="welcome-screen">
                        <h1>Welcome to AI Document Chat</h1>
                        <p>
                            Select a conversation or create a new one to start chatting.
                        </p>
                    </div>
                )}
          </main>

        </div>
      )
}

export default ChatPage