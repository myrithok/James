import { render, screen } from "@testing-library/react";
import WordSection from "./WordSection";

test("should render wordsection without issue", () => {
  const defaultProps = {
    data: {
      word: "Test",
      weight: 0.2154,
    },
    topicId: 1,
    wordId: 3,
  };
  render(<WordSection {...defaultProps} />);
  screen.getByTestId(
    `word-section-${defaultProps.topicId}-${defaultProps.wordId}`
  );
  screen.getByTestId(
    `word-data-${defaultProps.topicId}-${defaultProps.wordId}`
  );
  screen.getByTestId(
    `weight-section-${defaultProps.topicId}-${defaultProps.wordId}`
  );
  screen.getByText("Test");
  screen.getByText("0.2154");
});
