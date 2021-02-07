import { render, screen } from "@testing-library/react";
import DocumentSection from "./DocumentSection";

const defaultProps = {
  data: {
    doctitle: "canadian-covid_economy",
    topics: [
      {
        topicnum: 5,
        weight: "0.0001271892",
        sentiment: "0.4664622149561388",
      },
      {
        topicnum: 18,
        weight: "0.00089594617",
        sentiment: "0.4664821888273987",
      },
    ],
  },
  id: 1,
};

test("should render Doc section with correct elements", () => {
  render(<DocumentSection {...defaultProps} />);
  screen.getByTestId("sentiment-section-1");
  screen.getByTestId("sentiment-section-heading-1");
  screen.getByTestId("sentiment-section-heading-1");
  screen.getByTestId("sentiment-sub-heading-1");
  screen.getByTestId("sentiment-grid-1");
  const sentRows = screen.getAllByTestId("sentiment-row");
  expect(sentRows.length).toEqual(2);
});

test("should render Doc section with correct values", () => {
  render(<DocumentSection {...defaultProps} />);
  screen.getByText("Document Title: canadian-covid_economy");
  screen.getByText("5");
  screen.getByText("0.0001271892");
  screen.getByText("0.4664622149561388");
  screen.getByText("18");
  screen.getByText("0.00089594617");
  screen.getByText("0.4664821888273987");
});

test("should render Doc section with no data display", () => {
  render(
    <DocumentSection
      data={{ doctitle: "canadian-covid_economy", topics: [] }}
      id={1}
    />
  );
  screen.getByTestId("sentiment-section-1");
  screen.getByTestId("sentiment-section-heading-1");
  screen.getByTestId("sentiment-section-heading-1");
  screen.getByTestId("sentiment-sub-heading-1");
  screen.getByTestId("sentiment-grid-1");
  screen.getByTestId("no-sentiment-data-1");
  screen.getByText("Sorry, no sentiments could be parsed from the document.");
  screen.getByText("Please upload a different document and try again.");
  expect(screen.queryByTestId("sentiment-row")).not.toBeInTheDocument();
});
