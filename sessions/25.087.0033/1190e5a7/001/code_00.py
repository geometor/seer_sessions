import numpy as np
from collections import Counter

"""
Identify the line color that forms complete horizontal and/or vertical lines.
Identify the background color (typically the most frequent color that is not the line color).
Count the number of horizontal lines (H) and vertical lines (V).
The output grid dimensions are (H + 1) rows and (V + 1) columns.
Fill the output grid entirely with the background color.
"""

def find_line_color(grid):
    """Identifies the color forming complete horizontal or vertical lines."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)

    for color in unique_colors:
        # Check for complete horizontal lines
        for r in range(rows):
            if np.all(grid[r, :] == color):
                return color  # Found a horizontal line color

        # Check for complete vertical lines
        for c in range(cols):
            if np.all(grid[:, c] == color):
                return color # Found a vertical line color
    
    # Should not happen based on task description, but return None if no line color found
    return None 

def find_background_color(grid, line_color):
    """Identifies the background color (most frequent non-line color)."""
    counts = Counter(grid.flatten())
    
    # Remove the line color from counts if it exists
    if line_color in counts:
        del counts[line_color]
        
    # If there are other colors, return the most common one
    if counts:
        return counts.most_common(1)[0][0]
    
    # Edge case: If the grid only contained the line color (unlikely for this task)
    # Or if the logic failed to find a non-line color. 
    # Returning 0 (white) as a fallback, though this might need adjustment based on constraints.
    # Based on examples, background color is always present.
    if not counts:
        # Fallback: check a corner that's not part of a line?
        # Check top-left, assuming it's not a crossing point of lines
        if grid[0, 0] != line_color:
            return grid[0, 0]
        # Check another point if top-left is a line
        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if grid[r,c] != line_color:
                    return grid[r,c]

    # If still no background found (e.g., grid is all line color), this is an unexpected state.
    # Returning a default (like 0) might be necessary, but indicates a problem.
    return 0 # Default fallback


def transform(input_grid):
    """
    Transforms the input grid by identifying line patterns and creating an output
    grid representing the segmented regions filled with the background color.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Identify the line color
    line_color = find_line_color(input_grid_np)
    if line_color is None:
        # Handle error: No line color found (may indicate input doesn't match pattern)
        # For now, return a minimal grid or raise an error
        print("Warning: No line color identified.")
        # Try guessing background based on frequency alone if line color fails
        counts = Counter(input_grid_np.flatten())
        if counts:
             background_color = counts.most_common(1)[0][0]
             return np.full((1, 1), background_color, dtype=int).tolist() # Default 1x1 grid
        else:
             return [[0]] # Absolute fallback


    # 2. Identify the background color
    background_color = find_background_color(input_grid_np, line_color)

    # 3. Count the number of distinct horizontal lines
    horizontal_line_count = 0
    for r in range(rows):
        if np.all(input_grid_np[r, :] == line_color):
            horizontal_line_count += 1
    output_rows = horizontal_line_count + 1

    # 4. Count the number of distinct vertical lines
    vertical_line_count = 0
    for c in range(cols):
        if np.all(input_grid_np[:, c] == line_color):
            vertical_line_count += 1
    output_cols = vertical_line_count + 1

    # 5. Create a new grid with dimensions R rows and C columns
    # 6. Fill this new grid entirely with the identified background color
    output_grid_np = np.full((output_rows, output_cols), background_color, dtype=int)

    # Convert back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid