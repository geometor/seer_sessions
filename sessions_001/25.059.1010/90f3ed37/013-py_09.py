import numpy as np

def find_azure_regions(grid):
    """Finds all contiguous horizontal lines of azure (8) pixels."""
    azure_regions = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = None
        for c in range(cols):
            if grid[r, c] == 8:
                if start_col is None:
                    start_col = c
            elif start_col is not None:
                length = c - start_col
                azure_regions.append({
                    'start_row': r,
                    'start_col': start_col,
                    'end_col': c -1,
                    'length': length
                })
                start_col = None
        if start_col is not None:  # Handle regions that extend to the end of the row
            length = cols - start_col
            azure_regions.append({
                'start_row': r,
                'start_col': start_col,
                'end_col': cols - 1,
                'length': length
            })
    return azure_regions

def transform(input_grid):
    """Transforms the input grid by replacing adjacent segments to azure regions with blue."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find all azure regions
    azure_regions = find_azure_regions(output_grid)

    # Replace adjacent segment with blue
    for region in azure_regions:
      start_row = region['start_row']
      end_col = region['end_col']
      length = region['length']
      replace_start_col = end_col + 1

      for i in range(length):
          if replace_start_col + i < cols: # stay in bounds
            output_grid[start_row, replace_start_col + i] = 1

    return output_grid

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    input_azure = find_azure_regions(input_grid)
    output_azure = find_azure_regions(output_grid)
    transformed_grid = transform(input_grid)
    is_correct = np.array_equal(transformed_grid, output_grid)

    print(f"Input Azure Regions: {input_azure}")
    print(f"Output Azure Regions: {output_azure}")
    print(f"Transformation Correct: {is_correct}")

    # Show differences if not correct
    if not is_correct:
      diff = transformed_grid != output_grid
      print(f"Difference indices: {np.where(diff)}")
      print("Transformed Grid:\n", transformed_grid)
      print("Expected Output Grid:\n", output_grid)

# Example data (replace with actual data from the task)

examples = [
    (np.array([[8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 8, 8, 0],
              [0, 0, 0, 0, 0, 0, 8, 8, 8, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),

    (np.array([[8, 8, 0, 0, 0, 0, 0, 8, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 8, 8, 8, 8, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[1, 1, 0, 0, 0, 0, 0, 8, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),

    (np.array([[0, 0, 0, 0, 8, 8, 0, 0, 0, 0],
               [0, 8, 8, 8, 8, 8, 8, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 8, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
               [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 8, 0, 0, 0]]))
]


for i, (input_grid, output_grid) in enumerate(examples):
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, output_grid)