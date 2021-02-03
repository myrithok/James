import React from "react";

const Sentiment = ({ data }) => {
  const { topicnum, weight, sentiment } = data;
  return (
    <div className="sentiment-row">
      <div className="cell">{topicnum}</div>
      <div className="cell">{weight}</div>
      <div className="cell">{sentiment}</div>
    </div>
  );
};

export default Sentiment;
