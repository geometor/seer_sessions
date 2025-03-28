import numpy as np
from collections import deque

"""
Identifies all separate non-background objects in the input grid.
For each object, counts the number of unique colors it contains.
Selects the object with the maximum number of unique colors.
Returns a new grid containing only the selected object, cropped to its bounding box.
"""

# Helper function using BFS to find one connected object and its properties
def find_one_object(grid, start_r, start_c, visited):
    """
    Finds a single connected object starting from (start_r, start_c) using BFS.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row.
        start_c (int): Starting column.
        visited (np.array): Boolean array marking visited cells.

    Returns:
        tuple: (list_of_coords, unique_color_count)
               list_of_coords is a list of (row, col) tuples for the object.
               unique_color_count is the number of distinct non-zero colors in the object.
               Returns ([], 0) if the starting cell is background or already visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_r < rows and 0 <= start_c < cols) or \
       visited[start_r, start_c] or grid[start_r, start_c] == 0:
        return [], 0

    q = deque([(start_r, start_c)])
    object_coords = []
    object_colors = set()
    visited[start_r, start_c] = True

    while q:
        r, c = q.popleft()
        object_coords.append((r, c))
        color = grid[r, c]
        # Add color to set (set handles uniqueness automatically)
        object_colors.add(color) 

        # Explore 4-way neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if neighbor is non-background and not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and grid[nr, nc] != 0:
                visited[nr, nc] = True
                q.append((nr, nc))

    # We are counting non-background colors, so if 0 was somehow added (it shouldn't be), remove it.
    # However, the search condition grid[nr, nc] != 0 prevents this.
    # The count is simply the size of the set.
    return object_coords, len(object_colors)

# Helper function to get the bounding box of a set of coordinates
def get_bounding_box(coords):
    """
    Calculates the minimum bounding box for a list of coordinates.

    Args:
        coords (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_r, min_c, max_r, max_c) or None if coords is empty.
    """
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

# Helper function to extract a subgrid based on a bounding box
def extract_subgrid(grid, bbox):
    """
    Extracts a subgrid from the grid using the bounding box.

    Args:
        grid (np.array): The main grid.
        bbox (tuple): (min_r, min_c, max_r, max_c).

    Returns:
        np.array: The extracted subgrid. Returns empty array if bbox is None.
    """
    if bbox is None:
        # Return an empty numpy array with appropriate shape if needed,
        # or handle based on expected behavior for "no object found".
        # For ARC, returning an empty list of lists might be represented as np.array([]).shape -> (0,)
        # Let's return a 0x0 array for consistency.
         return np.array([[]]).reshape(0,0) 
    min_r, min_c, max_r, max_c = bbox
    # Slice numpy array: upper bound is exclusive, so add 1
    return grid[min_r:max_r+1, min_c:max_c+1]


def transform(input_grid):
    """
    Identifies all separate non-background objects in the input grid.
    For each object, counts the number of unique colors it contains.
    Selects the object with the maximum number of unique colors.
    Returns a new grid containing only the selected object, cropped to its bounding box.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    # Keep track of visited cells during object search
    visited = np.zeros_like(input_grid_np, dtype=bool)

    max_unique_colors = -1
    best_object_bbox = None

    # Iterate through each cell to find starting points of objects
    for r in range(rows):
        for c in range(cols):
            # If cell is part of an object and not yet visited
            if input_grid_np[r, c] != 0 and not visited[r, c]:
                # Find the complete object starting from this cell
                object_coords, unique_color_count = find_one_object(input_grid_np, r, c, visited)

                # If this object has more unique colors than the best found so far
                if unique_color_count > max_unique_colors:
                    max_unique_colors = unique_color_count
                    # Store the bounding box of this new best object
                    best_object_bbox = get_bounding_box(object_coords)
                
                # Note: Tie-breaking is implicitly handled by taking the first object
                # found with the maximum number of unique colors. If the problem
                # required a different tie-breaking rule (e.g., largest area, topmost),
                # additional logic would be needed here inside an `elif unique_color_count == max_unique_colors:` block.

    # After checking all cells, extract the subgrid of the best object
    if best_object_bbox:
        output_grid_np = extract_subgrid(input_grid_np, best_object_bbox)
    else:
        # Handle case where no non-background object is found
        # Return an empty grid as per ARC conventions (empty list of lists)
        output_grid_np = np.array([[]]).reshape(0,0) 

    # Convert the final numpy array back to a list of lists
    return output_grid_np.tolist()
