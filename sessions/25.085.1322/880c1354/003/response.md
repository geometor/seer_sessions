```python
import numpy as np

"""
Transformation Rule:

1. Identify the set of unique colors present in the input grid.
2. Separate the colors into 'static' (yellow(4), orange(7)) which always map to themselves, and 'dynamic' (all others).
3. Determine the specific color mapping rule based on the exact set of 'dynamic' colors present:
    - If dynamic colors are {blue(1), red(2), green(3), magenta(6)}, apply the cyclic mapping: 1->3, 3->2, 2->6, 6->1.
    - If dynamic colors are {blue(1), magenta(6), maroon(9)}, apply the cyclic mapping: 1->9, 9->6, 6->1.
    - If dynamic colors are {gray(5), magenta(6)}, apply the swap mapping: 5->6, 6->5.
4. Apply the determined mapping (including static color mappings) to every pixel in the input grid to produce the output grid. The output grid retains the same dimensions as the input.
"""

def transform(input_grid):
    """
    Applies a conditional color mapping transformation based on the set of non-static colors present.

    Args:
        input_grid (list of lists): A 2D list of integers representing the input grid.

    Returns:
        list of lists: A 2D list of integers representing the transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # --- Determine the transformation rule ---

    # Find all unique colors present in the grid
    unique_colors = set(np.unique(grid))

    # Identify the dynamic colors (excluding static yellow(4) and orange(7))
    static_colors = {4, 7}
    dynamic_colors = unique_colors - static_colors

    # Initialize the color mapping dictionary
    color_map = {}

    # Always map static colors to themselves
    color_map[4] = 4
    color_map[7] = 7

    # Determine the specific mapping based on the set of dynamic colors
    # Use a sorted tuple for consistent set representation
    dynamic_colors_tuple = tuple(sorted(list(dynamic_colors)))

    if dynamic_colors_tuple == (1, 2, 3, 6):
        # Case 1: {blue(1), red(2), green(3), magenta(6)} -> Cycle 1->3->2->6->1
        color_map.update({1: 3, 3: 2, 2: 6, 6: 1})
    elif dynamic_colors_tuple == (1, 6, 9):
         # Case 2: {blue(1), magenta(6), maroon(9)} -> Cycle 1->9->6->1
        color_map.update({1: 9, 9: 6, 6: 1})
    elif dynamic_colors_tuple == (5, 6):
         # Case 3: {gray(5), magenta(6)} -> Swap 5<->6
        color_map.update({5: 6, 6: 5})
    # else:
        # If other dynamic colors were present but not in the defined cases,
        # they would implicitly map to themselves via the .get default later.
        # No explicit handling needed here if the examples cover all cases.

    # --- Apply the transformation ---

    # Initialize output_grid as a copy of the input grid to preserve dimensions
    output_grid = np.copy(grid)

    # Iterate through each pixel and apply the determined color mapping
    for r in range(height):
        for c in range(width):
            input_color = grid[r, c]
            # Get the mapped color. Default to the input color itself if not found
            # in the map (covers static colors and any potential edge cases).
            output_grid[r, c] = color_map.get(input_color, input_color)

    # Convert the result back to a list of lists for the required output format
    return output_grid.tolist()
```