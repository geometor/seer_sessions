```python
import numpy as np
from collections import Counter

"""
Transformation Rule: Conditional Global Color Replacement based on Color Counts and Adjacency

1.  **Analyze Colors**: Examine the input grid and count the occurrences of each distinct color.
2.  **Check Color Count**: If there are not exactly three distinct colors in the grid, return the original grid unmodified.
3.  **Identify Key Colors**:
    *   Find the `background_color`, which is the color that appears most frequently.
    *   Identify the two remaining colors (non-background colors).
    *   Compare the counts of these two remaining colors. The one with the *smaller* count is the `fill_color`. If their counts are equal, the one with the numerically *lower* color value is designated the `fill_color`.
    *   The color that is neither the `background_color` nor the `fill_color` is the `barrier_color`.
4.  **Check Initial Adjacency**: Determine if any pixel initially having the `fill_color` is directly adjacent (up, down, left, or right, not diagonally) to any pixel initially having the `background_color` in the input grid.
5.  **Apply Transformation**:
    *   **If** the grid had exactly three colors **AND** at least one `fill_color` pixel was adjacent to a `background_color` pixel in the input:
        *   Create a new grid based on the input.
        *   Change the color of **every** pixel that had the `background_color` in the original input grid to the `fill_color`.
        *   Leave all pixels that were originally the `fill_color` or the `barrier_color` unchanged.
        *   Return the modified grid.
    *   **Else** (either not exactly three colors OR no initial adjacency between fill and background):
        *   Return the original input grid unmodified.
"""

def _is_adjacent(grid: np.ndarray, color1: int, color2: int) -> bool:
    """
    Checks if any pixel of color1 is cardinally adjacent to a pixel of color2.
    Optimized by only checking neighbors of color1 pixels.
    """
    rows, cols = grid.shape
    # Find all coordinates where the grid has color1
    color1_coords = np.argwhere(grid == color1)

    # Iterate through each coordinate of color1
    for r, c in color1_coords:
        # Check cardinal neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if the neighbor's coordinates are within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor pixel has color2
                if grid[nr, nc] == color2:
                    return True # Found an adjacent pair
    # If no adjacent pair is found after checking all color1 pixels and their neighbors
    return False

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a conditional global color replacement based on color frequencies and adjacency.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Analyze Input Colors: Get unique colors and their counts
    colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(colors, counts))

    # 2. Check Color Count: Must be exactly 3 colors
    if len(colors) != 3:
        # If not exactly 3 colors, return the original grid
        return input_grid

    # 3. Identify Key Colors
    # Find background color (most frequent)
    # np.argmax returns the index of the first maximum in case of ties.
    background_color_index = np.argmax(counts)
    background_color = colors[background_color_index]

    # Identify the other two colors and their counts
    non_background_colors = []
    non_background_counts = []
    for color, count in color_counts.items():
        if color != background_color:
            non_background_colors.append(color)
            non_background_counts.append(count)

    # Assign the two non-background colors and counts
    color1, color2 = non_background_colors[0], non_background_colors[1]
    count1, count2 = non_background_counts[0], non_background_counts[1]

    # Determine fill and barrier colors based on counts
    # Fill color is the one with the smaller count.
    # Tie-breaking: If counts are equal, the numerically smaller color value is the fill color.
    if count1 < count2:
        fill_color = color1
        barrier_color = color2
    elif count2 < count1:
        fill_color = color2
        barrier_color = color1
    else: # Counts are equal, use lower color value as fill color
        fill_color = min(color1, color2)
        barrier_color = max(color1, color2)

    # 4. Check Initial Adjacency: Is fill_color adjacent to background_color?
    # Use the helper function to check adjacency in the original grid
    is_fill_adjacent_to_background = _is_adjacent(grid, fill_color, background_color)

    # 5. Perform Transformation
    # Check if the trigger conditions are met: exactly 3 colors AND initial adjacency exists
    if is_fill_adjacent_to_background:
        # If conditions met, perform global replacement
        # Create a copy of the grid to modify
        output_grid = grid.copy()
        # Find all pixels that were originally the background color
        # and change them to the fill color in the output grid.
        output_grid[grid == background_color] = fill_color
        # Convert the resulting NumPy array back to a list of lists
        return output_grid.tolist()
    else:
        # If conditions are not met (no initial adjacency), return the original grid
        return input_grid
```