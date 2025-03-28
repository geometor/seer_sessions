import numpy as np
from collections import Counter

"""
Identifies horizontal and vertical lines of a single uniform color (L_color) that span the entire grid width or height, respectively.
These lines partition the grid into sections.
The output grid's dimensions are determined by the number of sections created by these lines (height = number of horizontal sections, width = number of vertical sections).
The output grid is filled entirely with the background color (B_color) from the input grid, which is the most frequent color excluding the line color.

1. Identify the color (L_color) forming complete horizontal and/or vertical lines.
2. Record the indices of these horizontal lines (H_lines) and vertical lines (V_lines).
3. Determine the background color (B_color) - the most frequent non-L_color pixel.
4. Calculate output height: Count intervals between horizontal boundaries (including edges and H_lines) that are wider than 1 pixel.
5. Calculate output width: Count intervals between vertical boundaries (including edges and V_lines) that are wider than 1 pixel.
6. Create the output grid of the calculated dimensions, filled with B_color.
"""

def _find_lines(grid):
    """Identifies the line color and indices of horizontal/vertical lines."""
    height, width = grid.shape
    h_lines_candidates = {}
    v_lines_candidates = {}
    potential_line_colors = []

    # Find potential horizontal lines and their colors
    for r in range(height):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1:
            color = unique_colors[0]
            h_lines_candidates[r] = color
            potential_line_colors.append(color)

    # Find potential vertical lines and their colors
    for c in range(width):
        unique_colors = np.unique(grid[:, c])
        if len(unique_colors) == 1:
            color = unique_colors[0]
            v_lines_candidates[c] = color
            potential_line_colors.append(color)

    if not potential_line_colors:
        return None, set(), set()

    # Determine the most likely line color
    line_color = Counter(potential_line_colors).most_common(1)[0][0]

    # Filter actual lines based on the determined line color
    h_lines = {r for r, color in h_lines_candidates.items() if color == line_color}
    v_lines = {c for c, color in v_lines_candidates.items() if color == line_color}

    return line_color, h_lines, v_lines

def _find_background_color(grid, line_color):
    """Finds the most frequent color excluding the line color."""
    pixels = grid.flatten()
    if line_color is not None:
        background_pixels = [p for p in pixels if p != line_color]
    else:
        background_pixels = list(pixels)

    if not background_pixels:
        # Default if only line color exists or grid is empty (edge case)
        return 0 
        
    return Counter(background_pixels).most_common(1)[0][0]

def _calculate_dimension(grid_dim, line_indices):
    """Calculates the output dimension based on line indices."""
    boundaries = sorted(list(set([-1] + list(line_indices) + [grid_dim])))
    count = 0
    for i in range(len(boundaries) - 1):
        if boundaries[i+1] - boundaries[i] > 1:
            count += 1
    # If no lines were found, the count will be 1 (the whole grid is one section)
    # Ensure minimum dimension is 1 if lines perfectly tile without gaps > 1
    return max(1, count) 

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on grid lines partitioning it.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid.
    """
    # Convert input to numpy array if it's not already
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)
        
    height, width = input_grid.shape

    # 1. & 2. Identify line color and indices
    line_color, h_lines, v_lines = _find_lines(input_grid)

    # 3. Determine background color
    background_color = _find_background_color(input_grid, line_color)

    # 4. Calculate output height (number of horizontal sections)
    output_height = _calculate_dimension(height, h_lines)

    # 5. Calculate output width (number of vertical sections)
    output_width = _calculate_dimension(width, v_lines)
    
    # 6. Create and fill the output grid
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    return output_grid