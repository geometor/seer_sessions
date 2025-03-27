```python
import numpy as np

"""
Identifies a horizontal gray line that divides the grid.
Red pixels extend vertically towards the gray line, stopping one step away.
Blue pixels extend vertically towards the nearest horizontal grid boundary (top or bottom).
The original colored pixels are included in the extension.
Other pixels (white background, gray line) remain unchanged.
"""

def find_gray_line_row(grid_np):
    """Finds the row index of the solid horizontal gray line."""
    height = grid_np.shape[0]
    for r in range(height):
        # Check if the entire row is gray (color 5)
        if np.all(grid_np[r, :] == 5):
            return r
    return None # Return None if no gray line is found

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find the row index of the horizontal gray line
    gray_row_index = find_gray_line_row(input_np)

    # If no gray line is found (should not happen based on examples), return the original grid copy
    if gray_row_index is None:
        # This case might need specific handling depending on task variations
        # For now, assume the gray line always exists as per the examples
        print("Warning: Gray line not found. Returning copy of input.")
        return output_np.tolist()

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]

            # Process red pixels (color 2)
            if color == 2:
                if r < gray_row_index:
                    # Red pixel is above the gray line, fill downwards towards it
                    # Fill from current row 'r' down to the row just above the gray line
                    output_np[r:gray_row_index, c] = 2
                elif r > gray_row_index:
                    # Red pixel is below the gray line, fill upwards towards it
                    # Fill from the row just below the gray line up to the current row 'r'
                    output_np[gray_row_index + 1 : r + 1, c] = 2
                # Note: If r == gray_row_index, it's part of the line and shouldn't be red based on examples.

            # Process blue pixels (color 1)
            elif color == 1:
                # Calculate distance to top edge (r) and bottom edge (height - 1 - r)
                dist_to_top = r
                dist_to_bottom = height - 1 - r

                if dist_to_top <= dist_to_bottom:
                    # Closer to or equidistant from the top edge, fill upwards
                    # Fill from the top edge (row 0) down to the current row 'r'
                    output_np[0 : r + 1, c] = 1
                else:
                    # Closer to the bottom edge, fill downwards
                    # Fill from the current row 'r' down to the bottom edge (row height - 1)
                    output_np[r:height, c] = 1

            # Gray (5) and White (0) pixels are handled by copying the input initially

    # Convert the output numpy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid

```