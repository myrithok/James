import React from "react";
import Topic from "./components/Topic";
import "./styles.scss";

const Topics = ({ topics }) => {
  return (
    <div className="topic-container">
      <h2 className="topics-title">Topics</h2>
      {topics.map((topic) => (
        <Topic data={topic} />
      ))}
    </div>
  );
};

export default Topics;
