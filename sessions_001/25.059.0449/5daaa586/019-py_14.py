import numpy as np

def count_color_blocks(row):
    """Counts the number of contiguous color blocks in a row (excluding 0)."""
    blocks = 0
    current_color = None
    for cell in row:
        if cell != 0 and cell != current_color:
            blocks += 1
            current_color = cell
    return blocks

def get_color_blocks(row):
    """Gets the starting color of each contiguous color block in a row."""
    blocks = []
    current_color = None
    for cell in row:
        if cell != 0 and cell != current_color:
            blocks.append(cell)
            current_color = cell
    return blocks
    
def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    output_rows = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Row Selection: Select rows with more than two color blocks (excluding all 0 rows)
        if count_color_blocks(row) >= 1:
            # Object Identification: Get the color blocks in the row
            blocks = get_color_blocks(row)

            # Transformation and Output Generation
            new_row = []
            if len(blocks) > 0:
                for i in range(len(blocks)):
                  new_row.append(blocks[i])
                  if i < len(blocks) - 1:
                    new_row.append(4)

            if len(new_row) > 0:
                output_rows.append(new_row)

    # Convert the list of output rows to a NumPy array
    if len(output_rows) > 0:
      output_grid = np.array(output_rows)
    else:
      output_grid = np.array([])

    return output_grid

def verify_output(predicted_output, expected_output):
    if predicted_output.shape != expected_output.shape:
        print(f"Failed: Shape mismatch. Expected {expected_output.shape}, got {predicted_output.shape}")
        return False

    comparison = predicted_output == expected_output
    if not comparison.all():
        print(f"Failed: Element mismatch.\nExpected:\n{expected_output}\nGot:\n{predicted_output}")
        return False

    print("Passed")
    return True
# Example usage (replace with your actual task data)
task = {
  "train": [
    {
      "input": [[8, 8, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8], [8, 8, 8, 0, 8, 8, 8, 8, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8]],
      "output": [[8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8], [8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8], [8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8, 4, 8]]
    },
    {
      "input": [[0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[3], [3], [3], [3], [3], [3]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5]],
      "output": [[5], [5], [5], [5], [5], [5]]
    },
    {
      "input": [[6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 0, 0], [6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 0, 0], [6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 0, 0], [6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 0, 0], [6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 0, 0], [6, 0, 6, 0, 6, 0, 6, 0, 6, 0, 0, 0]],
      "output": [[6, 4, 6, 4, 6, 4, 6, 4, 6], [6, 4, 6, 4, 6, 4, 6, 4, 6], [6, 4, 6, 4, 6, 4, 6, 4, 6], [6, 4, 6, 4, 6, 4, 6, 4, 6], [6, 4, 6, 4, 6, 4, 6, 4, 6], [6, 4, 6, 4, 6, 4, 6, 4, 6]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[7, 7, 7, 7, 7, 7]]
    }
  ]
}

for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    input_grid = example["input"]
    expected_output = np.array(example["output"])
    predicted_output = transform(input_grid)
    verify_output(predicted_output, expected_output)
    print("---")