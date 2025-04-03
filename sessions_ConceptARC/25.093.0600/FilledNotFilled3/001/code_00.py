import numpy as np
from collections import deque

"""
Identifies shapes in the input grid that enclose a distinct inner region
and outputs the content of that region. A shape is a connected component
of identical non-zero digits (4-way connectivity). If an enclosed region
is found, its content (either a single digit or a subgrid defined by the
minimal bounding box around the enclosed cells) is returned. The process stops
after the first enclosing shape is found and processed.
"""

def find_shape(grid, start_r, start_c, visited):
    """
    Finds the connected component (shape) of a non-zero digit using BFS.
    Uses 4-way connectivity. Updates the visited array.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        visited (np.array): Boolean array tracking visited cells for shape finding.

    Returns:
        set: A set of (row, col) tuples representing the coordinates of the shape.
             Returns an empty set if the start cell is 0 or already visited.
    """
    rows, cols = grid.shape
    digit = grid[start_r, start_c]
    # Basic check: Don't start search on background or already visited cells
    if digit == 0 or visited[start_r, start_c]:
        return set()

    shape_coords = set()
    q = deque([(start_r, start_c)])
    visited[start_r, start_c] = True  # Mark the starting cell as visited
    shape_coords.add((start_r, start_c))

    while q:
        r, c = q.popleft()
        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor has the same digit and hasn't been visited yet
                if grid[nr, nc] == digit and not visited[nr, nc]:
                    visited[nr, nc] = True  # Mark neighbor as visited
                    shape_coords.add((nr, nc)) # Add neighbor to the shape
                    q.append((nr, nc)) # Add neighbor to the queue for further exploration
    return shape_coords

def check_enclosure_and_extract(grid, shape_coords):
    """
    Checks if a given shape encloses a region and extracts the content
    of the enclosed region. Enclosure is determined by checking reachability
    from the grid border without crossing the shape.

    Args:
        grid (np.array): The input grid.
        shape_coords (set): Set of (row, col) tuples for the shape's cells.

    Returns:
        int or list[list[int]] or None:
            - int: If a single cell is enclosed.
            - list[list[int]]: If multiple cells form an enclosed region (returns the bounding box content).
            - None: If the shape does not enclose any region.
    """
    rows, cols = grid.shape
    if not shape_coords: # Should not happen if called correctly, but safe check
        return None

    # 1. Determine Bounding Box of the shape
    # This helps to quickly identify potential internal cells.
    min_r = min(r for r, c in shape_coords)
    max_r = max(r for r, c in shape_coords)
    min_c = min(c for r, c in shape_coords)
    max_c = max(c for r, c in shape_coords)

    # 2. Identify Potential Inner Cells
    # These are cells strictly inside the bounding box that are not part of the shape itself.
    potential_inner_coords = set()
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            coord = (r, c)
            if coord not in shape_coords:
                potential_inner_coords.add(coord)

    # If there are no cells inside the bounding box (other than the shape itself),
    # it cannot enclose anything.
    if not potential_inner_coords:
        return None

    # 3. Flood fill (BFS) from the outside border
    # This identifies all cells reachable from the outside without crossing the shape.
    outside_visited = set()
    q_border = deque()

    # Initialize the queue with all border cells that are NOT part of the shape.
    # These are the starting points for the "outside" region.
    for r in range(rows):
        for c in [0, cols - 1]: # Left and Right borders
             coord = (r,c)
             if coord not in shape_coords and coord not in outside_visited:
                q_border.append(coord)
                outside_visited.add(coord)
    for c in range(1, cols - 1): # Top and Bottom borders (excluding corners already added)
        for r in [0, rows - 1]:
            coord = (r,c)
            if coord not in shape_coords and coord not in outside_visited:
               q_border.append(coord)
               outside_visited.add(coord)

    # Perform BFS starting from the border cells
    while q_border:
        r, c = q_border.popleft()
        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            coord = (nr, nc)
            # Check bounds, ensure the neighbor is NOT part of the blocking shape,
            # and hasn't been visited by this 'outside' flood fill yet.
            if 0 <= nr < rows and 0 <= nc < cols and \
               coord not in shape_coords and \
               coord not in outside_visited:
                outside_visited.add(coord)
                q_border.append(coord)

    # 4. Identify Enclosed Cells
    # Enclosed cells are those potential inner cells that were NOT reached by the flood fill from the outside.
    enclosed_coords = set()
    for coord in potential_inner_coords:
        if coord not in outside_visited:
            enclosed_coords.add(coord)

    # If no potential inner cells were determined to be enclosed, return None.
    if not enclosed_coords:
        return None

    # 5. Extract Content based on the identified enclosed cells
    # Determine the bounding box of the *enclosed* region itself.
    enclosed_min_r = min(r for r, c in enclosed_coords)
    enclosed_max_r = max(r for r, c in enclosed_coords)
    enclosed_min_c = min(c for r, c in enclosed_coords)
    enclosed_max_c = max(c for r, c in enclosed_coords)

    # Check if it's a single cell enclosure (like examples 1 and 3)
    if len(enclosed_coords) == 1 and enclosed_min_r == enclosed_max_r and enclosed_min_c == enclosed_max_c:
         # Safely extract the single value using .item()
        return grid[enclosed_min_r, enclosed_min_c].item()
    else:
        # Extract the rectangular subgrid defined by the bounding box of the enclosed cells.
        # This matches example 2 where a 2x2 area of 0s is enclosed.
        output_grid_np = grid[enclosed_min_r : enclosed_max_r + 1, enclosed_min_c : enclosed_max_c + 1]
        # Return as NumPy array (will be converted to list of lists later if needed)
        return output_grid_np

def transform(input_grid):
    """
    Identifies shapes in the input grid that enclose a distinct inner region
    and outputs the content of that region. A shape is a connected component
    of identical non-zero digits (4-way connectivity). If an enclosed region
    is found, its content (either a single digit or a subgrid) is returned.
    The process stops after the first enclosing shape is found and processed.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        int or list[list[int]] or None:
            - int: If a single cell is enclosed.
            - list[list[int]]: If multiple cells form an enclosed region.
            - None: If no enclosing shape is found in the grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    # Keep track of visited cells during shape finding to avoid processing the same shape multiple times
    visited_shape_finding = np.zeros_like(grid_np, dtype=bool)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If we find a non-zero cell that hasn't been visited yet, it's the start of a new shape
            if grid_np[r, c] != 0 and not visited_shape_finding[r, c]:
                # Find all connected cells belonging to this shape
                current_shape_coords = find_shape(grid_np, r, c, visited_shape_finding)

                # If a valid shape was identified (find_shape returns non-empty set)
                if current_shape_coords:
                    # Check if this shape encloses any region and get the content if it does
                    enclosed_content = check_enclosure_and_extract(grid_np, current_shape_coords)

                    # If enclosed_content is found (not None), we've found our answer.
                    if enclosed_content is not None:
                        # If the content is a NumPy array (subgrid), convert it to list of lists
                        if isinstance(enclosed_content, np.ndarray):
                            return enclosed_content.tolist()
                        else:
                            # If it's a single value (int), return it directly
                            return enclosed_content

    # If the loops complete without finding any enclosing shape, return None.
    return None