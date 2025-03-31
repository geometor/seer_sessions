import numpy as np
from collections import Counter

"""
Identify distinct, same-colored contiguous objects (non-background, non-noise) 
whose minimal bounding box fits within 6x6. Use the top-left corner of each 
such object's bounding box to define the top-left corner of a 6x6 window to 
extract from the input. Collect all unique 6x6 window definitions. Order 
them top-to-bottom, left-to-right based on their top-left corner. If the 
input grid contains any Orange (7) pixels, reverse this order. Extract each 
6x6 window, clean it by replacing noise pixels (Gray=5, Orange=7, Maroon=9) 
with the background color, and vertically stack the cleaned windows to create 
the output.
"""

def find_colored_objects(grid, background_color, noise_colors):
    """
    Finds contiguous objects of the *same* non-background, non-noise color.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color.
        noise_colors (set): A set of colors to ignore as part of objects.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains:
              - 'color': The color of the object.
              - 'pixels': A set of (row, col) tuples for pixels in the object.
              - 'bbox': A tuple (min_r, max_r, min_c, max_c) for the bounding box.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Start BFS if we find an unvisited pixel that is not background or noise
            if not visited[r, c] and color != background_color and color not in noise_colors:
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                current_color = color # Color of the object we are tracing
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if visited
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]:
                            neighbor_color = grid[nr, nc]
                            # Only add neighbors of the SAME color as the starting pixel
                            if neighbor_color == current_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store the found object details
                objects.append({
                    'color': current_color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, max_r, min_c, max_c)
                })
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the described logic.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    if rows == 0 or cols == 0:
        return []

    # 1. Identify the background color
    colors, counts = np.unique(grid, return_counts=True)
    if len(colors) == 0: # Handle empty input grid case
      return []
    background_color = colors[np.argmax(counts)]

    # 2. Define noise colors
    noise_colors = {5, 7, 9}

    # 3. Find all contiguous objects by color
    all_objects = find_colored_objects(grid, background_color, noise_colors)

    # 4. Filter objects by bounding box size (<= 6x6)
    filtered_objects = []
    for obj in all_objects:
        min_r, max_r, min_c, max_c = obj['bbox']
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        if height <= 6 and width <= 6:
            filtered_objects.append(obj)

    # 5. Get unique top-left corners (min_r, min_c) from filtered objects
    unique_corners = set()
    for obj in filtered_objects:
        min_r, _, min_c, _ = obj['bbox']
        # Ensure the 6x6 window starting at this corner fits within the grid
        if min_r + 6 <= rows and min_c + 6 <= cols:
             unique_corners.add((min_r, min_c))
        #else:
            # Optional: log or handle cases where object near edge implies window out of bounds
            # Based on examples, seems objects are placed such that 6x6 fits
            # pass 

    # 6. Handle case where no valid corners are found
    if not unique_corners:
        return [] 

    # 7. Sort unique corners (row, then column)
    sorted_corners = sorted(list(unique_corners), key=lambda x: (x[0], x[1]))

    # 8. Check for Orange (7) in the original input grid
    has_orange = np.any(grid == 7)

    # 9. Reverse order if Orange (7) is present
    if has_orange:
        sorted_corners.reverse()

    # 10. Initialize list for cleaned 6x6 output grids
    output_subgrids = []

    # 11. Iterate through corners, extract, clean, and collect
    for r_corner, c_corner in sorted_corners:
        # a. Extract the 6x6 subgrid (already bounds-checked in step 5)
        subgrid = grid[r_corner : r_corner + 6, c_corner : c_corner + 6].copy()
        
        # b. Clean the subgrid (replace noise with background)
        for r_sub in range(6):
            for c_sub in range(6):
                if subgrid[r_sub, c_sub] in noise_colors:
                    subgrid[r_sub, c_sub] = background_color
                    
        # c. Add cleaned subgrid to the list
        output_subgrids.append(subgrid)

    # 12. Vertically stack the cleaned grids
    if not output_subgrids:
         return [] # Should not happen if unique_corners was not empty, but good practice
         
    final_output_grid_np = np.vstack(output_subgrids)

    # Convert final numpy array back to list of lists
    return final_output_grid_np.tolist()