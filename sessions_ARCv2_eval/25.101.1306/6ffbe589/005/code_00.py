import collections
import numpy as np # Using numpy for efficient grid operations can be helpful

"""
The transformation identifies all distinct contiguous objects (groups of non-white pixels using 8-way adjacency) in the input grid. 
It calculates the size (pixel count) of each object. 
The object with the largest pixel count is selected as the target. 
If there's a tie in size, the object whose bounding box has the minimum top row index is chosen. If there's still a tie, the one with the minimum left column index is chosen.
A minimal bounding box is calculated for this target object. 
The output grid is created by cropping the input grid exactly to the dimensions and location of this bounding box. 
All pixels within this bounding box in the input, including background pixels (0), are copied directly to the output grid.
"""

def find_objects(grid: list[list[int]], background_color: int = 0) -> list[dict]:
    """
    Finds all distinct connected objects of non-background pixels in the grid using 8-way adjacency.

    Args:
        grid: The input grid (list of lists of integers).
        background_color: The integer value representing the background.

    Returns:
        A list of dictionaries, where each dictionary represents an object and contains:
        - 'coords': A set of (row, col) coordinates of the object's pixels.
        - 'size': The number of pixels in the object.
        - 'bbox': A tuple (min_row, max_row, min_col, max_col) for the object.
        Returns an empty list if the grid is empty or contains no non-background pixels.
    """
    grid_np = np.array(grid, dtype=int)
    height, width = grid_np.shape
    if height == 0 or width == 0: return []

    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid_np[r, c] != background_color and not visited[r, c]:
                # Found the start of a new object
                current_object_coords = set()
                q = collections.deque([(r, c)])
                visited[r, c] = True
                obj_size = 0
                min_obj_r, max_obj_r = r, r
                min_obj_c, max_obj_c = c, c

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    obj_size += 1
                    # Update bounding box limits for this object during traversal
                    min_obj_r = min(min_obj_r, row)
                    max_obj_r = max(max_obj_r, row)
                    min_obj_c = min(min_obj_c, col)
                    max_obj_c = max(max_obj_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue # Skip self
                            
                            nr, nc = row + dr, col + dc

                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of the object and not visited
                                if grid_np[nr, nc] != background_color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                
                # Store object info if it has pixels
                if current_object_coords:
                     objects.append({'coords': current_object_coords, 
                                     'size': obj_size, 
                                     'bbox': (min_obj_r, max_obj_r, min_obj_c, max_obj_c)})
    return objects

# Note: get_bounding_box is integrated into find_objects now for efficiency

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Finds the largest object by pixel count in the input_grid, determines its
    bounding box, and returns the portion of the input_grid corresponding to that
    bounding box.
    """
    background_color = 0
    
    # 1. Identify all distinct non-background objects, their sizes, and bounding boxes
    objects = find_objects(input_grid, background_color)

    # Handle cases with no non-background objects found
    if not objects:
        # Return an empty list as per ARC guidelines for impossible tasks or no clear output
        return [] 

    # 2. Select the target object: largest size, tie-break with top-most then left-most bbox corner
    # Sort objects: primary key size (desc), secondary key min_row (asc), tertiary key min_col (asc)
    objects.sort(key=lambda obj: (obj['size'], -obj['bbox'][0], -obj['bbox'][2]), reverse=True)
    
    # The target object is the first one in the sorted list
    target_object_info = objects[0]
    
    # 3. Get the bounding box of the target object
    min_r, max_r, min_c, max_c = target_object_info['bbox']

    # Handle potential issue if bounding box is invalid (shouldn't happen if object exists)
    if max_r < min_r or max_c < min_c:
         # This case indicates an error in find_objects or an empty object was selected
         return [] 

    # 4. Crop the input grid using the bounding box coordinates
    # Python list slicing is [start:end], where 'end' is exclusive. So, use max_r+1 and max_c+1.
    output_grid = [row[min_c : max_c + 1] for row in input_grid[min_r : max_r + 1]]
    
    # 5. Return the cropped grid
    return output_grid