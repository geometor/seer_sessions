```python
import numpy as np

"""
Transformation Rule:

1. Identify a continuous line of azure (8) pixels, which acts as a static barrier. Determine its orientation (horizontal or vertical) and location (row or column index).
2. Identify the 'mobile' color, which is the non-white (0), non-azure (8) color present in the input grid.
3. Initialize an output grid of the same dimensions as the input, filled with white (0).
4. Copy the azure barrier line from the input to the output grid.
5. If the barrier is horizontal at row `b_idx`:
    - For each column, count the number of mobile pixels located strictly *below* the barrier (`row > b_idx`) in the input grid.
    - Place that number of mobile pixels in the same column in the output grid, stacking vertically *upwards* starting from the row immediately *above* the barrier (`row = b_idx - 1`).
6. If the barrier is vertical at column `b_idx`:
    - For each row, count the number of mobile pixels located strictly *to the right* of the barrier (`col > b_idx`) in the input grid.
    - Place that number of mobile pixels in the same row in the output grid, stacking horizontally *rightwards* starting from the column immediately *to the right* of the barrier (`col = b_idx + 1`).
7. Pixels of the mobile color on the 'other' side of the barrier (above a horizontal barrier, left of a vertical barrier) are effectively removed as the output grid starts white and only pixels below/right are counted and relocated.
"""

def find_barrier(grid):
    """Finds the location, orientation, and color of the barrier line."""
    barrier_color = 8 # Azure is the barrier color in examples
    coords = np.argwhere(grid == barrier_color)

    if coords.size == 0:
        return None, None, None # No barrier found

    rows = coords[:, 0]
    cols = coords[:, 1]

    # Check if all barrier pixels are in the same row
    if np.all(rows == rows[0]):
        return 'horizontal', rows[0], barrier_color
    # Check if all barrier pixels are in the same column
    elif np.all(cols == cols[0]):
        return 'vertical', cols[0], barrier_color
    else:
        # This case shouldn't happen based on examples (barrier is always a straight line)
        return None, None, None # Malformed barrier


def find_mobile_color(grid, barrier_color):
    """Finds the color of the mobile pixels."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0 and color != barrier_color: # Not white and not barrier
            return color
    return None # No mobile color found


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_grid)

    # Find the barrier line
    orientation, barrier_index, barrier_color = find_barrier(input_grid)

    if orientation is None:
        # Handle cases without a clear barrier if necessary,
        # for now, assume valid input per examples
        return output_grid # Or return input_grid, or raise error

    # Find the mobile color
    mobile_color = find_mobile_color(input_grid, barrier_color)

    if mobile_color is None:
        # Handle cases without mobile pixels if necessary
        # Copy only the barrier if it exists
        if barrier_index is not None:
             if orientation == 'horizontal':
                 output_grid[barrier_index, :] = barrier_color
             elif orientation == 'vertical':
                 output_grid[:, barrier_index] = barrier_color
        return output_grid

    # Copy the barrier to the output grid
    if orientation == 'horizontal':
        output_grid[barrier_index, :] = barrier_color
    elif orientation == 'vertical':
        output_grid[:, barrier_index] = barrier_color

    # Process based on barrier orientation
    if orientation == 'horizontal':
        # Iterate through each column
        for c in range(width):
            # Count mobile pixels below the barrier in this column
            count = 0
            for r in range(barrier_index + 1, height):
                if input_grid[r, c] == mobile_color:
                    count += 1
            
            # Place the counted pixels above the barrier in the output
            for i in range(count):
                target_row = barrier_index - 1 - i
                # Check bounds before placing
                if target_row >= 0:
                    output_grid[target_row, c] = mobile_color
                else:
                    # Stop if we run out of space above the barrier
                    break

    elif orientation == 'vertical':
        # Iterate through each row
        for r in range(height):
            # Count mobile pixels to the right of the barrier in this row
            count = 0
            for c in range(barrier_index + 1, width):
                if input_grid[r, c] == mobile_color:
                    count += 1

            # Place the counted pixels to the right of the barrier in the output
            for i in range(count):
                target_col = barrier_index + 1 + i
                # Check bounds before placing
                if target_col < width:
                    output_grid[r, target_col] = mobile_color
                else:
                    # Stop if we run out of space to the right
                    break

    return output_grid.tolist() # Return as list of lists per ARC standard

```