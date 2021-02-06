import { render, screen } from "@testing-library/react";
import FilesContainer from "./FilesContainer";

const defaultProps = {
  files: [
    {
      size: 123123123,
      name: "test-name.txt",
    },
    {
      size: 123123123,
      name: "different-test-name.txt",
    },
  ],
};

test("should render file container with correct elements", () => {
  render(<FilesContainer {...defaultProps} />);
  screen.getByTestId("files-container");
});

test("should render with correct values", () => {
  render(<FilesContainer {...defaultProps} />);
  screen.getByText("File 0: test-name.txt [123123.1KB]");
  screen.getByText("File 1: different-test-name.txt [123123.1KB]");
  screen.getByTestId("remove-btn-0");
  screen.getByTestId("remove-btn-1");
});
