import React from "react";

const WordSection = ({ data, topicId, wordId }) => {
  const { word, stem, weight } = data;
  return (
    <div
      className="word-section"
      data-testid={`word-section-${topicId}-${wordId}`}
    >
      <div className="word-data" data-testid={`word-data-${topicId}-${wordId}`}>
        {word}
      </div>
      <div className="stem-data">
        stem: {stem}
      </div>
      <div
        className="weight-data"
        data-testid={`weight-section-${topicId}-${wordId}`}
      >
        {weight}
      </div>
    </div>
  );
};

export default WordSection;
