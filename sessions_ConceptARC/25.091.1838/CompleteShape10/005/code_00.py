import numpy as np
from collections import deque

"""
Fill horizontal gaps within each row, bounded by the horizontal extent
(minimum to maximum column) of the largest non-background object's pixels
present in that specific row. The gaps are filled with the color of the 
largest non-background object.
"""

def _find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors using BFS.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color designated as background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'pixels' (set of (r, c) tuples), and 'size'.
              Returns an empty list if no non-background objects are found.
              Returns None if grid is empty or invalid.
    """
    # Check for empty or invalid grid early
    if grid is None or grid.size == 0:
        # print("Warning: Input grid is None or empty.")
        return None
    # Ensure grid is 2D numpy array
    if grid.ndim != 2:
         # print(f"Warning: Input grid is not 2D (shape: {grid.shape}).")
         return None 
    
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-background pixel and not visited yet, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                obj_color = grid[r, c]
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Add the found object to the list
                if current_object_pixels:
                    objects.append({
                        'color': obj_color,
                        'pixels': current_object_pixels, 
                        'size': len(current_object_pixels)
                    })
                    
    return objects

def transform(input_grid):
    """
    Applies the horizontal gap filling transformation to the input grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    try:
        input_np = np.array(input_grid, dtype=int)
        if input_np.ndim != 2:
             # Return original potentially invalid input if not 2D
             # print("Warning: Input grid is not 2D.")
             return input_grid 
    except ValueError:
        # Handle non-rectangular lists etc.
        # print("Warning: Input grid could not be converted to NumPy array (e.g., non-rectangular).")
        return input_grid # Return original input on conversion error

    rows, cols = input_np.shape
    if rows == 0 or cols == 0:
        # print("Warning: Input grid is empty.")
        return input_grid # Handle empty grid case

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Step 1: Identify background color (assuming 0 based on examples/ARC convention)
    # In ARC tasks, background is almost always 0 (black/white confusion here, but value is 0).
    background_color = 0 
    # Alternate: find most frequent color - more robust but maybe not needed for ARC
    # colors, counts = np.unique(input_np, return_counts=True)
    # if counts.size > 0:
    #     background_color = colors[np.argmax(counts)]
    # else: # Grid was empty or single color
    #      return output_grid.tolist() 

    # Step 2: Find all non-background objects using the helper function
    objects = _find_objects(input_np, background_color)

    # If no non-background objects found (or grid was invalid), return the original grid
    if not objects:
        # print("No non-background objects found.")
        return output_grid.tolist() 

    # Step 3: Find the largest object (by pixel count) to determine the fill color
    largest_object = max(objects, key=lambda obj: obj['size'])
    fill_color = largest_object['color']
    
    # Step 4: Iterate through each row of the grid
    for r in range(rows):
        # Step 5: Find all column indices where the *input* grid has the *fill_color* in the current row
        row_pixels_indices = np.where(input_np[r, :] == fill_color)[0]

        # Step 6: Check if the fill_color was present in this row
        if len(row_pixels_indices) > 0:
            # Determine the horizontal extent (minimum and maximum column indices) of the fill_color in this row
            min_col = np.min(row_pixels_indices)
            max_col = np.max(row_pixels_indices)

            # Step 7: Fill background pixels within this horizontal extent in the output grid
            # Iterate through columns from min_col to max_col (inclusive)
            for c in range(min_col, max_col + 1):
                # Check if the pixel at (r, c) in the *original input* grid was the background color
                if input_np[r, c] == background_color:
                    # If it was background, change its color to the fill_color in the *output* grid
                    output_grid[r, c] = fill_color

    # Convert the final numpy array back to list of lists format for the ARC standard output
    return output_grid.tolist()