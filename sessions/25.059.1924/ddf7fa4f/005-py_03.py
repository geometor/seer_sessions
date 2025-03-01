import numpy as np

def find_object(grid, color):
    """Finds the bounding box of a contiguous region of the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Color not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def analyze_example(input_grid, output_grid):
    # Gray region dimensions
    gray_bounds = find_object(input_grid, 5)
    if gray_bounds is None:
        gray_width = gray_height = 0
    else:
        gray_min_row, gray_min_col = gray_bounds[0]
        gray_max_row, gray_max_col = gray_bounds[1]
        gray_width = gray_max_col - gray_min_col + 1
        gray_height = gray_max_row - gray_min_row + 1

    # Top row colors (excluding white)
    top_row_colors = [color for color in np.unique(input_grid[0]) if color != 0]

    # Colored region dimensions in output
    colored_region_widths = []
    for color in top_row_colors:
        color_bounds = find_object(output_grid, color)
        if color_bounds:
            color_min_row, color_min_col = color_bounds[0]
            color_max_row, color_max_col = color_bounds[1]
            color_width = color_max_col - color_min_col + 1
            colored_region_widths.append(color_width)
        else:
            colored_region_widths.append(0)

    print(f"  Gray Region: Width={gray_width}, Height={gray_height}")
    print(f"  Top Row Colors: {top_row_colors}")
    print(f"  Colored Region Widths in Output: {colored_region_widths}")

    # also get the width of the colors in the top row
    top_row_widths = []
    for color in top_row_colors:
        bounds = find_object(input_grid[0:1, :], color)
        if bounds is not None:
          min_row, min_col = bounds[0]
          max_row, max_col = bounds[1]
          width = max_col - min_col + 1
        else:
          width = 0

        top_row_widths.append(width)

    print(f"  Top Row Widths: {top_row_widths}")
    print("-" * 20)


task_id = 'f2a864af'
examples = [
  {
    "input": [
      [0, 2, 0, 0, 0, 6, 6, 0, 0, 8, 8, 8],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
      [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
      [0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0]
    ],
    "output": [
      [0, 2, 0, 0, 0, 6, 6, 0, 0, 8, 8, 8],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 2, 2, 6, 6, 6, 6, 8, 8, 8, 0],
      [0, 0, 2, 2, 6, 6, 6, 6, 8, 8, 8, 0],
      [0, 0, 2, 2, 6, 6, 6, 6, 8, 8, 8, 0]
    ]
  },
    {
    "input": [
      [0, 0, 0, 0, 0, 6, 0, 0, 8, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
      [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0]
    ],
    "output": [
      [0, 0, 0, 0, 0, 6, 0, 0, 8, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 6, 6, 6, 6, 6, 8, 8, 8, 0, 0, 0],
      [0, 6, 6, 6, 6, 6, 8, 8, 8, 0, 0, 0]
    ]
  },
    {
    "input": [
      [0, 0, 0, 2, 0, 0, 0, 6, 0, 0, 8, 8],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
      [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
      [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0]
    ],
    "output": [
      [0, 0, 0, 2, 0, 0, 0, 6, 0, 0, 8, 8],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 2, 2, 2, 2, 6, 6, 6, 8, 8, 8, 0],
      [0, 2, 2, 2, 2, 6, 6, 6, 8, 8, 8, 0],
      [0, 2, 2, 2, 2, 6, 6, 6, 8, 8, 8, 0]
    ]
  },
      {
    "input": [
      [0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
      [5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0]
    ],
    "output": [
      [0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0],
      [6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0]
    ]
  }
]

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(np.array(example["input"]), np.array(example["output"]))