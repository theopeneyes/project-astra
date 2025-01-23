import React, { useState,useEffect } from 'react';
import axios from 'axios';
import { pageName } from "./common/pagesName";
import { useComponentName } from "./common/loadedComponentName";

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [uploadedUrl, setUploadedUrl] = useState('');
    const { setComponentName } = useComponentName(pageName.fileUpload);

    useEffect(() => {
        debugger
        setComponentName(pageName.fileUpload);
      }, []);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setUploadedUrl(response.data.url);
        } catch (err) {
            console.error('Upload error:', err);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>
            {uploadedUrl && <p>File uploaded: <a href={uploadedUrl}>{uploadedUrl}</a></p>}
        </div>
    );
};

export default FileUpload;
