```python
"""
Identify the primary non-white color (1, 2, or 3) present in the 5x5 input grid.
Based on this identified color, return a specific predefined 3x3 output grid pattern using gray (5) and white (0) pixels.
- If the input color is blue (1), return a gray plus shape.
- If the input color is red (2), return a gray inverted T shape.
- If the input color is green (3), return a gray rotated L shape.
The position or count of the primary color pixels in the input does not affect the output.
"""

import numpy as np

# Define the mapping from input color to output pattern
OUTPUT_PATTERNS = {
    1: np.array([
        [0, 5, 0],
        [5, 5, 5],
        [0, 5, 0]
    ], dtype=int),
    2: np.array([
        [5, 5, 5],
        [0, 5, 0],
        [0, 5, 0]
    ], dtype=int),
    3: np.array([
        [0, 0, 5],
        [0, 0, 5],
        [5, 5, 5]
    ], dtype=int)
}

def find_primary_color(grid):
    """Finds the first non-zero color in the grid."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    # Should not happen based on examples, but good practice
    # Return a default or raise an error if no non-zero color found
    # Let's return 0 for now, assuming the default output should be all white
    # Although the examples guarantee a primary color.
    # Returning None might be better to indicate an issue.
    # Based on the problem constraints, a primary color should always exist.
    raise ValueError("Input grid does not contain a non-white primary color.")


def transform(input_grid):
    """
    Transforms the input grid based on the identified primary color.
    
    Args:
        input_grid (list of lists or numpy array): The 5x5 input grid.

    Returns:
        numpy array: The 3x3 output grid.
    """
    # Ensure input is a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # 1. Identify the primary non-white color
    primary_color = find_primary_color(input_np)

    # 2. Select the corresponding output pattern based on the primary color
    if primary_color in OUTPUT_PATTERNS:
        output_grid = OUTPUT_PATTERNS[primary_color]
    else:
        # Handle unexpected colors if necessary, though examples only show 1, 2, 3
        # For now, let's raise an error for unexpected primary colors
         raise ValueError(f"Unexpected primary color found: {primary_color}")

    # 3. Return the selected 3x3 output grid
    return output_grid

```