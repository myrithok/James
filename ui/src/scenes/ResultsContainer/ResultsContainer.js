import React from "react";
import { Button } from "@material-ui/core";
import Topics from "./components/Topics";
import Sentiments from "./components/Sentiments";

const ResultsContainer = ({
  topics,
  sentiments,
  handleDownload,
  hiddenTopics,
  toggleHide,
}) => {
  return (
    <div className="results-container">
      <Topics
        topics={topics}
        hiddenTopics={hiddenTopics}
        toggleHide={toggleHide}
      />
      <Sentiments sentiments={sentiments} hiddenTopics={hiddenTopics} />
      <div className="results-footer">
        <Button
          variant="contained"
          color="primary"
          onClick={() => window.location.reload(false)}
          className="results-reset-btn"
          data-testid="results-reset-btn"
        >
          Reset
        </Button>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleDownload()}
          className="results-reset-btn"
          data-testid="results-reset-btn"
        >
          Download Results
        </Button>
      </div>
    </div>
  );
};

export default ResultsContainer;
