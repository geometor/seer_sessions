import numpy as np
from collections import Counter

"""
Identifies maximal contiguous regions of pixels whose colors are not the background color and not designated noise colors (Gray=5, Orange=7, Maroon=9).
Filters these regions, keeping only those whose minimal bounding box is exactly 6x6 pixels.
Determines the top-left corner (row, column) for each filtered region's bounding box.
Collects these top-left corners. Sorts them primarily by row index, secondarily by column index.
Checks the original input grid for the presence of any Orange (7) pixels. If found, reverses the sorted order of corners.
For each corner in the final ordered list:
  1. Extracts the 6x6 pixel subgrid from the input grid starting at that corner.
  2. Creates a cleaned version of the extracted 6x6 subgrid by replacing any pixels matching the noise colors (5, 7, 9) with the background color.
Vertically stacks the cleaned 6x6 subgrids in the final determined order to produce the output grid.
"""

def find_maximal_objects_and_bboxes(grid, background_color, noise_colors):
    """
    Finds maximal contiguous regions of non-background, non-noise colors and their bounding boxes.

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
              # - 'pixels': A set of (row, col) tuples comprising the object. (Optional)
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
                # object_pixels = set([(r, c)]) # Optional: collect pixels if needed
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Standard BFS
                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    
                    # Update bounding box for the current pixel
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
                                # object_pixels.add((nr,nc)) # Optional

                # Store the bounding box of the found maximal object
                objects.append({
                    'min_row': min_r, 'max_row': max_r, 
                    'min_col': min_c, 'max_col': max_c,
                    # 'pixels': object_pixels # Optional
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

    # 1. Determine the background color
    # Use np.unique which is efficient for this
    colors, counts = np.unique(grid, return_counts=True)
    if len(colors) == 0: # Should not happen if rows/cols > 0, but safe check
       return []
    background_color = colors[np.argmax(counts)]

    # 2. Define noise colors
    noise_colors = {5, 7, 9}

    # 3. Find all maximal contiguous regions (non-background, non-noise)
    # 4. Calculate their bounding boxes (done within the helper function)
    all_objects = find_maximal_objects_and_bboxes(grid, background_color, noise_colors)
    
    # 5. Filter regions to keep only those with an exactly 6x6 bounding box
    valid_object_corners = []
    for obj in all_objects:
        height = obj['max_row'] - obj['min_row'] + 1
        width = obj['max_col'] - obj['min_col'] + 1
        if height == 6 and width == 6:
            # 6. Collect the top-left corner coordinates
            valid_object_corners.append((obj['min_row'], obj['min_col']))

    # Handle case where no valid 6x6 regions are found
    if not valid_object_corners:
        return [] 

    # 7. Sort unique corners (top-to-bottom, then left-to-right)
    # Ensure uniqueness although BFS should find distinct maximal regions
    unique_sorted_corners = sorted(list(set(valid_object_corners)), key=lambda x: (x[0], x[1]))

    # 8. Check for Orange (7) pixels anywhere in the input grid
    has_orange_signal = np.any(grid == 7)

    # 9. Reverse order if Orange (7) is present
    if has_orange_signal:
        unique_sorted_corners.reverse()

    # 10. Initialize list for cleaned 6x6 output grids
    output_subgrids = []

    # 11. Iterate through the final ordered corners
    for r_corner, c_corner in unique_sorted_corners:
        # 11a. Extract the 6x6 region
        # Check if extraction is within bounds (should be guaranteed by 6x6 bbox filter if grid dims >= 6)
        if r_corner + 6 <= rows and c_corner + 6 <= cols:
            subgrid = grid[r_corner : r_corner + 6, c_corner : c_corner + 6].copy()
            
            # 11b. Clean the subgrid (replace noise with background)
            # Create a mask for noise colors within the subgrid
            noise_mask = np.isin(subgrid, list(noise_colors))
            # Replace noise pixels with the background color
            subgrid[noise_mask] = background_color
                        
            # 11c. Add cleaned subgrid to the list
            output_subgrids.append(subgrid)
        # else: # Defensive check, should not happen with current logic
            # print(f"Warning: Cannot extract 6x6 grid at {r_corner, c_corner} from grid of size {rows, cols}") 


    # 12. Vertically stack the cleaned grids
    if not output_subgrids:
         # This case is hit if valid_object_corners was empty initially
         return [] 
         
    final_output_grid_np = np.vstack(output_subgrids)

    # Convert final numpy array back to list of lists for ARC standard output
    return final_output_grid_np.tolist()