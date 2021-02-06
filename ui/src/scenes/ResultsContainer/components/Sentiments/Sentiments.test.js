import { render, screen } from "@testing-library/react";
import Sentiments from "./Sentiments";

const defaultProps = {
  sentiments: [
    {
      doctitle: "canadian-covid_economy",
      topics: [
        {
          topicnum: 6,
          weight: "0.00013250425",
          sentiment: "0.4664526623235231",
        },
        {
          topicnum: 12,
          weight: "0.9970626",
          sentiment: "0.4664740564311913",
        },
        {
          topicnum: 13,
          weight: "0.00012891214",
          sentiment: "0.46647680606424335",
        },
      ],
    },
    {
      doctitle: "dogs-boats",
      topics: [
        {
          topicnum: 3,
          weight: "0.00013914949",
          sentiment: "0.1989638616015134",
        },
        {
          topicnum: 4,
          weight: "0.0001449878",
          sentiment: "0.1989606636635585",
        },
        {
          topicnum: 8,
          weight: "0.9976317",
          sentiment: "0.19895441250913964",
        },
      ],
    },
  ],
};

test("should render Sentiments section with correct elements", () => {
  render(<Sentiments {...defaultProps} />);
  screen.getByTestId("sentiment-container");
  screen.getByTestId("sentiment-title");
});

test("should render Sentiments section with corrent values", () => {
  render(<Sentiments {...defaultProps} />);
  screen.getByTestId("sentiment-container");
  screen.getByTestId("sentiment-title");
  const sentimentSections = screen.getAllByTestId(/sentiment-section-\d$/);
  expect(sentimentSections.length).toEqual(2);
  const sentiments = screen.getAllByTestId(/sentiment-row$/);
  expect(sentiments.length).toEqual(6);
  screen.getByText("Document Title: dogs-boats");
  screen.getByText("Document Title: canadian-covid_economy");
});

test("should render Sentiments section with no data section", () => {
  render(<Sentiments sentiments={[]} />);
  screen.getByTestId("sentiment-container");
  screen.getByTestId("sentiment-title");

  screen.getByTestId("no-sentiment-data");
  screen.getByText("Sorry, no sentiments could be parsed from the document.");
  screen.getByText("Please upload a different document and try again.");
});
