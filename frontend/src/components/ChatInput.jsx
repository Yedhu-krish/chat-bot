import { useState } from "react";


function ChatInput({onSend,disabled}){
    const [message,setMessage] = useState("")
    function addMessage(){
        onSend(message)
        setMessage("")
    }
    return(
        <div className="chat-input">
            <input disabled={disabled} type="text" value={message} onChange={(e) => setMessage(e.target.value)}/>
            <button disabled={disabled} onClick={addMessage}>Send</button>
        </div>
    )
}

export default ChatInput