import numpy as np

"""
This transformation identifies two distinct non-zero patterns in the input grid. 
One pattern, composed of the digit '8', forms a hollow rectangular "frame". 
The other pattern, composed of different non-zero digits, is the "content".
The transformation copies the "content" pattern into the hollow interior of the "frame" pattern.

1. Identify the coordinates of all cells belonging to the "frame" (value 8).
2. Identify the coordinates of all cells belonging to the "content" pattern (non-zero, non-8 values).
3. Calculate the bounding box of the "frame" pattern.
4. Calculate the bounding box of the "content" pattern.
5. Determine the top-left corner of the area *inside* the frame (assumed to be one cell inwards from the frame's top-left bounding box corner).
6. Create a copy of the input grid to serve as the output grid.
7. Iterate through the cells within the "content" pattern's bounding box in the input grid.
8. For each cell that belongs to the "content" pattern (non-zero, non-8 value):
    a. Calculate its relative position within the "content" pattern's bounding box.
    b. Determine the corresponding target position in the output grid by adding the relative position to the top-left corner of the frame's interior.
    c. Place the "content" cell's value at the calculated target position in the output grid, overwriting the existing value.
9. Return the modified output grid.
"""

def find_pattern_coords(grid, value=None, exclude_values=None):
    """Finds coordinates of cells matching specific criteria."""
    coords = []
    rows, cols = grid.shape
    if exclude_values is None:
        exclude_values = []

    for r in range(rows):
        for c in range(cols):
            cell_value = grid[r, c]
            if value is not None:
                if cell_value == value:
                    coords.append((r, c))
            elif cell_value != 0 and cell_value not in exclude_values:
                 coords.append((r, c))
    return coords

def get_bounding_box(coords):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a list of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Identifies a frame (value 8) and a content pattern (other non-zeros) in the
    input grid, and copies the content pattern into the frame's interior.
    """
    # Convert input to numpy array for easier slicing and manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find coordinates of the frame (value 8)
    frame_coords = find_pattern_coords(grid, value=8)

    # Find coordinates of the content pattern (non-zero, non-8)
    content_coords = find_pattern_coords(grid, exclude_values=[0, 8])

    # Proceed only if both patterns are found
    if not frame_coords or not content_coords:
        # If either pattern is missing, return the original grid
        return output_grid.tolist()

    # Calculate bounding boxes
    frame_bbox = get_bounding_box(frame_coords)
    content_bbox = get_bounding_box(content_coords)

    if not frame_bbox or not content_bbox:
         # Should not happen if coords lists are not empty, but good practice
         return output_grid.tolist()

    frame_r_min, frame_c_min, _, _ = frame_bbox
    content_r_min, content_c_min, content_r_max, content_c_max = content_bbox

    # Determine the top-left corner of the frame's interior
    # Assumption: Interior starts one cell inside the frame's bounding box
    interior_r0 = frame_r_min + 1
    interior_c0 = frame_c_min + 1

    # Iterate through the bounding box of the content pattern in the input grid
    for r in range(content_r_min, content_r_max + 1):
        for c in range(content_c_min, content_c_max + 1):
            # Get the value from the original grid
            value = grid[r, c]

            # Check if this cell is part of the content pattern (non-zero and not 8)
            if value != 0 and value != 8:
                # Calculate relative position within the content pattern's bounding box
                rel_r = r - content_r_min
                rel_c = c - content_c_min

                # Calculate target position in the output grid within the frame's interior
                target_r = interior_r0 + rel_r
                target_c = interior_c0 + rel_c

                # Check if target position is within the grid bounds before writing
                if 0 <= target_r < rows and 0 <= target_c < cols:
                    # Place the content value into the output grid
                    output_grid[target_r, target_c] = value

    # Convert the result back to a list of lists
    return output_grid.tolist()