import numpy as np
from collections import deque

"""
Identifies all distinct contiguous non-white objects (using 8-way connectivity) 
in the input grid. Verifies that exactly two objects exist. Selects the object 
whose topmost pixel has the minimum row index (appears higher in the grid). 
Creates a new output grid containing only the selected object, cropped to its 
minimal bounding box. Pixels within the bounding box but not part of the 
selected object are set to white (0).
"""

def find_objects_8_way(grid):
    """
    Finds all contiguous objects (8-way connectivity) of non-white pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'pixels' (set of (r, c) tuples),
              'bbox' (min_row, min_col, max_row, max_col), and 'top_row'.
              Returns an empty list if no non-white pixels are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Define 8 directions for connectivity check
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # Start BFS if a non-white, unvisited pixel is found
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search (BFS)
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))

                    # Update bounding box and find minimum row (top_row)
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (8-directional)
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds, has the same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store object details
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'top_row': min_r
                })
                
    return objects

def crop_object(grid, obj):
    """
    Creates a new grid containing only the specified object, cropped to its bounding box.
    Pixels within the bounding box not belonging to the object are white (0).

    Args:
        grid (np.array): The original input grid (used to get object colors).
        obj (dict): The object dictionary containing 'pixels' and 'bbox'.

    Returns:
        np.array: The cropped output grid.
    """
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Initialize output grid with background color (white, 0)
    output_grid = np.zeros((height, width), dtype=int)

    # Copy object pixels to the output grid, adjusting coordinates
    for r, c in obj['pixels']:
        # Calculate relative position in the cropped grid
        output_r = r - min_r
        output_c = c - min_c
        # Ensure coordinates are within the bounds of the new grid (should always be true)
        if 0 <= output_r < height and 0 <= output_c < width:
             # Use the color from the original grid
             output_grid[output_r, output_c] = grid[r, c] 

    return output_grid

def transform(input_grid):
    """
    Transforms the input grid by selecting the highest object and cropping it.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid. Returns an empty list if not 
                       exactly two objects are found.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Find all distinct non-white objects using 8-way connectivity
    objects = find_objects_8_way(grid_np)

    # Verify that exactly two objects were found, as per task constraints
    if len(objects) != 2:
        # Handle unexpected number of objects (return empty or raise error)
        # Based on training examples, this case assumes valid input has 2 objects.
        # Returning empty list seems safer than potentially wrong output.
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning empty grid.")
        return [[]] 

    # Determine the object with the minimum top_row index (the highest one)
    # The `min` function with a lambda key works perfectly here.
    selected_object = min(objects, key=lambda obj: obj['top_row'])

    # Create the output grid by cropping the selected object
    output_grid_np = crop_object(grid_np, selected_object)

    # Convert the resulting NumPy array back to a list of lists format
    output_grid = output_grid_np.tolist()

    return output_grid