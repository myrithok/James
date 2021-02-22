import React from "react";
import { descriptionText, bugText } from "../../resources";

const ApplicationDescription = () => {
  return (
    <div className="description-container" data-testid="description-container">
      <h4>Welcome to James</h4>
      <p>{descriptionText}</p>
      <h4>Help up improve</h4>
      <p>{bugText}</p>
      <a href="https://github.com/myrithok/James/issues">here</a>
    </div>
  );
};

export default ApplicationDescription;
