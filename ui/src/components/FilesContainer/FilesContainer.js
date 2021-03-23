import React from "react";
import UploadedFile from "../UploadedFile";

const FilesContainer = ({ files, setFiles }) => {
  return (
    <div data-testid="files-container">
      {files.map((file, index) => (
        //  Custom component for each uploaded file
        <UploadedFile
          id={index + 1}
          key={index + 1}
          file={file}
          removeFile={() =>
            setFiles(files.filter((file) => file !== files[index]))
          }
        />
      ))}
    </div>
  );
};

export default FilesContainer;
