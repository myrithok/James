import React from "react";

const WordSection = ({ data }) => {
  const { word, weight } = data;
  return (
    <div className="word-section">
      <div className="word-data">{word}</div>
      <div className="weight-data">{weight}</div>
    </div>
  );
};

export default WordSection;
