import "./MessageList.css"

function MessageList({messages}){
    return(
        <div className="message-list">{
            messages.map((message,index)=>(
                <div key={message.id} className={message.role === "user"?"user-message":"assistant-message"}>
                    <strong>{message.role}</strong>
                     <p>{message.content}</p>
                </div>
            ))
            }    
        </div>
        
    )
}

export default MessageList