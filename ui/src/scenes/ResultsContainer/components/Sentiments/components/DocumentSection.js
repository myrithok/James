import React from "react";
import Sentiment from "./Sentiment";

const SentimentGridHeadings = () => (
  <div className="sentiment-grid-headings">
    <div className="heading">Topic Number</div>
    <div className="heading">Weight</div>
    <div className="heading">Sentiment</div>
  </div>
);

const DocumentSection = ({ data }) => {
  const { doctitle, topics } = data;
  return (
    <div className="sentiment-section">
      <div className="sentiment-section-heading">
        <h3 className="sentiment-sub-heading">{`Document Title: ${doctitle}`}</h3>
      </div>
      <div className="sentiment-grid">
        <SentimentGridHeadings />
        {topics.map((topic) => (
          <Sentiment data={topic} />
        ))}
      </div>
    </div>
  );
};

export default DocumentSection;
