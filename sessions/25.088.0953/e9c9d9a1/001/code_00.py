import numpy as np

"""
Transforms the input grid based on compartments defined by green lines.

1.  Identifies the row indices of the topmost and bottommost horizontal green lines.
2.  Identifies the column indices of the leftmost and rightmost vertical green lines.
3.  Creates a copy of the input grid.
4.  Iterates through each white pixel (0) in the input grid.
5.  Based on the pixel's position relative to the identified outermost green lines,
    it fills the corresponding pixel in the output grid with a specific color:
    - Top-left corner compartment (above topmost horizontal, left of leftmost vertical): Red (2)
    - Top-right corner compartment (above topmost horizontal, right of rightmost vertical): Yellow (4)
    - Bottom-left corner compartment (below bottommost horizontal, left of leftmost vertical): Blue (1)
    - Bottom-right corner compartment (below bottommost horizontal, right of rightmost vertical): Azure (8)
    - Central compartments (between topmost and bottommost horizontal, and between leftmost and rightmost vertical): Orange (7)
6.  Green pixels (3) and other white pixels remain unchanged.
"""

def find_lines(grid, axis):
    """Finds the indices of full lines of green (3) along a given axis."""
    lines = []
    target_color = 3
    if axis == 0: # Horizontal lines (check rows)
        for r in range(grid.shape[0]):
            if np.all(grid[r, :] == target_color):
                lines.append(r)
    elif axis == 1: # Vertical lines (check columns)
        for c in range(grid.shape[1]):
            if np.all(grid[:, c] == target_color):
                lines.append(c)
    return lines

def transform(input_grid):
    """
    Applies the compartment coloring transformation to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Find horizontal and vertical green lines
    h_lines = find_lines(input_np, 0)
    v_lines = find_lines(input_np, 1)

    # If no lines are found, return the original grid (or handle as needed)
    if not h_lines or not v_lines:
        # Based on examples, lines always seem present. If not, the logic below
        # might raise errors or produce unexpected results. Returning copy for safety.
        # Consider raising an error or specific handling if this case is possible.
        return output_grid

    # Determine the outermost line indices
    first_h_line = min(h_lines)
    last_h_line = max(h_lines)
    first_v_line = min(v_lines)
    last_v_line = max(v_lines)

    # Define colors for compartments
    colors = {
        'top_left': 2,      # Red
        'top_right': 4,     # Yellow
        'bottom_left': 1,   # Blue
        'bottom_right': 8,  # Azure
        'central': 7,       # Orange
    }

    # Iterate through each pixel and apply coloring rules if it's white (0)
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 0: # Check only white pixels
                # Top-left compartment
                if r < first_h_line and c < first_v_line:
                    output_grid[r, c] = colors['top_left']
                # Top-right compartment
                elif r < first_h_line and c > last_v_line:
                    output_grid[r, c] = colors['top_right']
                # Bottom-left compartment
                elif r > last_h_line and c < first_v_line:
                    output_grid[r, c] = colors['bottom_left']
                # Bottom-right compartment
                elif r > last_h_line and c > last_v_line:
                    output_grid[r, c] = colors['bottom_right']
                # Central compartments
                elif first_h_line < r < last_h_line and first_v_line < c < last_v_line:
                    output_grid[r, c] = colors['central']
                # Other white areas remain white (handled by the initial copy)

    return output_grid.tolist() # Return as list of lists