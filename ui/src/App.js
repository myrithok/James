import React, { useCallback, useState } from "react";
import Axios from "axios";
import FileDownload from "js-file-download";
import { Input } from "@material-ui/core";
import ResultsContainer from "./scenes/ResultsContainer/ResultsContainer";
import ApplicationDescription from "./components/ApplicationDescription/ApplicationDescription";
import UploadControls from "./components/UploadControls/UploadControls";
import FileDrop from "./components/FileDrop";
import "./App.css";

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
  const [hiddenTopics, setHiddenTopics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [numTopics, numTopicsInput] = useInput({
    type: "number",
  });

  const handleToggleHide = (topicId) => {
    if (hiddenTopics.includes(topicId)) {
      const newTopics = hiddenTopics.filter((topic) => topic !== topicId);
      setHiddenTopics(newTopics);
    } else {
      setHiddenTopics([...hiddenTopics, topicId]);
    }
  };

  //Reusable function to handle input from user in a text box
  function useInput({ type }) {
    const [value, setValue] = useState("");
    const input = (
      <Input
        inputMode={"numeric"}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        type={type}
        inputProps={{ min: 1, max: 100 }}
      />
    );
    return [value, input];
  }
  /*
  Function to handle the submission, accessed by the "Calculate" button
  Data is submitted as a FormData object, as a POST request to the Flask backend server, hosted at http://localhost:5000/upload
  formData contains the number of files, the number of topics, and each file labeled by its index
  The response is the results from running the topic modeling and sentiment analysis algorithms on the input files
*/

  const handleSubmit = useCallback(() => {
    setLoading(true);
    let formData = new FormData();
    formData.append("fileCount", files.length);
    formData.append("numTopics", numTopics);
    files.forEach((file, index) => {
      formData.append(`file${index}`, file);
    });
    Axios({
      url: "http://35.183.97.235:8002/upload",
      method: "POST",
      data: formData,
    })
      .then((response) => {
        setResults(response.data);
        setLoading(true);
      })
      .catch((error) => console.log(error));
  }, [files, numTopics]);

  const handleDownload = useCallback(() => {
    let formData = new FormData();
    formData.append("results", JSON.stringify(results));
    formData.append("hiddenTopics", JSON.stringify(hiddenTopics));
    Axios({
      url: "http://35.183.97.235:8002/download",
      method: "POST",
      data: formData,
    }).then((response) => {
      FileDownload(response.data, "report.csv");
    });
  }, [results, hiddenTopics]);

  return (
    <div className="App">
      <h1>James</h1>
      <div className="main-content">
        {/*
          Dropzone is used to allow the user to "drop" text files into the area, or select them from their drive
          Once received, the files are added to the state variable "files"
        */}
        {!results && <FileDrop setFiles={setFiles} loading={loading} />}
      </div>
      {/*
        Results are outputted here in JSON, once received
      */}
      {results && (
        <ResultsContainer
          topics={results.topics}
          sentiments={results.sentiments}
          handleDownload={handleDownload}
          hiddenTopics={hiddenTopics}
          toggleHide={handleToggleHide}
        />
      )}
      {!results && (
        <UploadControls
          numTopicsInput={numTopicsInput}
          numTopics={numTopics}
          files={files}
          setFiles={setFiles}
          handleSubmit={handleSubmit}
          loading={loading}
        />
      )}
      {!results && <ApplicationDescription />}
    </div>
  );
};

export default App;
