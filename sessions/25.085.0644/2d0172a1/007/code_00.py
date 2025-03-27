import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify the background color (most frequent) and foreground color (second most frequent) in the input grid.
2. Find all contiguous objects composed of the foreground color pixels (using 8-way connectivity).
3. For each foreground object, determine its minimal bounding box (MBB).
4. Count the number of background-colored pixels within the MBB of each foreground object in the original input grid.
5. Select the target object: the foreground object whose MBB contains the *largest* number of background-colored pixels. If there's a tie, select the largest object (by pixel count) among the tied objects.
6. Determine the minimal bounding box enclosing only the pixels of the selected target object.
7. Create an output grid whose dimensions are 2 larger (in height and width) than the bounding box of the target object.
8. Initialize the output grid with the background color.
9. Draw a 1-pixel thick border around the output grid using the foreground color.
10. Copy only the pixels belonging to the target object into the center of the output grid (inside the border), placed relative to the object's bounding box. The color copied is the foreground color. Pixels within the central area that do not correspond to a pixel from the target object remain the background color.
"""

def find_colors(grid):
    """
    Finds the background (most frequent) and foreground (typically the second most frequent) colors.
    Handles cases with only one color.
    """
    colors, counts = np.unique(grid, return_counts=True)
    
    if len(colors) == 1:
        return colors[0], None # Only one color present
    
    # Sort colors by frequency in descending order
    sorted_indices = np.argsort(-counts)
    background_color = colors[sorted_indices[0]]
    
    # Find the first color that is not the background color
    foreground_color = None
    for i in range(1, len(sorted_indices)):
        if colors[sorted_indices[i]] != background_color:
             foreground_color = colors[sorted_indices[i]]
             break
        # If all remaining colors are the same as background (shouldn't happen if len(colors)>1)
        # Or if only background exists, foreground remains None

    # If still None (e.g., grid was [0,0,0,1]), the second most frequent is the foreground
    if foreground_color is None and len(sorted_indices) > 1:
        foreground_color = colors[sorted_indices[1]]

    return background_color, foreground_color


def count_background_in_bbox(grid, bbox, background_color):
    """Counts background pixels within a given bounding box."""
    min_r, max_r, min_c, max_c = bbox
    count = 0
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Ensure coordinates are within grid bounds (should be by definition of bbox from find_objects)
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                if grid[r, c] == background_color:
                    count += 1
    return count

def find_objects(grid, target_color, background_color):
    """
    Finds all contiguous objects of the target_color using Breadth-First Search (BFS)
    with 8-way connectivity. Calculates the number of background pixels within each object's bounding box.
    Returns a list of objects (dictionaries with pixels, bbox, size, bg_in_bbox).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if pixel is target color and not visited
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col))
                    
                    # Update bounding box
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Explore 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue # Skip self
                            
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds and if neighbor is target color and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store the found object's details
                if current_object_pixels:
                    bbox = (min_r, max_r, min_c, max_c)
                    bg_count = count_background_in_bbox(grid, bbox, background_color)
                    
                    objects.append({
                        'pixels': set(current_object_pixels),
                        'min_row': min_r, 'max_row': max_r,
                        'min_col': min_c, 'max_col': max_c,
                        'size': len(current_object_pixels),
                        'bg_in_bbox': bg_count # Store the background count
                    })
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # Handle empty/invalid input grids
    if input_np.size == 0: return []
    if input_np.shape[0] == 0 or input_np.shape[1] == 0: return [[]] 

    # 1. Identify Background and Foreground Colors
    background_color, foreground_color = find_colors(input_np)

    # Handle edge case: Only one color in the grid
    if foreground_color is None:
        single_color = background_color
        # Return a 3x3 grid with the single color as border and center
        # Based on observation, might need adjustment, but plausible default.
        output_grid = np.full((3, 3), single_color, dtype=int)
        return output_grid.tolist()

    # 2. Find all contiguous objects of the foreground color and count bg pixels in their bbox
    objects = find_objects(input_np, foreground_color, background_color)

    # Handle edge case: No foreground objects found
    if not objects:
        # Return a minimal 3x3 grid: foreground border, background center.
        output_grid = np.full((3, 3), background_color, dtype=int)
        output_grid[0, :] = foreground_color
        output_grid[-1, :] = foreground_color
        output_grid[:, 0] = foreground_color
        output_grid[:, -1] = foreground_color
        return output_grid.tolist()

    # 3-5. Select the target object based on max background pixels in bbox, tie-break with size
    
    # Find the maximum background count
    max_bg_count = -1
    for obj in objects:
        if obj['bg_in_bbox'] > max_bg_count:
            max_bg_count = obj['bg_in_bbox']
            
    # Filter objects that have the maximum background count
    candidate_objects = [obj for obj in objects if obj['bg_in_bbox'] == max_bg_count]
    
    # Select the largest object among candidates (tie-breaker)
    if not candidate_objects: # Should not happen if objects list is not empty
         return [] # Or raise error
    
    target_object = max(candidate_objects, key=lambda obj: obj['size'])


    # 6. Determine the bounding box coordinates of the target object
    min_row, max_row = target_object['min_row'], target_object['max_row']
    min_col, max_col = target_object['min_col'], target_object['max_col']
    object_pixels = target_object['pixels'] # Set of (r, c) tuples

    # Calculate bounding box dimensions and output grid dimensions
    bbox_h = max_row - min_row + 1
    bbox_w = max_col - min_col + 1
    output_h = bbox_h + 2 # Add 2 for the border
    output_w = bbox_w + 2 # Add 2 for the border

    # 7. Create the OutputGrid initialized with the BackgroundColor
    output_grid = np.full((output_h, output_w), background_color, dtype=int)

    # 8. Draw the 1-pixel border using the ForegroundColor
    output_grid[0, :] = foreground_color  # Top row
    output_grid[-1, :] = foreground_color # Bottom row
    output_grid[:, 0] = foreground_color  # Left column
    output_grid[:, -1] = foreground_color # Right column

    # 9. Copy the pixels belonging to the target object into the OutputGrid's inner area
    for r_in, c_in in object_pixels:
        # Calculate the corresponding position within the output grid's central area
        # Offset by 1 due to the border
        r_out = (r_in - min_row) + 1
        c_out = (c_in - min_col) + 1
        
        # Place the foreground color at the calculated position
        # Basic bounds check (should always be true given calculation)
        if 1 <= r_out < output_h - 1 and 1 <= c_out < output_w - 1:
             output_grid[r_out, c_out] = foreground_color

    # Return the final grid as a list of lists
    return output_grid.tolist()