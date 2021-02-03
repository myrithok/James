import React from "react";
import WordSection from "./WordSection";

const Topic = ({ data }) => {
  const { topicnum, coherence, topicwords } = data;
  return (
    <div className="topic-section">
      <div className="topic-section-heading">
        <h3 className="topic-sub-heading">{`Topic Number: ${topicnum}`}</h3>
        <div className="topic-coherence">{`Coherence: ${coherence}`}</div>
      </div>
      <div className="words-grid">
        {topicwords.map((word) => (
          <WordSection data={word} />
        ))}
      </div>
    </div>
  );
};

export default Topic;
