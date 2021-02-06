import { useCallback, useState } from "react";
import Axios from "axios";
import { Input } from "@material-ui/core";
import ResultsContainer from "./scenes/ResultsContainer/ResultsContainer";
import ApplicationDescription from "./components/ApplicationDescription/ApplicationDescription";
import UploadControls from "./components/UploadControls/UploadControls";
import FileDrop from "./components/FileDrop";
import "./App.scss";

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
  const [loading, setLoading] = useState(false);
  const [numTopics, numTopicsInput] = useInput({
    type: "number",
    placeholder: "Leave blank for default",
  });

  //Reusable function to handle input from user in a text box
  function useInput({ type, placeholder }) {
    const [value, setValue] = useState("");
    const input = (
      <Input
        inputMode={"numeric"}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        type={type}
        placeholder={placeholder}
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
      url: "http://localhost:5000/upload",
      method: "POST",
      data: formData,
    })
      .then((response) => {
        setResults(response.data);
        setLoading(true);
      })
      .catch((error) => console.log(error));
  }, [files, numTopics]);

  return (
    <div className="App">
      <h1>James</h1>
      <div className="main-content">
        {/*
          Dropzone is used to allow the user to "drop" text files into the area, or select them from their drive
          Once received, the files are added to the state variable "files"
        */}
        {!results && <FileDrop setFiles={setFiles} />}
      </div>
      {/*
        Results are outputted here in JSON, once received
      */}
      {results && (
        <ResultsContainer
          topics={results.topics}
          sentiments={results.sentiments}
        />
      )}
      {!results && (
        <UploadControls
          numTopicsInput={numTopicsInput}
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
