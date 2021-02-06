import React from "react";
import Sentiment from "./Sentiment";

const SentimentGridHeadings = () => (
  <div className="sentiment-grid-headings">
    <div className="heading">Topic Number</div>
    <div className="heading">Weight</div>
    <div className="heading">Sentiment</div>
  </div>
);

const DocumentSection = ({ data, id }) => {
  const { doctitle, topics } = data;
  return (
    <div className="sentiment-section" data-testid={`sentiment-section-${id}`}>
      <div
        className="sentiment-section-heading"
        data-testid={`sentiment-section-heading-${id}`}
      >
        <h3
          className="sentiment-sub-heading"
          data-testid={`sentiment-sub-heading-${id}`}
        >{`Document Title: ${doctitle}`}</h3>
      </div>
      <div className="sentiment-grid" data-testid={`sentiment-grid-${id}`}>
        <SentimentGridHeadings />
        {topics.length === 0 ? (
          <div data-testid={`no-sentiment-data-${id}`}>
            <div>Sorry, no sentiments could be parsed from the document.</div>
            <div>Please upload a different document and try again.</div>
          </div>
        ) : (
          topics.map((topic) => <Sentiment data={topic} />)
        )}
      </div>
    </div>
  );
};

export default DocumentSection;
