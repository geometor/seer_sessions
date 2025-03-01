import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid highlighting the differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    comparison = np.where(grid1 == grid2, 0, grid1)  # 0 if elements are equal, grid1 if not
    return comparison

# Example usage with a dummy grids
grid1 = np.array([[0, 1], [2, 3]])
grid2 = np.array([[0, 1], [2, 4]])  # One difference at [1, 1]
comparison_result = compare_grids(grid1, grid2)
print(comparison_result)

# Load the training data and run the transform to generate predictions

task = {
    "train": [
        {
            "input": [[0, 1, 0, 1, 0],
                      [1, 0, 1, 0, 1],
                      [0, 1, 0, 1, 0]],
            "output": [[0, 2, 0, 2, 0],
                       [0, 0, 0, 0, 0],
                       [2, 0, 2, 0, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 1, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 0, 0, 2, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 2, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 2, 0, 0, 0]]
        }
    ],
    "test": [
        {
            "input": [[1, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0]],
            "output": [[2, 0, 0, 0, 2, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 2, 0, 0, 0, 0]]
        }
    ]
}


def transform(input_grid):
    # Initialize output_grid. The output grid width is the same as the input,
    # and height is 1.5 times the input height.
    input_height, input_width = input_grid.shape
    output_height = int(input_height * 1.5)
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid and map values to the output.
    for r in range(input_height):
        for c in range(input_width):
            output_row = int(r * 1.5)
            if input_grid[r, c] == 1:  # If blue
                output_grid[output_row, c] = 2  # Change to red
            else:  # if white
                output_grid[output_row,c] = input_grid[r,c] # copy the value (which is 0)
                
    return output_grid

print ("\nTrain Set Results:")
for i, example in enumerate(task["train"]):
  input_grid = np.array(example["input"])
  expected_output = np.array(example["output"])
  predicted_output = transform(input_grid)

  print(f"\nExample {i+1}:")
  print("  Input shape:", input_grid.shape)
  print("  Expected output shape:", expected_output.shape)
  print("  Predicted output shape:", predicted_output.shape)

  diff = compare_grids(predicted_output, expected_output)
  if isinstance(diff, str):
    print("  Difference:", diff)
  else:
    print("  Difference (0 means match, other values show differences):")
    print(diff)
