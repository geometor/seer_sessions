```python
import numpy as np
from collections import deque

"""
Identifies an azure (color 8) frame containing a rectangular background (color 0) hole.
Identifies a pattern area defined by the bounding box of all non-background, non-azure pixels.
Extracts the subgrid corresponding to the pattern area (including background pixels within it).
Copies the input grid to the output grid, then pastes the extracted pattern subgrid into the hole location in the output grid, overwriting existing pixels.
"""

def find_azure_frame_and_hole(grid):
    """
    Finds the azure frame pixels and the bounding box of the enclosed background hole.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (frame_bbox, hole_bbox) dictionaries, or (None, None) if not found.
               Bounding boxes are {'min_row', 'min_col', 'max_row', 'max_col'}.
    """
    height, width = grid.shape
    # Find all pixels with the frame color (8)
    azure_pixels = set((r, c) for r in range(height) for c in range(width) if grid[r, c] == 8)

    if not azure_pixels:
        # Return None if no frame pixels exist
        return None, None 

    # Calculate the bounding box of the frame pixels
    min_r_frame = min(r for r, c in azure_pixels)
    max_r_frame = max(r for r, c in azure_pixels)
    min_c_frame = min(c for r, c in azure_pixels)
    max_c_frame = max(c for r, c in azure_pixels)
    frame_bbox = {'min_row': min_r_frame, 'min_col': min_c_frame, 'max_row': max_r_frame, 'max_col': max_c_frame}

    # Search for a rectangular hole (background color 0) within the frame's bounding box
    hole_bbox = None
    # Use a visited array to track pixels checked during hole search
    visited_hole_search = np.zeros((height, width), dtype=bool)

    # Iterate through pixels strictly inside the frame's bounding box
    for r_start in range(min_r_frame + 1, max_r_frame):
        for c_start in range(min_c_frame + 1, max_c_frame):
            # If a background pixel is found that hasn't been visited yet
            if grid[r_start, c_start] == 0 and not visited_hole_search[r_start, c_start]:
                # Start Breadth-First Search (BFS) from this pixel to find connected background area
                q = deque([(r_start, c_start)])
                visited_hole_search[r_start, c_start] = True
                current_hole_pixels = set([(r_start, c_start)])
                # Track the bounds of this connected background area
                min_r_hole, max_r_hole = r_start, r_start
                min_c_hole, max_c_hole = c_start, c_start

                while q:
                    r, c = q.popleft()
                    # Update the bounds
                    min_r_hole = min(min_r_hole, r)
                    max_r_hole = max(max_r_hole, r)
                    min_c_hole = min(min_c_hole, c)
                    max_c_hole = max(max_c_hole, c)

                    # Check 4 cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        # Check if neighbor is strictly inside the frame, is background, and hasn't been visited
                        if min_r_frame < nr < max_r_frame and \
                           min_c_frame < nc < max_c_frame and \
                           grid[nr, nc] == 0 and \
                           not visited_hole_search[nr, nc]:
                            visited_hole_search[nr, nc] = True
                            current_hole_pixels.add((nr, nc))
                            q.append((nr, nc))

                # After BFS, check if the found connected component forms a solid rectangle
                hole_height = max_r_hole - min_r_hole + 1
                hole_width = max_c_hole - min_c_hole + 1
                is_rectangular = True
                # Check if the number of pixels found matches the area of the bounding box
                if len(current_hole_pixels) != hole_height * hole_width:
                     is_rectangular = False
                else:
                    # Verify all pixels within the calculated bounding box are indeed background pixels found in this component
                    for r_check in range(min_r_hole, max_r_hole + 1):
                         for c_check in range(min_c_hole, max_c_hole + 1):
                              if grid[r_check, c_check] != 0 or (r_check, c_check) not in current_hole_pixels:
                                   is_rectangular = False
                                   break
                         if not is_rectangular:
                              break
                              
                if is_rectangular:
                    # If it is a solid rectangle, store its bounding box
                    hole_bbox = {'min_row': min_r_hole, 'min_col': min_c_hole, 'max_row': max_r_hole, 'max_col': max_c_hole}
                    # Assuming only one hole based on task examples, return immediately
                    return frame_bbox, hole_bbox

    # If the loops complete without finding a valid rectangular hole
    return frame_bbox, None


def find_pattern_area(grid):
    """
    Finds the minimal bounding box enclosing all pattern pixels (non-0, non-8).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: Bounding box dictionary {'min_row', 'min_col', 'max_row', 'max_col'}
              of the pattern area, or None if no pattern pixels are found.
    """
    height, width = grid.shape
    # Identify all pixels that are not background (0) and not frame color (8)
    pattern_pixels = set((r, c) for r in range(height) for c in range(width) if grid[r, c] != 0 and grid[r, c] != 8)

    if not pattern_pixels:
        # Return None if no such pixels exist
        return None 

    # Calculate the minimal bounding box containing all pattern pixels
    min_r_pattern = min(r for r, c in pattern_pixels)
    max_r_pattern = max(r for r, c in pattern_pixels)
    min_c_pattern = min(c for r, c in pattern_pixels)
    max_c_pattern = max(c for r, c in pattern_pixels)
    pattern_bbox = {'min_row': min_r_pattern, 'min_col': min_c_pattern, 'max_row': max_r_pattern, 'max_col': max_c_pattern}

    return pattern_bbox


def extract_subgrid(grid, bbox):
    """
    Extracts the subgrid defined by the bounding box. Includes all pixels within the box.

    Args:
        grid (np.ndarray): The source grid.
        bbox (dict): Bounding box dictionary {'min_row', 'min_col', 'max_row', 'max_col'}.

    Returns:
        np.ndarray: The extracted subgrid. Returns None if bbox is None.
    """
    if bbox is None:
        return None
    # Slice the grid using bounding box coordinates
    return grid[bbox['min_row']:bbox['max_row']+1, bbox['min_col']:bbox['max_col']+1]


def paste_subgrid(target_grid, subgrid, top_left_coord):
    """
    Pastes a subgrid onto a target grid at the specified top-left coordinate,
    overwriting existing pixels. Handles boundary checks.

    Args:
        target_grid (np.ndarray): The grid to paste onto (modified in place).
        subgrid (np.ndarray): The subgrid to paste.
        top_left_coord (tuple): (row, col) for the top-left corner of the paste location.
    """
    # Check for invalid inputs
    if subgrid is None or top_left_coord is None:
        print("Warning: Subgrid or paste coordinate is None. Skipping paste.")
        return

    start_row, start_col = top_left_coord
    sub_height, sub_width = subgrid.shape
    target_height, target_width = target_grid.shape

    # Iterate through each pixel in the subgrid
    for r in range(sub_height):
        for c in range(sub_width):
            # Calculate the corresponding coordinates in the target grid
            target_r, target_c = start_row + r, start_col + c
            # Check if the target coordinates are within the bounds of the target grid
            if 0 <= target_r < target_height and 0 <= target_c < target_width:
                # Overwrite the target grid pixel with the subgrid pixel
                target_grid[target_r, target_c] = subgrid[r, c]


def transform(input_grid):
    """
    Applies the transformation: finds an azure frame with a hole,
    finds the pattern area (bounding box of non-0, non-8 pixels),
    extracts the pattern subgrid, and pastes it into the hole.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Step 1: Find the azure frame and the rectangular background hole inside it.
    frame_bbox, hole_bbox = find_azure_frame_and_hole(input_grid)

    # Step 2: Find the minimal bounding box containing all pattern pixels (non-0, non-8).
    pattern_bbox = find_pattern_area(input_grid)

    # Step 3: Check if the frame, hole, and pattern area were all successfully found.
    if frame_bbox is None or hole_bbox is None or pattern_bbox is None:
        # If any component is missing, return the original grid without modification.
        # print("Warning: Could not find frame, hole, or pattern area. Returning input.")
        return output_grid

    # Step 4: Extract the rectangular subgrid corresponding to the pattern area.
    # This includes all pixels (including background) within the pattern's bounding box.
    pattern_subgrid = extract_subgrid(input_grid, pattern_bbox)

    # Step 5: Check if pattern subgrid was extracted (should be valid if pattern_bbox was found).
    if pattern_subgrid is None:
        #  print("Warning: Failed to extract pattern subgrid. Returning input.")
         return output_grid # Should not happen if pattern_bbox is not None
         
    # Step 6: Determine the top-left coordinate for pasting (the top-left corner of the hole).
    paste_coord = (hole_bbox['min_row'], hole_bbox['min_col'])

    # Step 7: Check if the dimensions of the pattern subgrid match the hole dimensions (as observed in examples).
    hole_height = hole_bbox['max_row'] - hole_bbox['min_row'] + 1
    hole_width = hole_bbox['max_col'] - hole_bbox['min_col'] + 1
    pattern_height, pattern_width = pattern_subgrid.shape

    # This check is based on observations from examples; if sizes don't match, the task might be different.
    if pattern_height != hole_height or pattern_width != hole_width:
        print(f"Warning: Pattern subgrid ({pattern_height}x{pattern_width}) dimensions do not match hole ({hole_height}x{hole_width}). Behavior may be unexpected.")
        # Proceeding with paste anyway, aligned at top-left.

    # Step 8: Paste the extracted pattern subgrid onto the output grid.
    # The paste starts at the top-left corner of the hole.
    # All pixels from pattern_subgrid (including background 0s) overwrite the hole area.
    paste_subgrid(output_grid, pattern_subgrid, paste_coord)

    # Step 9: Return the modified grid.
    return output_grid
```