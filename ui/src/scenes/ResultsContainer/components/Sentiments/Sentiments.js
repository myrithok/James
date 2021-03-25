import React from "react";
import DocumentSection from "./components/DocumentSection";
import "./styles.css";

const Sentiments = ({ sentiments, hiddenTopics }) => {
  return (
    <div className="sentiment-container" data-testid="sentiment-container">
      <h2 className="sentiment-title" data-testid="sentiment-title">
        Sentiments
      </h2>
      {sentiments.length === 0 ? (
        <div data-testid={`no-sentiment-data`}>
          <div>Sorry, no sentiments could be parsed from the document.</div>
          <div>Please upload a different document and try again.</div>
        </div>
      ) : (
        sentiments.map((sentiment, index) => (
          <DocumentSection
            data={sentiment}
            id={index}
            key={index}
            hiddenTopics={hiddenTopics}
          />
        ))
      )}
    </div>
  );
};

export default Sentiments;
