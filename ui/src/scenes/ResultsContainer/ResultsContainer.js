import React from "react";
import { Button } from "@material-ui/core";
import ScrollToTop from "react-scroll-up";
import Topics from "./components/Topics";
import Sentiments from "./components/Sentiments";

const ResultsContainer = ({
  topics,
  sentiments,
  handleDownload,
  hiddenTopics,
  modelCoherence,
  toggleHide,
}) => {
  return (
    <div className="results-container">
      <h2 className="results-title">
      Results
      </h2>
      <div className="results-buttons">
        <Button
          variant="contained"
          color="primary"
          onClick={() => window.location.reload(false)}
          className="results-reset-btn"
          data-testid="results-reset-btn"
        >
          Reset
        </Button>
        &nbsp;&nbsp;
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
      <br />
      <Topics
        topics={topics}
        hiddenTopics={hiddenTopics}
        toggleHide={toggleHide}
        modelCoherence={modelCoherence}
      />
      <Sentiments sentiments={sentiments} hiddenTopics={hiddenTopics} />
      <ScrollToTop showUnder={0} duration={1000} >
        <Button
          variant="contained"
          color="primary"
          className="results-top-btn"
        >
          Back to Top
        </Button>
      </ScrollToTop>
    </div>
  );
};

export default ResultsContainer;
