import React from "react";
import { Button } from "@material-ui/core";
import Topics from "./components/Topics";
import Sentiments from "./components/Sentiments";

const ResultsContainer = ({ topics, sentiments, handleDownload }) => {
  return (
    <div className="results-container">
      <Topics topics={topics} />
      <Sentiments sentiments={sentiments} />
      <div className="results-footer">
        <Button
          variant="contained"
          color="primary"
          onClick={() => window.location.reload(false)}
          className="results-reset-btn"
          data-testId="results-reset-btn"
        >
          Reset
        </Button>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleDownload()}
          className="results-reset-btn"
          data-testId="results-reset-btn"
        >
          Download Results
        </Button>
      </div>
    </div>
  );
};

export default ResultsContainer;
