import numpy as np
from collections import defaultdict

"""
Transformation Rule:

1. Identify two parallel lines (walls) made of the same non-zero digit, either horizontally or vertically.
2. Identify a single, unique non-zero digit (marker) different from the wall digit.
3. Calculate the midpoint row (for horizontal walls) or midpoint column (for vertical walls) between the two walls using integer division.
4. Move the marker to the cell located at the midpoint index along the axis perpendicular to the walls, keeping its coordinate along the axis parallel to the walls unchanged.
5. The original cell of the marker is set to 0 (background).
6. All other cells (walls and background) remain unchanged.
"""

def _find_walls_and_marker(grid):
    """
    Finds the wall lines (horizontal or vertical), the wall value,
    the marker value, and the marker's initial position.
    """
    rows, cols = grid.shape
    non_zero_positions = defaultdict(list)
    row_counts = defaultdict(int)
    col_counts = defaultdict(int)
    all_non_zero = {} # Store value and position for potential markers

    # First pass: collect positions and counts for non-zero values
    for r in range(rows):
        for c in range(cols):
            val = grid[r, c]
            if val != 0:
                non_zero_positions[val].append((r, c))
                row_counts[(val, r)] += 1
                col_counts[(val, c)] += 1
                all_non_zero[(r,c)] = val

    wall_value = -1
    wall_orientation = None
    wall_indices = []
    marker_value = -1
    marker_pos = None

    # Identify walls
    for val, positions in non_zero_positions.items():
        # Check for horizontal walls
        val_rows = defaultdict(int)
        for r, c in positions:
            val_rows[r] += 1
        
        horizontal_lines = []
        for r, count in val_rows.items():
            if count == cols: # Check if it spans the full width
                 horizontal_lines.append(r)

        if len(horizontal_lines) == 2:
            wall_value = val
            wall_orientation = 'horizontal'
            wall_indices = sorted(horizontal_lines)
            break # Found walls

        # Check for vertical walls
        val_cols = defaultdict(int)
        for r, c in positions:
            val_cols[c] += 1

        vertical_lines = []
        for c, count in val_cols.items():
             if count == rows: # Check if it spans the full height
                 vertical_lines.append(c)

        if len(vertical_lines) == 2:
            wall_value = val
            wall_orientation = 'vertical'
            wall_indices = sorted(vertical_lines)
            break # Found walls

    if wall_value == -1:
        raise ValueError("Could not identify two parallel walls.")

    # Identify marker (the non-zero value that is NOT the wall value)
    for pos, val in all_non_zero.items():
        if val != wall_value:
            if marker_value != -1:
                 raise ValueError("Found more than one potential marker.")
            marker_value = val
            marker_pos = pos

    if marker_value == -1:
         raise ValueError("Could not identify the marker.")

    return wall_value, wall_orientation, wall_indices, marker_value, marker_pos


def _calculate_target_position(wall_orientation, wall_indices, marker_pos):
    """Calculates the target position for the marker."""
    row_in, col_in = marker_pos
    if wall_orientation == 'horizontal':
        r1, r2 = wall_indices
        row_target = (r1 + r2) // 2
        col_target = col_in
    elif wall_orientation == 'vertical':
        c1, c2 = wall_indices
        row_target = row_in
        col_target = (c1 + c2) // 2
    else:
        raise ValueError(f"Invalid wall orientation: {wall_orientation}")
    return row_target, col_target


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Moves a marker digit towards the midpoint between two parallel wall lines.
    """
    # Convert input list of lists to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = grid.copy()

    # 1. & 2. Identify Walls and Marker
    wall_value, wall_orientation, wall_indices, marker_value, marker_pos = _find_walls_and_marker(grid)
    row_in, col_in = marker_pos

    # 3. Calculate Target Position
    row_target, col_target = _calculate_target_position(wall_orientation, wall_indices, marker_pos)

    # 4. & 5. Move Marker in the output grid
    # Set original marker position to background (0)
    output_grid[row_in, col_in] = 0
    # Set target position to marker value
    output_grid[row_target, col_target] = marker_value

    # 6. Return the modified grid (converted back to list of lists if necessary)
    return output_grid.tolist()
