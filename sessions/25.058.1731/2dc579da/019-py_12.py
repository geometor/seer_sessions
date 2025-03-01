import numpy as np

def find_pixel_location(grid, color):
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return [r, c]
    return None

def get_blue_pixels(grid):
    blue_pixels = []
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == 1:
                blue_pixels.append((r, c))
    return blue_pixels

def transform(input_grid):
    input_grid = np.array(input_grid)
    azure_location = find_pixel_location(input_grid, 8)
    blue_pixels = get_blue_pixels(input_grid)
    row_start = azure_location[0] - 2
    row_end = azure_location[0] + 3
    col_start = azure_location[1] - 2
    col_end = azure_location[1] + 3
    output_grid = np.zeros((5, 5), dtype=int)
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
                if (r, c) not in blue_pixels:
                    output_row = r - row_start
                    output_col = c - col_start
                    output_grid[output_row, output_col] = input_grid[r, c]
    return output_grid.tolist()

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 8, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 8, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 8, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 8, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 8, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
        [0, 1, 1, 1, 8, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
       [0,0,0,0,0],
       [0,1,0,0,2],
       [1,8,1,1,1],
       [0,1,0,0,2],
       [0,0,0,0,0]
      ]
    }
  ]
}

def compare_grids(grid1, grid2):
    return np.array_equal(np.array(grid1), np.array(grid2))

for i, example in enumerate(task["train"]):
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Expected Output: {expected_output}")
    print(f"  Actual Output:   {actual_output}")
    print(f"  Match:           {compare_grids(expected_output, actual_output)}")