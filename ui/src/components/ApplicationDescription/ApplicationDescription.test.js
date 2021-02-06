import { render, screen } from "@testing-library/react";
import ApplicationDescription from "./ApplicationDescription";

test("should render ApplicationDescription with correct elements", () => {
  render(<ApplicationDescription />);
  screen.getByTestId("description-container");
  //   The exact wording for this is yet to be determined,
  //   TODO update tests to reflect changes to the ux when decided upon
  screen.getByText("Super Awesome Description");
});
