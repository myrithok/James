import React from "react";
import { Button } from "@material-ui/core";
import WordSection from "./WordSection";
import SentenceSection from "./SentenceSection";

const Topic = ({ data, toggleHide, hiddenTopics }) => {
  const { topicnum, coherence, topicwords, examplesentences } = data;
  const hideTopic = hiddenTopics.includes(topicnum);
  return hideTopic ? (
    <div className="topic-section" data-testid={`topic-section-${topicnum}`}>
      <div
        className="topic-section-heading"
        data-testid={`topic-section-heading-${topicnum}`}
      >
        <h3
          className="topic-sub-heading"
          data-testid={`topic-sub-heading-${topicnum}`}
        >{`Topic ${topicnum}`}</h3>
        <Button
          onClick={() => toggleHide(topicnum)}
          variant="contained"
          color="primary"
        >
          Show this topic
        </Button>
      </div>
    </div>
  ) : (
    <div className="topic-section" data-testid={`topic-section-${topicnum}`}>
      <div
        className="topic-section-heading"
        data-testid={`topic-section-heading-${topicnum}`}
      >
        <h3
          className="topic-sub-heading"
          data-testid={`topic-sub-heading-${topicnum}`}
        >{`Topic ${topicnum}`}</h3>
        <Button
          onClick={() => toggleHide(topicnum)}
          variant="contained"
          color="primary"
        >
          Hide this topic
        </Button>
        <div
          className="topic-coherence"
          data-testid={`topic-coherence-${topicnum}`}
        >{`Coherence: ${coherence}`}</div>
      </div>
      <div className="words-grid" data-testid={`words-grid-${topicnum}`}>
        {topicwords.map((word, index) => (
          <WordSection
            data={word}
            topicId={topicnum}
            wordId={index}
            key={index}
          />
        ))}
      </div>
      <div className="sentence-grid">
        <div className="sentence-title">Example sentences:</div>
        {examplesentences.map((sentence, index) => (
          <SentenceSection
            data={sentence}
            topicId={topicnum}
            sentenceId={index}
            key={index}
          />
        ))}
      </div>
    </div>
  );
};

export default Topic;
