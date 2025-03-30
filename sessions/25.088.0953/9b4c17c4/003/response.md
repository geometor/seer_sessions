```python
import numpy as np
from collections import deque

"""
Identifies contiguous red objects (color 2) within distinct background regions 
(color 1 - blue or 8 - azure). For each red object, determines the horizontal 
boundaries (min and max column) of its containing background region. 
If the background region is blue (1), the object is moved horizontally to the 
right edge of the region. 
If the background region is azure (8), the object is moved horizontally to the 
left edge of the region. 
The object's vertical position remains unchanged. The background regions themselves 
are static.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates
              of the pixels belonging to a single object. Returns empty list if 
              no objects of the specified color are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Start BFS from this pixel
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds
                        if 0 <= nr < height and 0 <= nc < width:
                             # Check if neighbor is the same color and not visited
                             if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # Add the found object's coordinates to the list if it's not empty
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_background_region_boundaries(grid, obj_coords):
    """
    Determines the background color and horizontal boundaries of the connected 
    background region immediately surrounding or containing the object.

    Args:
        grid (np.array): The input grid.
        obj_coords (set): Set of (row, col) coordinates for the object.

    Returns:
        tuple: (background_color, region_min_col, region_max_col) or
               (None, -1, -1) if no valid background region is found adjacent 
               to the object.
    """
    height, width = grid.shape
    object_color = 2 # Assuming objects are always red (color 2)
    
    # Find a starting pixel for the background BFS
    q_start_points = deque()
    visited_bg_search = set() # Keep track of visited pixels during background search
    background_color = -1

    # Check neighbors of all object pixels to find a valid background starting point
    for r_obj, c_obj in obj_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_obj + dr, c_obj + dc
            # Check if neighbor is within bounds and not part of the object itself
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in obj_coords:
                potential_bg_color = grid[nr, nc]
                # Check if it's a valid background color (blue or azure)
                if potential_bg_color == 1 or potential_bg_color == 8:
                     # If we haven't found a background color yet, set it
                     if background_color == -1:
                         background_color = potential_bg_color
                         # Add this neighbor as a starting point if it matches the determined color
                         if (nr, nc) not in visited_bg_search:
                            q_start_points.append((nr, nc))
                            visited_bg_search.add((nr, nc))
                     # If we already have a background color, only add neighbors of that color
                     elif potential_bg_color == background_color:
                          if (nr, nc) not in visited_bg_search:
                             q_start_points.append((nr, nc))
                             visited_bg_search.add((nr, nc))
                     # If we find a neighbor of a *different* valid background color,
                     # this indicates an edge case not handled by the simple logic
                     # (e.g., object touching both blue and azure). Assume the first found color is correct.
                     # else: pass

    # If no valid adjacent background pixel was found, we cannot determine the region
    if background_color == -1 or not q_start_points:
         # Fallback: Check if the object is single pixel and grid has only one background color?
         # Or maybe the object fills almost the whole grid?
         # Let's check non-object pixels for a dominant background color.
         non_obj_pixels = grid[grid != object_color]
         unique_bg, counts = np.unique(non_obj_pixels, return_counts=True)
         valid_bg_present = [c for c in unique_bg if c == 1 or c == 8]

         if len(valid_bg_present) == 1:
             background_color = valid_bg_present[0]
             # Need to find *any* pixel of this color to start BFS
             bg_indices = np.argwhere(grid == background_color)
             if len(bg_indices) > 0:
                 start_node = tuple(bg_indices[0])
                 if start_node not in visited_bg_search:
                     q_start_points.append(start_node)
                     visited_bg_search.add(start_node)
                 # else: it was already found near the object, but queue was empty? Unlikely.
             else:
                 return None, -1, -1 # No pixels of this background color found

         elif len(valid_bg_present) == 0:
              return None, -1, -1 # No blue or azure pixels found at all
         else: # Both blue and azure present, but none adjacent? Ambiguous.
             # Stick with the first one found if any adjacent was found, otherwise fail.
             if background_color == -1: # implies q_start_points is empty too
                 return None, -1, -1

    # BFS to find all connected background pixels of the determined color
    region_coords = set()
    q = q_start_points # Use the starting points found near the object
    visited_bfs = visited_bg_search # Reuse visited set

    while q:
        row, col = q.popleft()
        region_coords.add((row, col))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            # Check bounds, ensure it's the correct background color, and not visited
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == background_color and (nr, nc) not in visited_bfs:
                visited_bfs.add((nr, nc))
                q.append((nr, nc))

    # If BFS didn't find any region coords (shouldn't happen if q_start_points had items)
    if not region_coords:
        print(f"Warning: BFS for background region failed despite finding start points for object near {next(iter(obj_coords))}.")
        return background_color, -1, -1 # Return color but indicate boundary failure

    # Determine min/max col of the background region from the coordinates found
    region_min_col = width
    region_max_col = -1
    for r_reg, c_reg in region_coords:
        region_min_col = min(region_min_col, c_reg)
        region_max_col = max(region_max_col, c_reg)

    # Handle case where region was technically found but resulted in invalid bounds (e.g., empty after filtering?)
    if region_min_col == width or region_max_col == -1:
        print(f"Warning: Calculated invalid region boundaries for object near {next(iter(obj_coords))}.")
        return background_color, -1, -1

    return background_color, region_min_col, region_max_col


def get_object_boundaries(obj_coords):
    """
    Finds the minimum and maximum column index occupied by the object.

    Args:
        obj_coords (set): Set of (row, col) coordinates for the object.

    Returns:
        tuple: (object_min_col, object_max_col) or (-1, -1) if obj_coords is empty.
    """
    if not obj_coords:
        return -1, -1
    
    # Initialize min_col to positive infinity and max_col to negative infinity
    min_col = float('inf')
    max_col = float('-inf')
    
    # Iterate through object coordinates to find min and max columns
    for _, c in obj_coords:
        min_col = min(min_col, c)
        max_col = max(max_col, c)
        
    # Check if min_col or max_col were updated, if not, return invalid bounds
    if min_col == float('inf') or max_col == float('-inf'):
        return -1, -1
        
    return int(min_col), int(max_col)


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Moves red objects (2) within blue (1) or azure (8) backgrounds.
    Objects in blue backgrounds move to the right boundary of their background region.
    Objects in azure backgrounds move to the left boundary of their background region.
    """
    # Convert input grid list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to modify and return as the output
    output_np = np.copy(input_np)
    height, width = output_np.shape
    object_color = 2
    blue_color = 1
    azure_color = 8

    # Find all red objects in the input grid
    red_objects = find_objects(input_np, object_color)

    # Process each red object found
    for obj_coords in red_objects:
        if not obj_coords:
            continue # Skip if somehow an empty object set was returned

        # Determine the background color and boundaries for the current object
        background_color, region_min_col, region_max_col = get_background_region_boundaries(input_np, obj_coords)

        # If background region details are invalid, skip processing this object
        if background_color is None or region_min_col == -1 or region_max_col == -1:
            # Optional: print a warning
            # print(f"Warning: Could not determine valid region for object starting near {next(iter(obj_coords))}. Skipping.")
            continue

        # Determine the object's current horizontal boundaries
        object_min_col, object_max_col = get_object_boundaries(obj_coords)
        
        # If object boundaries are invalid, skip
        if object_min_col == -1 or object_max_col == -1:
             # Optional: print a warning
             # print(f"Warning: Could not determine valid boundaries for object starting near {next(iter(obj_coords))}. Skipping.")
             continue

        # Calculate the required horizontal shift based on the background color
        shift_amount = 0
        if background_color == blue_color:
            # Move Right: Shift needed to align object's right edge with region's right edge
            shift_amount = region_max_col - object_max_col
        elif background_color == azure_color:
            # Move Left: Shift needed to align object's left edge with region's left edge
            shift_amount = region_min_col - object_min_col # This will be <= 0
        else:
            # Should not happen if get_background_region_boundaries works correctly
            # print(f"Warning: Invalid background color {background_color} determined. Skipping object.")
            continue
            
        # Only perform the move if a shift is necessary
        if shift_amount != 0:
            # Erase the object from its original position in the output grid
            # Set the original object pixels to the determined background color
            for r, c in obj_coords:
                # Basic boundary check for safety, though coordinates should be valid
                if 0 <= r < height and 0 <= c < width:
                     output_np[r, c] = background_color 

            # Draw the object in its new position
            for r, c in obj_coords:
                # Calculate the new column position
                new_c = c + shift_amount
                # Check if the new position is within grid bounds
                if 0 <= r < height and 0 <= new_c < width:
                     output_np[r, new_c] = object_color
                else:
                     # This indicates an error in logic or boundary calculation,
                     # as the object should stay within the calculated region boundaries.
                     # Optional: print a warning
                     # print(f"Warning: Object pixel ({r},{c}) moved out of bounds to ({r},{new_c}). Region: {region_min_col}-{region_max_col}. Shift: {shift_amount}")
                     # As a fallback, maybe revert the erase? Or leave as is?
                     # Reverting the erase might be safer if the move failed.
                     # However, the specification implies the move should always be valid.
                     # Let's stick to drawing within bounds. If a pixel goes out, it's lost,
                     # which might reveal the error more clearly than partial drawing.
                     pass 

    # Convert the final NumPy array back to a list of lists for the return value
    return output_np.tolist()
```