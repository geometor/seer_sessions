import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    description = f"Grid Size: {rows}x{cols}\n"
    unique_colors = np.unique(grid)
    description += f"Unique Colors: {unique_colors}\n"
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    description += f"Color Counts: {color_counts}\n"

    # object analysis
    objects = {}
    for color in unique_colors:
        coords = np.argwhere(grid == color)
        min_row, min_col = np.min(coords, axis=0)
        max_row, max_col = np.max(coords, axis=0)
        width = max_col - min_col + 1
        height = max_row - min_row + 1

        # consider this an object if it has some area
        if width * height > 0:
            objects[color] = {"min_row":min_row, "min_col":min_col, "max_row":max_row, "max_col":max_col,
                            "width": width, "height": height}

    description += f"Objects:{objects}\n"
    return description
def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the color transformation rules.
            if input_grid[i, j] == 5:
                output_grid[i, j] = 3
            elif input_grid[i,j] == 0:
                output_grid[i, j] = 4
            else:
                 output_grid[i,j] = input_grid[i,j] # Added to accommodate other tasks
    return output_grid

task = {
    "train": [
        {
            "input": [[5, 0, 5], [0, 5, 0], [5, 0, 5]],
            "output": [[3, 4, 3], [4, 3, 4], [3, 4, 3]],
        },
        {
            "input": [[0, 5, 0], [5, 0, 5], [0, 5, 0]],
            "output": [[4, 3, 4], [3, 4, 3], [4, 3, 4]],
        },
        {
            "input": [[5, 0, 5], [0, 0, 0], [5, 0, 5]],
            "output": [[3, 4, 3], [4, 4, 4], [3, 4, 3]],
        },
        {
            "input":  [[0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
            "output": [[4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4],[4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4],[4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4],[4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4],[4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]
        },
        {
            "input":  [[5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5,0,5],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
            "output": [[3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3],[3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3],[3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3],[3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3],[3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]
        }

    ],
    "test": [
        {
            "input": [[0, 5, 0], [5, 5, 5], [0, 5, 0]],
            "output": [[4, 3, 4], [3, 3, 3], [4, 3, 4]],
        }
    ],
}

for i, example in enumerate(task["train"]):
  input_grid = np.array(example["input"])
  expected_output = np.array(example["output"])
  predicted_output = transform(input_grid)
  print(f"Example {i+1}:")
  print("Input:")
  print(describe_grid(input_grid))
  print("Expected Output:")
  print(describe_grid(expected_output))
  print("Predicted Output:")
  print(describe_grid(predicted_output))
  print("Correct:", np.array_equal(expected_output, predicted_output))
  print("-" * 20)