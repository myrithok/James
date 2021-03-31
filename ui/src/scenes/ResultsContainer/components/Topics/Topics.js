import React from "react";
import Topic from "./components/Topic";
import "./styles.css";

const Topics = ({ topics, toggleHide, hiddenTopics, modelCoherence }) => {
  return (
    <div className="topic-container" data-testid="topic-container">
      <h2 className="topic-title" data-testid="topic-title">
        Topics
      </h2>
      <div className="model-coherence">
        Topic Model Coherence = {modelCoherence}
      </div>
      {topics.map((topic, index) => (
        <Topic
          data={topic}
          id={index}
          key={index}
          toggleHide={toggleHide}
          hiddenTopics={hiddenTopics}
        />
      ))}
    </div>
  );
};

export default Topics;
