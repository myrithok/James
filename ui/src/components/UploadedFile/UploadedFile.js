import { Button } from "@material-ui/core";
import React from "react";
import "./styles.scss";

/*
  UploadedFile Component to handle each uploaded file
  State:
    file: Contains the text file uploaded
    removeFile: Contains a function to remove the file from the uploads
    id: Index of the file
 */

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
