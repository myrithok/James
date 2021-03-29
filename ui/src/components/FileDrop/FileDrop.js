import React from "react";
import Dropzone from "react-dropzone";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloudDownloadAlt } from "@fortawesome/free-solid-svg-icons";

const FileDrop = ({ setFiles, loading }) => {
  return (
    <Dropzone
      onDrop={(acceptedFiles) => setFiles(acceptedFiles)}
      multiple
      disabled={loading}
    >
      {({ getRootProps, getInputProps }) => (
        <div className="drop-zone" data-testid="drop-zone" {...getRootProps()}>
          <input {...getInputProps()} />
          <FontAwesomeIcon
            icon={faCloudDownloadAlt}
            size="3x"
            data-testid="file-drop-icon"
          />
          <p className="file-drop-instructions">
            Drop files or click here to select files from your drive
          </p>
        </div>
      )}
    </Dropzone>
  );
};

export default FileDrop;
