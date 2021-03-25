import React from "react";

const SentenceSection = ({ data, topicId, sentenceId }) => {
  const { sentence, weight } = data;
  return (
    <div
      className="sentence-section"
    >
      <div className="sentence-data">
        {sentence}
      </div>
      <div className="sentenceweight-data">
        Topic weight: {weight}
      </div>
    </div>
  );
};

export default SentenceSection;
