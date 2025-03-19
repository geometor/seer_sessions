import numpy as np

def report_grid_diff(grid1, grid2):
    """Reports the differences between two grids."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    diff = grid1 != grid2
    num_diffs = np.sum(diff)
    return f"Number of differing pixels: {num_diffs}"
def count_colors(grid):
   color_counts = {}
   for color in np.unique(grid):
       color_counts[color] = np.sum(grid == color)
   return color_counts

examples = [
    {
        "input": np.array([[8, 8, 8, 2, 2, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 4, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8]]),
    },
     {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 2, 2, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 4, 8, 8, 8, 8, 8]]),
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 2, 8, 8, 8, 8],
                           [8, 8, 8, 2, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8]]),
    },
   {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 2, 2, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 4, 8, 8, 8, 8]]),
    },
    {
        "input": np.array([[8, 2, 8, 8, 8, 8, 8, 8, 8],
                           [8, 2, 8, 8, 8, 8, 8, 2, 2],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8, 8, 4],
                            [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    },
]
def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)  # Initialize with the input grid
    red_pairs = find_horizontal_red_pairs(input_grid)
    for pair in red_pairs:
        (_, c1), (_, c2) = pair
        # Place yellow pixel to the right of the pair
        if c2 + 1 < output_grid.shape[1]:
           output_grid[c1,c2+1] = 4
        

    return output_grid

def find_horizontal_red_pairs(grid):
    """Finds horizontally adjacent red pixels."""
    red_pairs = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1] - 1):
            if grid[r, c] == 2 and grid[r, c + 1] == 2:
                red_pairs.append(((r, c), (r, c + 1)))
    return red_pairs

for i, example in enumerate(examples):
  input_grid = example['input']
  output_grid = example['output']
  predicted_output = transform(input_grid)
  print(f"Example {i+1}:")
  print(f"  Differences: {report_grid_diff(output_grid, predicted_output)}")
  print(f"Input color counts {count_colors(input_grid)}")
  print(f"Output color counts {count_colors(output_grid)}")
  print(f"Predicted output color counts {count_colors(predicted_output)}")
