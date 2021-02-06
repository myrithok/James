import React from "react";
import WordSection from "./WordSection";

const Topic = ({ data }) => {
  const { topicnum, coherence, topicwords } = data;
  return (
    <div className="topic-section" data-testid={`topic-section-${topicnum}`}>
      <div
        className="topic-section-heading"
        data-testid={`topic-section-heading-${topicnum}`}
      >
        <h3
          className="topic-sub-heading"
          data-testid={`topic-sub-heading-${topicnum}`}
        >{`Topic Number: ${topicnum}`}</h3>
        <div
          className="topic-coherence"
          data-testid={`topic-coherence-${topicnum}`}
        >{`Coherence: ${coherence}`}</div>
      </div>
      <div className="words-grid" data-testid={`words-grid-${topicnum}`}>
        {topicwords.map((word, index) => (
          <WordSection data={word} topicId={topicnum} wordId={index} />
        ))}
      </div>
    </div>
  );
};

export default Topic;
