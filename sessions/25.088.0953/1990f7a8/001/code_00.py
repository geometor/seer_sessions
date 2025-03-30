import numpy as np
from collections import deque

"""
Identifies exactly four distinct red (2) objects in the input grid. 
Each object's pattern is assumed to be contained within a 3x3 bounding box area 
in the input. 
These four 3x3 areas (patches) are extracted.
The patches are sorted based on the top-left coordinate of their bounding box 
in the original input grid (first by row, then by column).
A 7x7 output grid is created, initialized to white (0).
The sorted 3x3 patches are placed onto the 7x7 output grid in a 2x2 arrangement 
with a one-pixel white border between them:
- 1st patch -> top-left (rows 0-2, cols 0-2)
- 2nd patch -> top-right (rows 0-2, cols 4-6)
- 3rd patch -> bottom-left (rows 4-6, cols 0-2)
- 4th patch -> bottom-right (rows 4-6, cols 4-6)
The central row (3) and central column (3) remain white.
"""

def find_objects(grid, color, background_color=0):
    """
    Finds connected components of a given color in the grid.
    For each component, identifies the top-left corner of its bounding box
    and extracts the 3x3 patch from the grid starting at that corner.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.
        background_color (int): The background color used for padding if needed.

    Returns:
        list: A list of dictionaries, where each dict contains:
              'coords': (row, col) tuple of the top-left corner of the 3x3 patch.
              'patch': a 3x3 np.array representing the extracted patch.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find all connected pixels of this object
                object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while q:
                    row, col = q.popleft()
                    object_pixels.append((row, col))
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the same color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Once the object is fully explored, determine its top-left corner (min_r, min_c)
                top_left_coord = (min_r, min_c)
                
                # Extract the 3x3 patch starting from this top-left corner
                patch_rows = 3
                patch_cols = 3
                
                # Create a 3x3 patch, initialize with background color
                final_patch = np.full((patch_rows, patch_cols), background_color, dtype=int)
                
                # Determine the actual slice dimensions available in the grid
                available_rows = min(patch_rows, height - min_r)
                available_cols = min(patch_cols, width - min_c)
                
                # Copy the available part from the input grid into the patch
                extracted_part = grid[min_r : min_r + available_rows, min_c : min_c + available_cols]
                final_patch[0:available_rows, 0:available_cols] = extracted_part

                # Store the object's top-left coordinate and its 3x3 patch
                objects.append({'coords': top_left_coord, 'patch': final_patch})

    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule:
    Extract four 3x3 object patches, sort them by position, and arrange them
    in a 2x2 layout on a 7x7 output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    target_color = 2
    background_color = 0
    output_size = (7, 7)
    patch_size = (3, 3)

    # 1. Find all red objects and extract their 3x3 patches
    objects = find_objects(input_np, target_color, background_color)

    # Expect exactly 4 objects based on training examples
    # if len(objects) != 4:
    #    print(f"Warning: Expected 4 objects, but found {len(objects)}. Proceeding anyway.")
        # Depending on ARC rules, might need specific error handling here.
        # For now, we proceed assuming the sorting and placement logic can handle it (or fail gracefully).

    # 2. Sort the found objects based on their top-left coordinate (row first, then column)
    objects.sort(key=lambda obj: obj['coords'])

    # 3. Create the 7x7 output grid, initialized with the background color
    output_grid = np.full(output_size, background_color, dtype=int)

    # 4. Define the top-left coordinates for placing the patches in the output grid
    placements = [
        (0, 0),  # Top-left quadrant
        (0, 4),  # Top-right quadrant
        (4, 0),  # Bottom-left quadrant
        (4, 4)   # Bottom-right quadrant
    ]

    # 5. Place the sorted patches onto the output grid
    num_objects_to_place = min(len(objects), len(placements)) # Place up to 4 objects
    for i in range(num_objects_to_place):
        obj = objects[i]
        patch = obj['patch']
        start_row, start_col = placements[i]
        
        # Calculate end row/col for slicing (should be start + 3)
        end_row = start_row + patch_size[0]
        end_col = start_col + patch_size[1]
        
        # Place the 3x3 patch into the designated quadrant
        output_grid[start_row:end_row, start_col:end_col] = patch

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()