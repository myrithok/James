import "./App.scss";
import Dropzone from "react-dropzone";
import { useState } from "react";
import UploadedFile from "./components/UploadedFile";
import { Button, Input } from "@material-ui/core";
import { isEmpty } from "lodash";
import Axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloudDownloadAlt } from "@fortawesome/free-solid-svg-icons";
import { fillerText, testResponse } from "./resources";

/*
  App contains the code for the main page of the application, using the custom component UploadedFile
  Using React Hooks to manage state:
    files: Contains all of the text files uploaded
    results: Contains the results obtained from running the ML model on the input files
    numTopics: An optional numeric value, allowing user to specify how many topics there are in the input files. Default value of "".
*/

const App = () => {
  //State Variables
  const [files, setFiles] = useState();
  const [results, setResults] = useState();
  const [numTopics, numTopicsInput] = useInput({type: "number", placeholder: "Leave blank for default"})

  //Reusable function to handle input from user in a text box
  function useInput({ type, placeholder }) {
    const [value, setValue] = useState("");
    const input = <Input inputMode={"numeric"} value={value} onChange={e => setValue(e.target.value)} type={type} placeholder={placeholder}/>;
    return [value, input];
  }
/*
  Function to handle the submission, accessed by the "Calculate" button
  Data is submitted as a FormData object, as a POST request to the Flask backend server, hosted at http://localhost:5000/upload
  formData contains the number of files, the number of topics, and each file labeled by its index
  The response is the results from running the topic modeling and sentiment analysis algorithms on the input files
*/

  const handleSubmit = () => {
    let formData = new FormData();
    formData.append("fileCount", files.length);
    formData.append("numTopics", numTopics);
    files.forEach((file, index) => {
      formData.append(`file${index}`, file);
    });
    Axios({
      url: "http://localhost:5000/upload",
      method: "POST",
      data: formData,
    }).then((response) => setResults(response));
  };

  return (
    <div className="App">
      <h1>James</h1>
      <div className="main-content">
        {/*
          Dropzone is used to allow the user to "drop" text files into the area, or select them from their drive
          Once received, the files are added to the state variable "files"
        */}
        <Dropzone onDrop={(acceptedFiles) => setFiles(acceptedFiles)} multiple>
          {({ getRootProps, getInputProps }) => (
            <div className="drop-zone" {...getRootProps()}>
              <input {...getInputProps()} />
              <FontAwesomeIcon icon={faCloudDownloadAlt} size="3x" />
              <p className="file-drop-instructions">
                Drop files or click here to select files from your drive
              </p>
            </div>
          )}
        </Dropzone>
      </div>
      {/*
        Results are outputted here in JSON, once received
      */}
      {results ? (
        <div className="results-container">
          These are the results:
          <pre>{`${JSON.stringify(results, null, 3)}`}</pre>
          <Button
              variant="contained"
              color="primary"
              onClick={() =>  window.location.reload(false)}
          >
            Start Over
          </Button>
        </div>
      ) : (
        <div className="controls-container">

          {/*
             Optional input field to input number of topics
          */}
          <label className="numTopicsPrompt">(Optional) Number of Topics: </label>
          {numTopicsInput}

          <br/>

          {files &&
            files.map((file, index) => (
              //  Custom component for each uploaded file
              <UploadedFile
                id={index}
                file={file}
                removeFile={() =>
                  setFiles(files.filter((file) => file !== files[index]))
                }
              />
            ))}

          {/*
              Button to submit files and send REST request to backend
          */}
          <Button
              variant="contained"
              color="primary"
              disabled={isEmpty(files)}
              onClick={() => handleSubmit()}
          >
            Calculate
          </Button>
        </div>
      )}
      <div className="description-container">
        <h4>Super Awesome Description</h4>
        <p>{fillerText}</p>
      </div>
    </div>
  );
};

export default App;
