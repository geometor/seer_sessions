import numpy as np
from collections import Counter
import sys

# Set higher recursion depth for deep searches if needed, though BFS is preferred.
# sys.setrecursionlimit(2000) 

def find_objects(grid_np, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid using BFS.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        background_color (int): The color to treat as background.

    Returns:
        list: A list of dictionaries, each representing an object with its 
              properties: color, pixels (list of (r, c) tuples), 
              pixel_area (int), bounding_box (tuple: min_r, min_c, max_r, max_c), 
              and bounding_box_area (int). Returns an empty list if no 
              non-background objects are found.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid_np[r, c]
            # Process only if it's not background and not visited yet
            if color != background_color and not visited[r, c]:
                # Start Breadth-First Search (BFS) to find the object
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                queue_idx = 0
                while queue_idx < len(q): # Efficient BFS without list.pop(0)
                    row, col = q[queue_idx]
                    queue_idx += 1
                    
                    obj_pixels.append((row, col))
                    
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-directional: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid_np[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Calculate object properties after BFS completes
                pixel_area = len(obj_pixels)
                bounding_box = (min_r, min_c, max_r, max_c)
                bbox_h = max_r - min_r + 1
                bbox_w = max_c - min_c + 1
                bounding_box_area = bbox_h * bbox_w

                # Store the found object and its properties
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'pixel_area': pixel_area,
                    'bounding_box': bounding_box,
                    'bounding_box_area': bounding_box_area
                })
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid by selecting a specific object and extracting its bounding box.
    
    The selection criteria are:
    1. Identify all contiguous non-background objects.
    2. Find the object(s) with the smallest pixel area (number of cells).
    3. If there is only one object with the smallest pixel area, select it.
    4. If there is a tie (multiple objects with the same smallest pixel area), 
       select the one among them that has the largest bounding box area.
    5. The output is the content of the input grid within the minimal bounding 
       box of the selected object.
    """
    
    # Convert input list of lists to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Handle empty input grids
    if input_grid_np.size == 0:
        return [] 
        
    # 1. Identify the background color (most frequent color)
    colors, counts = np.unique(input_grid_np, return_counts=True)
    if len(colors) == 0: # Should not happen if size > 0, but defensive check
        return []
    background_color = colors[np.argmax(counts)]

    # 2. Find all non-background objects and calculate their properties
    objects = find_objects(input_grid_np, background_color)

    # Handle case where no non-background objects are found
    if not objects:
        # Based on ARC tasks, there's usually an object. Return empty grid?
        # Or maybe the original grid if only background exists?
        # Let's return an empty grid for consistency if no objects found.
        return [] 
        
    # 3. Find the minimum pixel area among all found objects
    min_pixel_area = min(obj['pixel_area'] for obj in objects)
    
    # 4. Identify all objects having this minimum pixel area
    min_area_objects = [obj for obj in objects if obj['pixel_area'] == min_pixel_area]

    selected_object = None

    # 5. Apply selection criteria
    # Case a: Unique smallest pixel area object
    if len(min_area_objects) == 1:
        selected_object = min_area_objects[0]
        
    # Case b: Tie in smallest pixel area - select the one with largest bounding box area
    else: 
        max_bbox_area_in_tie = -1
        candidate_object = None
        for obj in min_area_objects:
            if obj['bounding_box_area'] > max_bbox_area_in_tie:
                max_bbox_area_in_tie = obj['bounding_box_area']
                candidate_object = obj
        selected_object = candidate_object # Assign the best candidate found
                
    # Ensure an object was selected (should always happen if objects exist and logic is sound)
    if selected_object is None:
         # Fallback: If selection somehow fails (e.g., multiple objects with min area
         # AND same max bbox area), pick the first one identified among the tie.
         # This might occur if ARC examples don't cover this specific ambiguity.
         if min_area_objects:
             selected_object = min_area_objects[0]
         else: # Should be impossible if objects list was not empty
             return [] # Return empty if something went wrong

    # 6. Determine the bounding box coordinates of the selected object
    min_r, min_c, max_r, max_c = selected_object['bounding_box']

    # 7. Extract the subgrid defined by the bounding box from the original input grid
    output_grid_np = input_grid_np[min_r:max_r+1, min_c:max_c+1]

    # Convert the resulting numpy array back to a list of lists for the final output format
    output_grid = output_grid_np.tolist()

    return output_grid