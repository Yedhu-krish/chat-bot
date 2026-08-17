import { useRef, useState } from "react";
import { uploadFile } from "../services/docService";

function UploadDocument({selectedConversation,onUploadSuccess}){
    const [file,setFile] = useState(null)
    const fileInputRef = useRef(null)

    async function handleUpload() {
        const data = await uploadFile(selectedConversation,file)
        onUploadSuccess()
        fileInputRef.current.value = null
        setFile(null)
    }

    return(
        <div>
            <input ref={fileInputRef} type="file" accept=".pdf" onChange={(e)=>setFile(e.target.files[0])} />
            <button disabled={!file} onClick={handleUpload}>Upload</button>
        </div>
    )
}

export default UploadDocument