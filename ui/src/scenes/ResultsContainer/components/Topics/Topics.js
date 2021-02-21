import React from "react";
import Topic from "./components/Topic";
import "./styles.css";

const Topics = ({ topics }) => {
  return (
    <div className="topic-container" data-testid="topic-container">
      <h2 className="topics-title" data-testid="topic-title">
        Topics
      </h2>
      {topics.map((topic, index) => (
        <Topic data={topic} id={index} />
      ))}
    </div>
  );
};

export default Topics;
