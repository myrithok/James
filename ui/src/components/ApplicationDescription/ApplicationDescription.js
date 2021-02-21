import React from "react";
import { descriptionText } from "../../resources";

const ApplicationDescription = () => {
  return (
    <div className="description-container" data-testid="description-container">
      <h4>James Description</h4>
      <p>{descriptionText}</p>
    </div>
  );
};

export default ApplicationDescription;
