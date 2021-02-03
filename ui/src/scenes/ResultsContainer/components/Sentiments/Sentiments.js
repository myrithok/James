import React from "react";
import DocumentSection from "./components/DocumentSection";
import "./styles.scss";

const Sentiments = ({ sentiments }) => {
  return (
    <div className="sentiment-container">
      <h2 className="sentiment-title">Sentiments</h2>
      {sentiments.map((sentiment) => (
        <DocumentSection data={sentiment} />
      ))}
    </div>
  );
};

export default Sentiments;
