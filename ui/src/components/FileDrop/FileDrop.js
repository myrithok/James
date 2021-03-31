import React from "react";
import Dropzone from "react-dropzone";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCloudDownloadAlt } from "@fortawesome/free-solid-svg-icons";
import "./styles.css";

const FileDrop = ({ setFiles, loading }) => {
  const maxSize = 5242880;
  return (
    <Dropzone
      onDrop={(acceptedFiles) => setFiles(acceptedFiles)}
      accept="text/plain"
      minSize={1}
      maxSize={maxSize}
      multiple
      disabled={loading}
    >
      {({ getRootProps, getInputProps, acceptedFiles, isDragReject, fileRejections}) => {
        let fileTooLarge = false;
        let fileTooSmall = false;
        let fileTypeInvalid = false;
        if (fileRejections.length > 0) {
          let fileSize = fileRejections[0].file.size;
          fileTooLarge = fileSize > maxSize
          fileTooSmall = fileSize===0
          fileTypeInvalid = !fileTooLarge && !fileTooSmall
        }

        return(
          <div className="drop-zone" data-testid="drop-zone" {...getRootProps()}>
          <input {...getInputProps()} />

            <FontAwesomeIcon
            icon={faCloudDownloadAlt}
            size="3x"
            data-testid="file-drop-icon"
          />
            {fileTooLarge && (
                <p className="errorText">
                  File is too large. Maximum size is 5MB
                </p>
            )}
            {fileTooSmall && (
                <p className="errorText">
                  File is empty
                </p>
              )}
            {(fileTypeInvalid || isDragReject) && (
                <p className="errorText">
                  Please upload a plain text file (.txt)
                </p>
            )}
            {!fileTooSmall && !fileTooLarge && !fileTypeInvalid && !isDragReject && (
                <p className="infoText">
                  Drop files or click here to select files from your drive
                </p>
            )}


        </div>
      )}
      }
    </Dropzone>
  );
};

export default FileDrop;
