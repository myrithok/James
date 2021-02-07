import { fireEvent, render, screen } from "@testing-library/react";
import UploadControls from "./UploadControls";

const props = {
  numTopicsInput: "",
  file: {
    size: 123123123,
    name: "test-name.txt",
  },
};

test("Should render without issue", () => {
  render(<UploadControls {...props} />);
  screen.getByTestId("num-topics-prompt");
  screen.getByTestId("submit-btn");
});

test("Should render loading state", () => {
  render(<UploadControls loading />);
  screen.getByTestId(`loader`);
});

test("Should call handleSubmit on click", () => {
  const handleSubmit = jest.fn();
  render(<UploadControls {...props} handleSubmit={handleSubmit()} />);
  screen.getByTestId("num-topics-prompt");
  const subBtn = screen.getByTestId("submit-btn");
  fireEvent.click(subBtn);
  expect(handleSubmit).toHaveBeenCalled();
});
