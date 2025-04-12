import numpy as np

"""
Transforms the input grid based on a local neighborhood rule.
1. Identifies the single dominant non-background color (shape_color) in the input grid.
2. Iterates through each background pixel (color 0).
3. If a background pixel is orthogonally adjacent to at least one pixel of the shape_color, 
   its color is changed to the shape_color in the output grid.
4. Pixels that are not background or do not meet the adjacency condition retain their original color.
"""

def _find_shape_color(grid: np.ndarray) -> int:
    """
    Finds the unique non-background color in the grid.
    Assumes there is exactly one non-background color, or returns 0 if none exist.
    """
    unique_colors = np.unique(grid)
    non_background_colors = unique_colors[unique_colors != 0]
    if len(non_background_colors) == 1:
        return non_background_colors[0]
    elif len(non_background_colors) == 0:
         # Handle case with only background
         return 0
    else:
        # If multiple non-background colors, the rule might be ambiguous based on examples.
        # Defaulting to the most frequent non-background color might be an alternative, 
        # but sticking to the observed pattern of a single shape color for now.
        # Let's find the most frequent one.
        colors, counts = np.unique(grid[grid != 0], return_counts=True)
        if len(colors) > 0:
            return colors[np.argmax(counts)]
        else:
            return 0 # Should not happen if len(non_background_colors) > 0 but handle defensively

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    background_color = 0

    # 1. Identify the shape color
    shape_color = _find_shape_color(grid)

    # If no shape color is found (e.g., all background), return the original grid
    if shape_color == background_color:
        return output_grid.tolist()

    # Define orthogonal neighbor directions
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # 2. Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # 3. Check if the current cell is background color
            if grid[r, c] == background_color:
                neighbor_count = 0
                # 4. Count orthogonal neighbors with the shape_color
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if neighbor has the shape_color
                        if grid[nr, nc] == shape_color:
                            neighbor_count += 1
                
                # 5. If at least one neighbor has the shape_color, update the output grid
                if neighbor_count >= 1:
                    output_grid[r, c] = shape_color

    # Convert back to list of lists and return
    return output_grid.tolist()