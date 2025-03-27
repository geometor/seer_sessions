```python
import numpy as np

def find_color_x(grid):
    """
    Identifies the unique non-gray color (Color X) in a grid.
    Assumes the grid contains exactly two colors: gray (5) and Color X.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The value of Color X.
    """
    unique_colors = np.unique(grid)
    # Filter out gray (5) and return the remaining color
    for color in unique_colors:
        if color != 5:
            return int(color) # Ensure it's a standard Python int
    # Should not happen based on task description, but handle defensively
    raise ValueError("Could not find a non-gray color (Color X) in the grid.")

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Identify the unique non-gray color (Color X).
    2. Replace all gray (5) pixels with Color X.
    3. Replace all original Color X pixels with white (0).
    """
    # Convert input to NumPy array for efficient operations
    grid = np.array(input_grid, dtype=int)

    # Step 1: Identify Color X
    try:
        color_x = find_color_x(grid)
    except ValueError as e:
        print(f"Error: {e}")
        # Return input grid unchanged or handle error as appropriate
        return input_grid

    # Create a copy of the grid to modify as the output
    # Using zeros ensures any pixel not explicitly set remains white (0)
    # but the rule dictates only gray and color_x change, others shouldn't exist.
    # Let's initialize with zeros and then fill based on the rules.
    output_grid = np.zeros_like(grid, dtype=int)

    # Step 2 & 3: Apply transformations using boolean indexing
    # Find locations of gray pixels
    gray_mask = (grid == 5)
    # Find locations of Color X pixels
    color_x_mask = (grid == color_x)

    # Apply the replacement rules
    # Where input was gray (5), output becomes Color X
    output_grid[gray_mask] = color_x
    # Where input was Color X, output becomes white (0)
    output_grid[color_x_mask] = 0
    # Note: Any pixel that was neither gray nor Color X (if any existed)
    # would remain 0 in the output_grid as initialized.

    # Convert the result back to a list of lists for the ARC environment
    return output_grid.tolist()

```