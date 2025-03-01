import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a grid highlighting the differences.
    Differences are marked with 1, identical cells with 0.
    """
    return (grid1 != grid2).astype(int)

def count_pixels(grid):
    """
    Counts the occurrences of each pixel value in a grid.
    """
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

task_data = {
    "train": [
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 2, 8, 8],
                [8, 5, 5, 5, 5, 8, 2, 2, 2, 8],
                [8, 5, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        },
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 5, 5, 5, 5, 5, 8],
                [8, 5, 8, 8, 8, 8, 8, 8, 5, 8],
                [8, 5, 8, 5, 5, 5, 5, 8, 5, 8],
                [8, 5, 8, 5, 5, 8, 8, 8, 5, 8],
                [8, 5, 8, 5, 5, 5, 5, 5, 5, 8],
                [8, 5, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 5, 5, 5, 5, 5, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                [0, 5, 0, 0, 0, 0, 0, 0, 5, 0],
                [0, 5, 0, 5, 5, 5, 5, 0, 5, 0],
                [0, 5, 0, 5, 5, 0, 0, 0, 5, 0],
                [0, 5, 0, 5, 5, 5, 5, 5, 5, 0],
                [0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        },
		{
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 5, 5, 5, 5, 8, 8, 8, 8, 8, 5, 5, 5, 5, 8],
                [8, 8, 5, 5, 5, 5, 8, 8, 8, 8, 8, 5, 5, 5, 5, 8],
                [8, 8, 5, 5, 5, 5, 8, 8, 8, 8, 8, 5, 5, 5, 5, 8],
                [8, 8, 5, 5, 5, 5, 8, 8, 8, 8, 8, 5, 5, 5, 5, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
                [0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
                [0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
                [0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }
    ]
}

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Red(2) -> White(0)
    Azure(8) -> White(0)
    Other colors remain unchanged.
    """
    output_grid = np.copy(input_grid)  # Create a copy to avoid modifying the original

    # Iterate through each pixel in the grid
    for row_index, row in enumerate(input_grid):
        for col_index, pixel in enumerate(row):
            # Apply the color change rules
            if pixel == 2:  # Red
                output_grid[row_index][col_index] = 0  # White
            elif pixel == 8:  # Azure
                output_grid[row_index][col_index] = 0  # White

    return output_grid

results = []
for i, example in enumerate(task_data["train"]):
  input_grid = np.array(example["input"])
  expected_output = np.array(example["output"])
  predicted_output = transform(input_grid)
  diff_grid = compare_grids(predicted_output, expected_output)
  input_pixel_counts = count_pixels(input_grid)
  expected_output_pixel_counts = count_pixels(expected_output)
  predicted_output_pixel_counts = count_pixels(predicted_output)
  diff_pixel_counts = count_pixels(diff_grid)

  results.append(
      {
          "example": i + 1,
          "input_pixels": input_pixel_counts,
          "expected_output_pixels": expected_output_pixel_counts,
          "predicted_output_pixels": predicted_output_pixel_counts,
          "diff_pixels": diff_pixel_counts,
          "diff_grid": diff_grid.tolist()
      }
  )

for result in results:
  print(result)