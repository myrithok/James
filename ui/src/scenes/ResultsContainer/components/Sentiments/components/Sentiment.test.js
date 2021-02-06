import { render, screen } from "@testing-library/react";
import Sentiment from "./Sentiment";

const defaultProps = {
  data: {
    topicnum: 1,
    weight: 123,
    sentiment: 0.54534,
  },
};

const renderIt = (props = {}) =>
  render(<Sentiment {...defaultProps} {...props} />);

test("should render a sentiment section with the correct elements", () => {
  renderIt();
  screen.getByTestId("sentiment-row");
  screen.getByTestId("topic-num-1");
  screen.getByTestId("weight-1");
  screen.getByTestId("sentiment-score-1");
});

test("should render a sentiment section with the correct values", () => {
  renderIt();
  screen.getByText("1");
  screen.getByText("123");
  screen.getByText("0.54534");
});
