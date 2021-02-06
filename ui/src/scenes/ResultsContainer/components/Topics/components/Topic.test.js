import { render, screen } from "@testing-library/react";
import Topic from "./Topic";

test("should render topic without issue", () => {
  const defaultProps = {
    data: {
      topicnum: 1,
      coherence: "-0.0948517194431557",
      topicwords: [
        {
          word: "economy",
          weight: "0.019615816",
        },
        {
          word: "covid",
          weight: "0.011126553",
        },
        {
          word: "continues",
          weight: "0.0086657265",
        },
        {
          word: "study",
          weight: "0.008322413",
        },
        {
          word: "economics",
          weight: "0.007848377",
        },
      ],
    },
  };
  render(<Topic {...defaultProps} />);
  screen.getByTestId(`topic-section-${defaultProps.data.topicnum}`);
  screen.getByTestId(`topic-section-heading-${defaultProps.data.topicnum}`);
  screen.getByTestId(`topic-sub-heading-${defaultProps.data.topicnum}`);
  screen.getByTestId(`topic-coherence-${defaultProps.data.topicnum}`);
  screen.getByTestId(`words-grid-${defaultProps.data.topicnum}`);
});

test("should render word sections for corresponding data", () => {
  const defaultProps = {
    data: {
      topicnum: 1,
      coherence: "-0.0948517194431557",
      topicwords: [
        {
          word: "economy",
          weight: "0.019615816",
        },
        {
          word: "covid",
          weight: "0.011126553",
        },
        {
          word: "continues",
          weight: "0.0086657265",
        },
        {
          word: "study",
          weight: "0.008322413",
        },
        {
          word: "economics",
          weight: "0.007848377",
        },
      ],
    },
  };
  render(<Topic {...defaultProps} />);
  screen.getByTestId(`word-section-${defaultProps.data.topicnum}-${1}`);
  screen.getByTestId(`word-data-${defaultProps.data.topicnum}-${2}`);
  screen.getByTestId(`weight-section-${defaultProps.data.topicnum}-${3}`);
});
