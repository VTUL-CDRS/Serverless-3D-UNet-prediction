import React, { useState } from 'react';
import { Storage } from '@aws-amplify/storage';
import './App.css';
import { withAuthenticator, Button } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';


function App({ signOut, user }) {

  const [file, setFile] = useState(null);
  const [images, setImages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [fileContents, setFileContents] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);

  const listImageClick = async () => {
    setIsLoading(true);
    try {
      const result = await Storage.list('results/');
      setImages(result);
      setIsLoading(false);
    }
    catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };


  async function getImageURL(filename) {
    try {
      const fileurl = await Storage.get(filename, {
        level: "public"
      });
      setFileContents(fileurl);
    }
    catch (error) {
      console.error(error);
    }
  };

  function handleFileChange(event) {
    setFile(event.target.files[0]);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      setUploadStatus('File uploading...');
      await Storage.put(file.name, file);
      setUploadStatus('File uploaded.');
    }
    catch (error) {
      console.error(error);
    }
  }


  return (
    <div style={styles.container}>

      <h1>3D Medical Imaging Segmentation</h1>

      <h3>User: {user.username}</h3>

      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>

      {uploadStatus}

      <p>
        <button type="submit" onClick={listImageClick}>Show files</button>
      </p>

      {isLoading ? <p>Loading...</p> : (
        <div>
          {Array.isArray(images.results) ? images.results.filter(file => file.key !== 'results/').map(file => (
            <p>{file.key} &nbsp;&nbsp; {Array.isArray(getImageURL(file.key))}
              <a href={fileContents} target="_blank" rel='noreferrer' download> Download </a>
            </p>
          )) : null}

        </div>
      )}

      <br />
      <br />


      <Button style={styles.button} onClick={signOut}>Sign out</Button>
    </div>
  );

}

const styles = {
  container: {
    width: 600,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    padding: 20,
  },
  hr: { width: "100%", border: "1px solid black" },
  input: {
    border: "none",
    backgroundColor: "#ddd",
    marginBottom: 10,
    padding: 8,
    fontSize: 18,
  },
  button: {
    backgroundColor: "black",
    color: "white",
    outline: "none",
    fontSize: 16,
    padding: "6px 0px",
    width: "30%",
  },
};

export default withAuthenticator(App);
