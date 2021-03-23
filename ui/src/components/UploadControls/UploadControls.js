import { Button } from "@material-ui/core";
import { isEmpty } from "lodash";
import React from "react";
import FilesContainer from "../FilesContainer";
import CircularProgress from "@material-ui/core/CircularProgress";

const UploadControls = ({
  numTopicsInput,
  files,
  setFiles,
  handleSubmit,
  loading,
}) => {
  return (
    <div className="controls-container">
      {/*
             Optional input field to input number of topics
          */}
      {loading ? (
        <CircularProgress data-testid="loader" />
      ) : (
        <>
          <label className="numTopicsPrompt" data-testid="num-topics-prompt">
            (Optional) Number of Topics:&nbsp;
          </label>
          {numTopicsInput}
          <br />
          {files && <FilesContainer files={files} setFiles={setFiles} />}
          {/*
              Button to submit files and send REST request to backend
          */}
          <Button
            variant="contained"
            color="primary"
            disabled={isEmpty(files)}
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
