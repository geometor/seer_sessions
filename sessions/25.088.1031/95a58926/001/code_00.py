import numpy as np

"""
Identifies horizontal and vertical gray (5) lines that form a grid structure.
Finds the unique 'target' color (not white 0 or gray 5) present in the input.
Initializes the output grid by copying the gray structure onto a white background.
Iterates through each intersection point (r, c) of the gray lines.
For each intersection, defines the 'cell' area above and to its left (bounded by the previous gray lines or grid edges).
Scans this cell area in the input grid for the presence of the target color.
If the target color is found within the input cell, the corresponding intersection point (r, c) in the output grid is changed from gray (5) to the target color.
Otherwise, the intersection point remains gray. All other non-gray areas in the output are white (0).
"""

def find_target_color(grid):
    """Finds the unique color in the grid that is not 0 (white) or 5 (gray)."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0 and color != 5:
            return color
    # Should ideally not happen based on problem description,
    # but return a default or raise error if necessary
    return -1 # Indicate not found or error

def find_grid_lines(grid):
    """Finds the indices of full horizontal and vertical gray lines."""
    height, width = grid.shape
    horz_lines = [r for r in range(height) if np.all(grid[r, :] == 5)]
    vert_lines = [c for c in range(width) if np.all(grid[:, c] == 5)]
    return horz_lines, vert_lines

def transform(input_grid):
    """
    Transforms the input grid based on the presence of a target color within
    cells defined by gray lines. Marks the bottom-right intersection of a cell
    with the target color if the cell contained that color.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with white (0)

    # Identify the target color
    target_color = find_target_color(input_grid)
    if target_color == -1:
        # Handle case where no target color is found (e.g., return input or error)
        # For now, let's assume a target color always exists per the examples
        print("Warning: No target color found.")
        # Copy input to output if no transformation seems possible
        return input_grid.tolist()


    # Identify the gray grid lines
    horz_lines, vert_lines = find_grid_lines(input_grid)

    # Copy the initial gray structure to the output grid
    output_grid[input_grid == 5] = 5

    # Process each intersection point
    for r in horz_lines:
        for c in vert_lines:
            # Determine the previous grid lines (or grid edge)
            # Find largest index in horz_lines < r, default to -1
            r_prev = -1
            for hr in reversed(horz_lines):
                if hr < r:
                    r_prev = hr
                    break

            # Find largest index in vert_lines < c, default to -1
            c_prev = -1
            for vc in reversed(vert_lines):
                if vc < c:
                    c_prev = vc
                    break

            # Define the cell boundaries (exclusive of the lines themselves)
            # Rows: r_prev + 1 to r - 1
            # Cols: c_prev + 1 to c - 1
            cell_row_start = r_prev + 1
            cell_row_end = r # Slice is exclusive at end
            cell_col_start = c_prev + 1
            cell_col_end = c # Slice is exclusive at end

            # Check if cell dimensions are valid
            if cell_row_start < cell_row_end and cell_col_start < cell_col_end:
                # Extract the cell from the input grid
                cell = input_grid[cell_row_start:cell_row_end, cell_col_start:cell_col_end]

                # Check if the target color exists within this cell
                if np.any(cell == target_color):
                    # If yes, update the intersection point color in the output grid
                    output_grid[r, c] = target_color
            # If cell dimensions are invalid (e.g., adjacent gray lines),
            # or if target color not found, the intersection remains gray (already set)

    return output_grid.tolist()