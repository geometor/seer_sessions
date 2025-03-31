```python
import numpy as np

"""
Find the single object in the input grid, composed of an outer frame color and an inner core color. 
Create an output grid by copying the input. 
Then, for every pixel in the original input object: 
- if it has the inner color, paint its direct orthogonal neighbors (up, down, left, right) with the inner color, provided they are currently white (0) and within grid bounds. 
- if it has the outer color, paint the cells two steps away orthogonally (up, down, left, right) with the outer color, provided they are currently white (0) and within grid bounds.
The painting happens on the output grid, using the original input grid as the reference for source pixel colors and locations.
"""

def find_colors(grid):
    """Finds the unique non-zero colors in the grid."""
    return sorted(list(np.unique(grid[grid != 0])))

def find_bounding_box(grid):
    """Finds the bounding box (min_row, min_col, max_row, max_col) of non-zero pixels."""
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None
    min_r, min_c = non_white_coords.min(axis=0)
    max_r, max_c = non_white_coords.max(axis=0)
    return (min_r, min_c, max_r, max_c)

def determine_inner_outer(grid, colors, bbox):
    """
    Determines the inner and outer colors.
    Assumes the color at the top-left corner of the bounding box is the outer color.
    """
    min_r, min_c, _, _ = bbox
    # The color at a corner of the bounding box is assumed to be the outer frame color.
    outer_c = grid[min_r, min_c]
    # The other non-white color must be the inner color.
    inner_c = colors[0] if colors[1] == outer_c else colors[1]
    return inner_c, outer_c

def transform(input_grid):
    """
    Applies the expansion transformation to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Find the non-white colors present
    non_white_colors = find_colors(input_np)

    # Expecting exactly two non-white colors for this pattern
    if len(non_white_colors) != 2:
        # If not two colors, or no colors, return the original grid
        # Or could raise an error depending on desired behavior for unexpected inputs
        return input_grid 

    # Find the bounding box of the object
    bbox = find_bounding_box(input_np)
    if bbox is None:
        # If no object found, return the original grid
        return input_grid

    # Determine which color is inner and which is outer
    inner_color, outer_color = determine_inner_outer(input_np, non_white_colors, bbox)

    # Define the relative coordinates for 1-step and 2-step orthogonal neighbors
    one_step_neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    two_step_neighbors = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    # Iterate through each cell of the *original* input grid
    for r in range(rows):
        for c in range(cols):
            original_color = input_np[r, c]

            # If the cell has the inner color, paint 1 step away
            if original_color == inner_color:
                for dr, dc in one_step_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if the target cell in the output is currently white
                    if 0 <= nr < rows and 0 <= nc < cols and output_np[nr, nc] == 0:
                        output_np[nr, nc] = inner_color
            
            # If the cell has the outer color, paint 2 steps away
            elif original_color == outer_color:
                for dr, dc in two_step_neighbors:
                    nr, nc = r + dr, c + dc
                    # Check bounds and if the target cell in the output is currently white
                    if 0 <= nr < rows and 0 <= nc < cols and output_np[nr, nc] == 0:
                        output_np[nr, nc] = outer_color

    # Convert the result back to a list of lists
    return output_np.tolist()
```