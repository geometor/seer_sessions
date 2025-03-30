import numpy as np
from collections import deque

"""
Identifies hollow blue (1) shapes enclosing an azure (8) region (hole) on an azure background.
For each such identified hole:
1. Calculates the center row and column of the hole's bounding box.
2. Draws magenta (6) lines horizontally across the center row and vertically down the center column.
3. These lines only replace pixels that were originally azure (8) in the input grid.
4. The original blue (1) pixels forming the shape are preserved.
"""

def _find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a single connected object.
                   Returns an empty list if no objects are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)]) # Queue for BFS
                visited[r, c] = True

                # Perform BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # If neighbor is the target color and not visited
                                if grid[nr, nc] == color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                # Add the found object's coordinates to the list if it's not empty
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def _get_bounding_box(coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) 
    for a non-empty set of coordinates.
    
    Args:
        coords (set): A set of (row, col) tuples. Assumes coords is not empty.

    Returns:
        tuple: (min_row, min_col, max_row, max_col)
    """
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid):
    """
    Transforms the input grid by finding azure holes enclosed by blue shapes
    and drawing magenta lines through the center of each hole.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The transformed 2D output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Define colors used in the task
    background_color = 8 # Azure (also the color of the hole)
    object_color = 1     # Blue (color of the enclosing shape)
    line_color = 6       # Magenta (color of the lines to draw)

    # Find all connected regions of the background/hole color (azure)
    potential_holes = _find_objects(input_grid, background_color)

    # Iterate through each potential hole found
    for hole_coords in potential_holes:
        # Skip if the set of coordinates is empty (shouldn't happen with _find_objects)
        if not hole_coords:
            continue

        is_enclosed = True
        all_neighbors = set()

        # --- Step 1: Check if the potential hole touches the grid border ---
        # If any part of the hole is on the edge, it cannot be enclosed.
        for r, c in hole_coords:
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                is_enclosed = False
                break
        # If it touches the border, skip to the next potential hole
        if not is_enclosed:
            continue 

        # --- Step 2: Find all unique neighbors surrounding the hole ---
        # Neighbors are defined by 8-connectivity (includes diagonals).
        for r, c in hole_coords:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip the center cell itself
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    # Ensure neighbor coordinates are within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                         neighbor_coord = (nr, nc)
                         # Add neighbor to the set only if it's NOT part of the hole itself
                         if neighbor_coord not in hole_coords:
                             all_neighbors.add(neighbor_coord)

        # --- Step 3: Check if all surrounding neighbors are of the object_color (blue) ---
        # If the set of neighbors is empty, something is wrong (this check handles edge cases,
        # though it shouldn't be empty if Step 1 passed).
        if not all_neighbors:
             is_enclosed = False
        else:
            # Check the color of each neighbor pixel in the original input grid
            for nr, nc in all_neighbors:
                # If any neighbor is NOT the expected object color (blue),
                # then this azure region is not properly enclosed by blue.
                if input_grid[nr, nc] != object_color:
                    is_enclosed = False
                    break

        # --- Step 4: If the hole is confirmed to be enclosed, draw the lines ---
        if is_enclosed:
            # Calculate the bounding box of the hole coordinates
            min_r, min_c, max_r, max_c = _get_bounding_box(hole_coords)
            
            # Calculate the center row and column using integer division
            center_row = (min_r + max_r) // 2
            center_col = (min_c + max_c) // 2

            # Draw the horizontal magenta line across the center row
            # Important: Only change pixels in the output grid if the corresponding
            # pixel in the *input* grid was the background color (azure).
            # This prevents overwriting the original blue shape pixels.
            for c in range(width):
                if input_grid[center_row, c] == background_color:
                    output_grid[center_row, c] = line_color

            # Draw the vertical magenta line down the center column
            # Apply the same condition: only replace original background pixels.
            for r in range(height):
                if input_grid[r, center_col] == background_color:
                    output_grid[r, center_col] = line_color

    # Return the final modified grid
    return output_grid