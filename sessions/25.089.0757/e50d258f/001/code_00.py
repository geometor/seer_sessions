import numpy as np
from collections import deque

"""
Identify all distinct contiguous groups (objects) of non-white pixels (color > 0) in the input grid, considering diagonal adjacency.
Count the number of red pixels (color 2) within each object.
Select the object with the maximum count of red pixels. If there's a tie, choose the object whose topmost pixel is highest (minimum row index); if still tied, choose the one whose leftmost pixel is furthest left (minimum column index).
Determine the minimal rectangular bounding box enclosing the selected object.
Extract and return the subgrid corresponding to this bounding box from the input grid.
"""

def find_objects(grid):
    """
    Finds all distinct contiguous objects of non-white pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start a Breadth-First Search (BFS) for a new object
                current_object = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Keep track of top-left point for tie-breaking

                while q:
                    row, col = q.popleft()
                    current_object.append((row, col))

                    # Update top-left point
                    if row < min_r:
                        min_r = row
                        min_c = col
                    elif row == min_r and col < min_c:
                        min_c = col

                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = row + dr, col + dc

                            # Check bounds and if neighbor is part of the object and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] != 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if current_object:
                    # Store the object along with its top-left corner for tie-breaking
                    objects.append({'coords': current_object, 'top_left': (min_r, min_c)})
                    
    return objects

def count_color(grid, obj_coords, color_val):
    """
    Counts the occurrences of a specific color within an object's coordinates.

    Args:
        grid (np.array): The input grid.
        obj_coords (list): List of (row, col) tuples for the object.
        color_val (int): The color value to count.

    Returns:
        int: The count of the specified color.
    """
    count = 0
    for r, c in obj_coords:
        if grid[r, c] == color_val:
            count += 1
    return count

def get_bounding_box(obj_coords):
    """
    Calculates the minimal bounding box for a set of coordinates.

    Args:
        obj_coords (list): List of (row, col) tuples for the object.

    Returns:
        tuple: (min_row, min_col, max_row, max_col)
    """
    if not obj_coords:
        return None # Or handle as appropriate

    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    min_row = min(rows)
    min_col = min(cols)
    max_row = max(rows)
    max_col = max(cols)
    
    return min_row, min_col, max_row, max_col

def extract_subgrid(grid, bbox):
    """
    Extracts a subgrid based on bounding box coordinates.

    Args:
        grid (np.array): The input grid.
        bbox (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        np.array: The extracted subgrid.
    """
    min_row, min_col, max_row, max_col = bbox
    return grid[min_row : max_row + 1, min_col : max_col + 1]


def transform(input_grid):
    """
    Transforms the input grid by finding the object with the most red pixels (2),
    handling ties by top-left position, and extracting its bounding box.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid (extracted subgrid).
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Find all distinct non-white objects
    objects = find_objects(grid_np)

    if not objects:
        # Handle cases with no non-white pixels if necessary
        # Returning an empty grid or the original might be options.
        # Based on examples, seems there's always at least one object.
        return [] # Return empty list for empty grid representation

    # 2. Count red (2) pixels for each object and find the best object
    best_object_info = None
    max_red_count = -1

    for obj_info in objects:
        obj_coords = obj_info['coords']
        top_left = obj_info['top_left']
        
        # 3. Count red pixels
        red_count = count_color(grid_np, obj_coords, 2)

        # 4. Compare with current best
        if red_count > max_red_count:
            max_red_count = red_count
            best_object_info = obj_info
        elif red_count == max_red_count:
            # Tie-breaking: compare top-left corners
            current_best_top_left = best_object_info['top_left']
            if top_left[0] < current_best_top_left[0]: # Higher row (smaller index)
                best_object_info = obj_info
            elif top_left[0] == current_best_top_left[0]: # Same row
                if top_left[1] < current_best_top_left[1]: # Further left column (smaller index)
                    best_object_info = obj_info

    if best_object_info is None:
         # This case might happen if there are objects but none contain red pixels.
         # The logic above should still select the top-leftmost object among those with 0 reds.
         # If objects list was empty, already handled. Let's assume the logic selects one.
         # If for some reason it's still None (e.g., error in logic), return empty.
         # Re-evaluating: The loop initializes max_red_count to -1.
         # If all objects have 0 red pixels, the first object encountered will set max_red_count=0
         # and become the best_object_info. Subsequent objects with 0 red pixels will be compared
         # using the tie-breaker. So best_object_info should not be None if objects list is not empty.
         pass # Should have a best object selected by now if objects existed.

    # 5. Get bounding box of the selected object
    best_object_coords = best_object_info['coords']
    bbox = get_bounding_box(best_object_coords)
    
    # 6. Extract the subgrid
    output_grid_np = extract_subgrid(grid_np, bbox)
    
    # Convert back to list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid