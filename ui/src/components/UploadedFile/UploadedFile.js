import { Button } from "@material-ui/core";
import React from "react";
import "./styles.scss";

const UploadedFile = ({ file = {}, removeFile, id }) => (
  <div className="uploaded-file-container">
    {file.name ? (
      <>
        <div className="file-name">{`File ${id}: ${file.name} [${(
          file.size / 1000
        ).toFixed(1)}KB]`}</div>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => removeFile()}
          className="remove-btn"
        >
          Remove
        </Button>
      </>
    ) : null}
  </div>
);

export default UploadedFile;
