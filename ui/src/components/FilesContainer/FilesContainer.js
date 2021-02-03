import React from "react";
import UploadedFile from "../UploadedFile";

const FilesContainer = ({ files, setFiles }) => {
  return (
    <div>
      {files.map((file, index) => (
        //  Custom component for each uploaded file
        <UploadedFile
          id={index}
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
