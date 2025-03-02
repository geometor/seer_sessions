import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    """Analyzes an example and provides metrics."""

    input_yellow_pixels = np.sum(input_grid == 4)
    expected_yellow_pixels = np.sum(expected_output == 4)
    actual_yellow_pixels = np.sum(actual_output == 4)

    input_yellow_positions = np.array(np.where(input_grid == 4)).T
    expected_yellow_positions = np.array(np.where(expected_output == 4)).T
    actual_yellow_positions = np.array(np.where(actual_output == 4)).T

    print(f"  Input Yellow Pixels: {input_yellow_pixels}")
    print(f"  Expected Yellow Pixels: {expected_yellow_pixels}")
    print(f"  Actual Yellow Pixels: {actual_yellow_pixels}")
    print(f"  Input Yellow Positions:\n{input_yellow_positions}")
    print(f"  Expected Yellow Positions:\n{expected_yellow_positions}")
    print(f"  Actual Yellow Positions:\n{actual_yellow_positions}")
    print("-" * 20)
def get_cross_object(grid, color=4):
    rows, cols = grid.shape
    vertical_bar = []
    horizontal_bar = []

    # Find vertical bar
    for c in range(cols):
      for r in range(rows):
        if grid[r,c] == color:
          vertical_bar.append((r,c))
          break

    # Find the vertical bar's column
    vertical_col = -1
    if vertical_bar:
      vertical_col = vertical_bar[0][1]


    # Find Horizontal Bar
    for r in range(rows):
      for c in range(cols):
        if grid[r,c] == color:
            horizontal_bar.append((r,c))
            break

    # Find the horizontal bar's row
    horizontal_row = -1
    if horizontal_bar:
      horizontal_row = horizontal_bar[0][0]
        

    return vertical_bar, horizontal_bar, vertical_col, horizontal_row

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get the cross object parts
    vertical_bar, horizontal_bar, vertical_col, horizontal_row = get_cross_object(input_grid)

    # Move the vertical bar to the first column
    if vertical_bar:
        for r in range(rows):
            output_grid[r, 0] = 4

    # move horizontal bar to row index 6
    if horizontal_bar:
          new_row = horizontal_row + 3
          if 0 <= new_row < rows:
            for c in range(cols):
              output_grid[new_row,c] = 4


    return output_grid

# Example Data (replace with actual data from the task)
train = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 4, 4, 4, 4, 4, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
np.array([[4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
(np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 4, 4, 4, 4, 4, 4, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
np.array([[4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]])),
(np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 4, 4, 4, 0, 0, 0],
       [0, 0, 0, 0, 4, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
np.array([[4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]))
]
for i, (input_grid, expected_output) in enumerate(train):
    actual_output = transform(input_grid)
    print(f"Example {i+1}:")
    analyze_example(input_grid, expected_output, actual_output)