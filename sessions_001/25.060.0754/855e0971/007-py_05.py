import numpy as np

# Provided code (slightly modified for reporting)
def get_columns_with_color(grid, color):
    """Finds columns containing a specified color."""
    cols = []
    for x in range(grid.shape[1]):
        if np.any(grid[:, x] == color):
           cols.append(x)
    return cols

def get_white_regions(grid):
    """Finds contiguous white regions within each column."""
    white_regions = {}
    for x in range(grid.shape[1]):
      white_indices = np.where(grid[:, x] == 0)[0]
      if len(white_indices) > 0:
        regions = []
        start = white_indices[0]
        for i in range(1, len(white_indices)):
          if white_indices[i] != white_indices[i-1] + 1:
            regions.append((x, start, white_indices[i-1]))
            start = white_indices[i]
        regions.append((x, start, white_indices[-1]))
        white_regions[x] = regions
    return white_regions

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array
    # Find columns with white pixels (color 0).
    white_cols = get_columns_with_color(input_grid, 0)

    output_grid = np.copy(input_grid)

    # Vertical Reflection for columns with white
    for col in white_cols:
        # Find the contiguous white region in the column
        white_indices = np.where(input_grid[:, col] == 0)[0]
        if len(white_indices) > 0:
          white_start = white_indices[0]
          white_end = white_indices[-1]
          white_height = white_end-white_start + 1

          #create a slice of the input to reflect
          reflect_region = input_grid[0:white_end+1, col]

          #create an extended output grid
          new_height = input_grid.shape[0] + white_height
          output_grid = np.zeros((new_height, input_grid.shape[1]), dtype=int)

          #copy original input to new grid
          output_grid[0:input_grid.shape[0],:] = input_grid

          #add reflected region
          output_grid[white_end + 1: white_end+1+reflect_region.shape[0], col] = reflect_region

    return output_grid

# Mock training data (replace with actual data loading)
train_data = [
    (
      [[5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5]],
      
      [[5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5]]
    ),
     (
      [[5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5]],
      
      [[5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5]]
    ),
  (
      [[5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 5, 5, 0, 5],
      [5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5]],
      
      [[5, 5, 5, 5, 5, 0, 5],
      [5, 5, 5, 0, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5]]
    ),
  (
      [[0, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 0, 5],
      [5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 0]],
      
      [[5, 5, 5, 5, 5, 0, 5],
      [0, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 5],
      [5, 5, 5, 5, 5, 5, 0]]
    )
]

for i, (input_grid, expected_output) in enumerate(train_data):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_grid = transform(input_grid.tolist())  # Use tolist() for compatibility
    white_cols = get_columns_with_color(input_grid, 0)
    white_regions = get_white_regions(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input Size: {input_grid.shape}")
    print(f"  Output Size: {expected_output.shape}")
    print(f"  Transformed Output Size: {np.array(transformed_grid).shape}")
    print(f"  Columns with White: {white_cols}")
    print(f"Contiguous White Regions: {white_regions}")
    print(f"  Correct Output: {np.array_equal(transformed_grid, expected_output)}")
    print("-" * 20)