import numpy as np
from collections import deque

def find_coords_of_color(grid, color):
    """Finds all coordinates (row, col) of a given color in the grid."""
    coords = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                coords.append((r, c))
    return coords

def find_primary_color(grid):
    """Finds the first color in the grid that is not white (0) or gray (5)."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color != 5:
                return color
    return None # Should not happen based on task description

def find_contiguous_object(grid, start_coords_set, target_color):
    """
    Finds all connected pixels of target_color starting from any coordinate
    in start_coords_set using Breadth-First Search (BFS).
    Includes the start_coords themselves if they match the target_color.
    """
    if not start_coords_set:
        return set()

    rows, cols = grid.shape
    object_coords = set()
    queue = deque()
    visited = set()

    # Initialize queue and visited with starting coordinates
    # that actually match the target color
    for r, c in start_coords_set:
         if 0 <= r < rows and 0 <= c < cols and grid[r,c] == target_color and (r,c) not in visited:
            queue.append((r, c))
            visited.add((r,c))

    while queue:
        r, c = queue.popleft()
        object_coords.add((r, c))

        # Check 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip self

                nr, nc = r + dr, c + dc

                # Check bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if neighbor has target color and hasn't been visited
                    if grid[nr, nc] == target_color and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))

    return object_coords


def transform(input_grid):
    """
    Transforms the input grid based on the following logic:
    1. Finds the single gray pixel (5).
    2. Determines the primary color (non-white, non-gray).
    3. Identifies the primary color object adjacent (including diagonals) to the gray pixel.
    4. Calculates the bounding box of this selected object.
    5. Creates an output grid matching the bounding box size.
    6. Copies the shape of the selected object into the output grid, relative to its top-left corner.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Find the single gray pixel (5)
    gray_coords_list = find_coords_of_color(grid, 5)
    if not gray_coords_list:
        # Handle error: No gray pixel found (though task implies one exists)
        return [] # Or raise an error
    gray_r, gray_c = gray_coords_list[0]

    # 2. Determine the primary color
    primary_color = find_primary_color(grid)
    if primary_color is None:
        # Handle error: No primary color found
        return [] # Or raise an error

    # 3. Identify the primary color object adjacent to the gray pixel
    # Find initial neighbors of the gray pixel that have the primary color
    start_primary_coords = set()
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = gray_r + dr, gray_c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == primary_color:
                start_primary_coords.add((nr, nc))

    # Find the full contiguous object starting from these neighbors
    selected_object_coords = find_contiguous_object(grid, start_primary_coords, primary_color)

    if not selected_object_coords:
         # Handle case where gray is not adjacent to any primary color pixel
         # Based on examples, this shouldn't happen. If it does, return empty grid?
         # Or maybe the gray pixel itself defines a 1x1 object if no neighbors?
         # Let's assume based on examples an adjacent object is always found.
         # If this assumption is wrong, the code might need adjustment.
         # For now, return an empty grid if no object found.
         return []


    # 4. Calculate the minimum bounding box
    min_r = min(r for r, c in selected_object_coords)
    max_r = max(r for r, c in selected_object_coords)
    min_c = min(c for r, c in selected_object_coords)
    max_c = max(c for r, c in selected_object_coords)

    # 5. Determine the height and width and create the output grid
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    output_grid = np.zeros((height, width), dtype=int) # Fill with white (0)

    # 6. Map the selected object pixels to the output grid
    for r, c in selected_object_coords:
        relative_r = r - min_r
        relative_c = c - min_c
        output_grid[relative_r, relative_c] = primary_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()