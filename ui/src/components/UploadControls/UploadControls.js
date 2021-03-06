import { Button } from "@material-ui/core";
import { isEmpty } from "lodash";
import React from "react";
import FilesContainer from "../FilesContainer";
import CircularProgress from "@material-ui/core/CircularProgress";

const UploadControls = ({
  numTopicsInput,
  numTopics,
  datasetSelect,
  datasetChoice,
  files,
  setFiles,
  handleSubmit,
  loading,
}) => {
  const isNumTopicsInvalid =
    numTopics < 1 || numTopics > 200 || numTopics % 1 !== 0;

  return (
    <div className="controls-container">
      {/*
             Optional input field to input number of topics
          */}
      {loading ? (
        <div className="loading-container">
          Processing! This may take a few minutes...
          <br /> <br />
          <CircularProgress data-testid="loader" />
          <br /> <br />
          <Button
            variant="contained"
            color="primary"
            onClick={() => window.location.reload(false)}
            className="loading-cancel-btn"
          >
            Cancel
          </Button>
        </div>
      ) : (
        <>
          <label className="numTopicsPrompt" data-testid="num-topics-prompt">
            Number of Topics:&nbsp;
          </label>
          {numTopicsInput}
          <br />
          <div className="topic-num-restriction">
            *Number of topics must be an integer between 1 and 200
          </div>
          <label className="datasetPrompt">
            Sentiment Dataset:&nbsp;
          </label>
          {datasetSelect}
          <br />
          {files && <FilesContainer files={files} setFiles={setFiles} />}
          {/*
              Button to submit files and send REST request to backend
            */}
          <Button
            variant="contained"
            color="primary"
            disabled={isEmpty(files) || isNumTopicsInvalid}
            onClick={handleSubmit}
            data-testid="submit-btn"
          >
            Calculate
          </Button>

        </>
      )}
    </div>
  );
};

export default UploadControls;
