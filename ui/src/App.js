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

const App = () => {
  const [files, setFiles] = useState();
  const [results, setResults] = useState();


  function useInput({ type }) {
    const [value, setValue] = useState("");
    const input = <Input name={"Number of Topics"} inputMode={"numeric"} value={value} onChange={e => setValue(e.target.value)} type={type} placeholder="Leave blank for default"/>;
    return [value, input];
  }

  const [numTopics, numTopicsInput] = useInput({type: "text", pattern:"[0-9]*"})

  const handleSubmit = () => {
    let formData = new FormData();
    formData.append("fileCount", files.length);
    files.forEach((file, index) => {
      formData.append(`file${index}`, file);
    });
    formData.append("numTopics", numTopics);
    Axios({
      url: "http://localhost:5000/upload",
      method: "POST",
      data: formData,
    }).then((response) => setResults(testResponse));
  };

  return (
    <div className="App">
      <h1>James</h1>
      <div className="main-content">
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
      {results ? (
        <div>These are the results: {`${results}`}</div>
      ) : (
        <div className="controls-container">
          {files &&
            files.map((file, index) => (
              <UploadedFile
                id={index}
                file={file}
                removeFile={() =>
                  setFiles(files.filter((file) => file !== files[index]))
                }
              />
            ))}

          <label >(Optional) Number of Topics: </label>
          {numTopicsInput}

          <br/>

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
