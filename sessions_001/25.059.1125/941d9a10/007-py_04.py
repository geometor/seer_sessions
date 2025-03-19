import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair to extract relevant features."""

    # Find gray lines (horizontal and vertical)
    gray_rows = np.where(np.all(input_grid == 5, axis=1))[0]
    gray_cols = np.where(np.all(input_grid == 5, axis=0))[0]

    # Find colored regions. Assume they are 3x3 and only one of each color
    blue_region_coords = []
    red_region_coords = []
    green_region_coords = []

    for i in range(input_grid.shape[0]):
      for j in range(input_grid.shape[1]):
        if output_grid[i,j] == 1:
          blue_region_coords.append((i,j))
        if output_grid[i,j] == 2:
          red_region_coords.append((i,j))
        if output_grid[i,j] == 3:
          green_region_coords.append((i,j))

    #get the bounding box of the regions
    blue_region = None
    if len(blue_region_coords) > 0:
      blue_region = (
          (min(blue_region_coords, key=lambda x: x[0])[0], min(blue_region_coords, key=lambda x: x[1])[1]),
          (max(blue_region_coords, key=lambda x: x[0])[0], max(blue_region_coords, key=lambda x: x[1])[1])
      )
    red_region = None
    if len(red_region_coords) > 0:
      red_region = (
          (min(red_region_coords, key=lambda x: x[0])[0], min(red_region_coords, key=lambda x: x[1])[1]),
          (max(red_region_coords, key=lambda x: x[0])[0], max(red_region_coords, key=lambda x: x[1])[1])
      )
    green_region = None
    if len(green_region_coords) > 0:
      green_region = (
          (min(green_region_coords, key=lambda x: x[0])[0], min(green_region_coords, key=lambda x: x[1])[1]),
          (max(green_region_coords, key=lambda x: x[0])[0], max(green_region_coords, key=lambda x: x[1])[1])
      )

    return {
        "gray_rows": gray_rows.tolist(),
        "gray_cols": gray_cols.tolist(),
        "blue_region": blue_region,
        "red_region": red_region,
        "green_region": green_region,
    }

# Example usage (replace with actual data from the task - I am adding it manually here)
task_examples = [
    { # Example 0
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 0, 0, 0, 5, 0, 0],
            [0, 0, 5, 0, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 5, 5, 5, 5, 5, 0],
            [0, 0, 5, 0, 0, 0, 5, 0, 0],
            [0, 0, 5, 0, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 5, 3, 3],
            [0, 0, 0, 0, 0, 0, 5, 3, 3],
        ]),
    },
     { # Example 1
        "input": np.array([
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
          [0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0],
          [0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 0, 5, 5, 5, 5, 0, 0, 0],
          [0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0],
          [0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0],
          [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
          [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0],
          [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0],
          [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0],
        ])
    },
        { # Example 2
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
        ])
    }

]

results = [analyze_example(ex["input"], ex["output"]) for ex in task_examples]
print(results)