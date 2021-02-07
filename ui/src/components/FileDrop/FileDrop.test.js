import { render, screen } from "@testing-library/react";
import FileDrop from "./FileDrop";

test("should render filedrop with correct elements", () => {
  render(<FileDrop />);
  screen.getByTestId("drop-zone");
  screen.getByTestId("file-drop-icon");
  screen.getByText("Drop files or click here to select files from your drive");
});
