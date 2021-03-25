import React from "react";

const Sentiment = ({ data: { topicnum, weight, sentiment }, hiddenTopics }) =>
  hiddenTopics.includes(topicnum) ? null : (
    <div className="sentiment-row" data-testid="sentiment-row">
      <div className="cell" data-testid={`topic-num-${topicnum}`}>
        {topicnum}
      </div>
      <div className="cell" data-testid={`weight-${topicnum}`}>
        {weight}
      </div>
      <div className="cell" data-testid={`sentiment-score-${topicnum}`}>
        {sentiment}
      </div>
    </div>
  );

export default Sentiment;
