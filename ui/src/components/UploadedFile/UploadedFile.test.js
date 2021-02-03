import { fireEvent, render, screen } from "@testing-library/react";
import UploadedFile from "./UploadedFile";

const props = {
  id: "123",
  file: {
    size: 123123123,
    name: "test-name.txt",
  },
};

test("Should render without issue", () => {
  const title = `File ${props.id}: ${props.file.name} [${(
    props.file.size / 1000
  ).toFixed(1)}KB]`;
  render(<UploadedFile {...props} />);
  screen.getByTestId(`uploaded-file-container-${props.id}`);
  screen.getByTestId(`remove-btn-${props.id}`);
  screen.getByText(title);
});

test("Should call removeFile on remove button click", () => {
  const removeFile = jest.fn();
  render(<UploadedFile {...props} removeFile={removeFile} />);
  const rmvBtn = screen.getByTestId(`remove-btn-${props.id}`);
  fireEvent.click(rmvBtn);

  expect(removeFile).toBeCalled();
});
