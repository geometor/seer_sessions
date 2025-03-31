```python
import numpy as np
from collections import Counter

"""
Identifies maximal contiguous objects composed of non-background, non-noise colors 
in the input grid. Filters these objects to keep only those whose minimal bounding 
box is exactly 6x6 pixels. The top-left corners of these bounding boxes define 
the 6x6 regions to be extracted. These regions are ordered primarily by the row 
and secondarily by the column of their top-left corner. This order is reversed 
if any Orange (7) pixel exists anywhere in the input grid. Each selected 6x6 region 
is extracted from the input, cleaned by replacing noise pixels (Gray=5, Orange=7, 
Maroon=9) with the identified background color, and then these cleaned 6x6 grids 
are vertically stacked in the determined order to form the final output grid.
"""

def find_objects_and_bboxes(grid, background_color, noise_colors):
    """
    Finds contiguous objects of non-background, non-noise colors and their bounding boxes.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color.
        noise_colors (set): A set of colors defined as noise.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              - 'min_row': Min row of the bounding box.
              - 'max_row': Max row of the bounding box.
              - 'min_col': Min col of the bounding box.
              - 'max_col': Max col of the bounding box.
              - 'pixels': A set of (row, col) tuples comprising the object. (Optional, useful for debugging)
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Start BFS if we find an unvisited pixel that is not background or noise
            if not visited[r, c] and color != background_color and color not in noise_colors:
                q = [(r, c)]
                visited[r, c] = True
                object_pixels = set([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.pop(0)
                    
                    # Update bounding box
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
                            # Add neighbor if it's part of the object (not background or noise)
                            if neighbor_color != background_color and neighbor_color not in noise_colors:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                object_pixels.add((nr,nc))
                
                # Store the bounding box of the found object
                objects.append({
                    'min_row': min_r, 'max_row': max_r, 
                    'min_col': min_c, 'max_col': max_c,
                    'pixels': object_pixels # Optional
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # Handle empty input grid case
    if rows == 0 or cols == 0:
        return []

    # 1. Identify the background color
    colors, counts = np.unique(grid, return_counts=True)
    if len(colors) == 0:
       return []
    background_color = colors[np.argmax(counts)]

    # 2. Define noise colors
    noise_colors = {5, 7, 9}

    # 3. Find all distinct contiguous objects (non-background, non-noise)
    all_objects = find_objects_and_bboxes(grid, background_color, noise_colors)
    
    # 4. Filter objects to keep only those with an exactly 6x6 bounding box
    valid_object_corners = []
    for obj in all_objects:
        height = obj['max_row'] - obj['min_row'] + 1
        width = obj['max_col'] - obj['min_col'] + 1
        if height == 6 and width == 6:
            # 5. Collect the top-left corner coordinates
            valid_object_corners.append((obj['min_row'], obj['min_col']))

    # Handle case where no valid 6x6 objects are found
    if not valid_object_corners:
        return [] 

    # 6. Sort corners (top-to-bottom, then left-to-right)
    # Ensure uniqueness in case multiple objects map to the same bbox (unlikely but possible)
    unique_sorted_corners = sorted(list(set(valid_object_corners)), key=lambda x: (x[0], x[1]))

    # 7. Check for Orange (7) pixels anywhere in the input grid
    has_orange_signal = np.any(grid == 7)

    # 8. Reverse order if Orange (7) is present
    if has_orange_signal:
        unique_sorted_corners.reverse()

    # 9. Initialize list for cleaned 6x6 output grids
    output_subgrids = []

    # 10. Iterate through the final ordered corners
    for r_corner, c_corner in unique_sorted_corners:
        # 11a. Extract the 6x6 region
        # Check if extraction is within bounds (should be guaranteed by object finding if grid dims >= 6)
        if r_corner + 6 <= rows and c_corner + 6 <= cols:
            subgrid = grid[r_corner : r_corner + 6, c_corner : c_corner + 6].copy()
            
            # 11b. Clean the subgrid (replace noise with background)
            for r_sub in range(6):
                for c_sub in range(6):
                    if subgrid[r_sub, c_sub] in noise_colors:
                        subgrid[r_sub, c_sub] = background_color
                        
            # 11c. Add cleaned subgrid to the list
            output_subgrids.append(subgrid)
        # else: # Should not happen based on examples and logic, but good defensive programming
            # print(f"Warning: Cannot extract 6x6 grid at {r_corner, c_corner} from grid of size {rows, cols}") 


    # 12. Vertically stack the cleaned grids
    if not output_subgrids:
         return [] # Return empty list if no valid subgrids could be processed
         
    final_output_grid_np = np.vstack(output_subgrids)

    # Convert final numpy array back to list of lists
    return final_output_grid_np.tolist()
```