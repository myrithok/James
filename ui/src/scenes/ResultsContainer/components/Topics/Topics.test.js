import { render, screen } from "@testing-library/react";
import Topics from "./Topics";

const defaultProps = {
  topics: [
    {
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
      ],
    },
    {
      topicnum: 2,
      coherence: "-0.0948517194431123",
      topicwords: [
        {
          word: "test",
          weight: "0.019615816",
        },
        {
          word: "this",
          weight: "0.011126553",
        },
        {
          word: "testing",
          weight: "0.0086657265",
        },
      ],
    },
  ],
};

test("should render Topics section without issue", () => {
  render(<Topics {...defaultProps} />);
  screen.getByTestId("topic-container");
  screen.getByTestId("topic-title");
});

test("should render wordsection without issue", () => {
  render(<Topics {...defaultProps} />);
  screen.getByTestId(`topic-section-${1}`);
  screen.getByTestId(`topic-section-heading-${2}`);
  screen.getByTestId(`topic-sub-heading-${2}`);
  screen.getByTestId(`topic-coherence-${1}`);
  screen.getByTestId(`words-grid-${1}`);
});

test("should render topic without issue", () => {
  render(<Topics {...defaultProps} />);
  screen.getByTestId(`word-data-${1}-${1}`);
  screen.getByTestId(`weight-section-${2}-${2}`);
  screen.getByText("economy");
  screen.getByText("covid");
});
