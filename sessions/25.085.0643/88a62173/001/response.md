```python
import numpy as np

"""
Identify the four 2x2 quadrants in the 5x5 input grid, separated by the central 
white row (row index 2) and central white column (column index 2). These 
quadrants are Top-Left (TL: rows 0-1, cols 0-1), Top-Right (TR: rows 0-1, cols 3-4), 
Bottom-Left (BL: rows 3-4, cols 0-1), and Bottom-Right (BR: rows 3-4, cols 3-4).

For each quadrant, count the number of non-white pixels (value is not 0).

Determine the maximum count among the four quadrants. If only one quadrant 
has this maximum count, select that quadrant as the output.

If more than one quadrant shares the maximum count, determine the minimum count 
among the four quadrants. If only one quadrant has this minimum count, select 
that quadrant as the output.

If the counts are the same across all four quadrants (meaning neither the 
maximum nor the minimum count was unique), select the Bottom-Right quadrant (BR) 
as the output.

The output grid is a 2x2 grid that is an exact copy of the selected quadrant.
"""

def _count_non_white(grid_part):
  """Counts non-zero pixels in a numpy array."""
  return np.count_nonzero(grid_part)

def transform(input_grid):
    """
    Selects a 2x2 quadrant from a 5x5 grid based on non-white pixel counts.
    """
    # Convert input list of lists to a numpy array for easier slicing
    grid = np.array(input_grid, dtype=int)

    # Ensure the input grid is 5x5
    if grid.shape != (5, 5):
        # Handle unexpected input size if necessary, maybe raise error or return default
        print(f"Warning: Expected 5x5 grid, got {grid.shape}")
        # For now, let's try to proceed if possible, or return an empty/default grid
        # Returning the input might be safest if unsure how to handle
        return input_grid # Or consider raising ValueError

    # 1. Identify the four 2x2 quadrants
    quadrants = {
        "TL": grid[0:2, 0:2],
        "TR": grid[0:2, 3:5],
        "BL": grid[3:5, 0:2],
        "BR": grid[3:5, 3:5]
    }

    # 2. Count non-white pixels in each quadrant
    counts = {name: _count_non_white(quad) for name, quad in quadrants.items()}

    # Convert counts values to a list for easier processing
    count_values = list(counts.values())
    quadrant_names = list(counts.keys())

    # 3. Determine the maximum count and check for uniqueness
    max_count = max(count_values)
    max_indices = [i for i, count in enumerate(count_values) if count == max_count]

    selected_quadrant_name = None

    if len(max_indices) == 1:
        # If only one quadrant has the maximum count, select it
        selected_quadrant_name = quadrant_names[max_indices[0]]
    else:
        # 4. If max count is not unique, determine minimum count and check uniqueness
        min_count = min(count_values)
        min_indices = [i for i, count in enumerate(count_values) if count == min_count]

        if len(min_indices) == 1:
            # If only one quadrant has the minimum count, select it
            selected_quadrant_name = quadrant_names[min_indices[0]]
        else:
            # 5. If min count is also not unique (implies all counts are equal), select Bottom-Right
            selected_quadrant_name = "BR"

    # 6. Get the selected quadrant's grid data
    output_grid_np = quadrants[selected_quadrant_name]

    # Convert the numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```