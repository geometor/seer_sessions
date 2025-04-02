import numpy as np
from collections import Counter

"""
Transforms an input grid based on identifying the largest contiguous non-background object and specific single-pixel 'anchor' objects.

1.  Determine the background color (most frequent pixel color).
2.  Find all contiguous objects (connected orthogonally or diagonally) of non-background colors.
3.  Identify the object with the largest number of pixels. Its color is the 'shape_color'.
4.  Identify all single-pixel objects whose color is neither the background color nor the 'shape_color'. These are 'anchor points'. Their color is the 'anchor_color'.
5.  Create an output grid filled with the background color.
6.  For each anchor point's location (r, c), draw a 3x3 cross pattern in the output grid:
    - Center pixel (r, c) gets the 'anchor_color'.
    - Orthogonally adjacent pixels (r-1, c), (r+1, c), (r, c-1), (r, c+1) get the 'shape_color', respecting grid boundaries.
"""

def find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid.
    Connectivity includes orthogonal and diagonal neighbors.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                obj_color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    
                    # Check 8 neighbors (orthogonal and diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] == obj_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                objects.append({
                    'color': obj_color,
                    'locations': obj_pixels,
                    'size': len(obj_pixels)
                })
    return objects

def transform(input_grid):
    """
    Applies the described transformation to the input grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # 1. Determine background color
    unique_colors, counts = np.unique(grid, return_counts=True)
    background_color = unique_colors[np.argmax(counts)]
    
    # 2. Find all non-background objects
    all_objects = find_objects(grid, background_color)
    
    # Handle case where there are no non-background objects
    if not all_objects:
        return input_grid # Or return grid filled with background? Task implies input is preserved if no anchors/shapes. Let's return a background grid.
        # return np.full((rows, cols), background_color, dtype=int).tolist()

    # 3. Identify the largest object and its color ('shape_color')
    largest_object = max(all_objects, key=lambda obj: obj['size'])
    shape_color = largest_object['color']
    
    # 4. Identify anchor points (single-pixel objects with distinct color)
    anchor_points = []
    anchor_color = -1 # Initialize anchor color
    for obj in all_objects:
        if obj['size'] == 1 and obj['color'] != background_color and obj['color'] != shape_color:
            if anchor_color == -1:
                 anchor_color = obj['color'] # Assume all anchors have the same color
            # Ensure consistency if multiple anchors exist (though examples imply one anchor color)
            if obj['color'] == anchor_color:
                 anchor_points.append(obj['locations'][0]) # location is (row, col)

    # 5. Create output grid filled with background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Handle case where no anchor points are found
    if not anchor_points:
        # If no anchors, maybe the original grid or just background is expected.
        # The examples show patterns appear ONLY if anchors exist AND a largest shape exists.
        # Returning background seems most consistent if anchors are the trigger.
        return output_grid.tolist() 

    # 6. Draw the cross pattern for each anchor point
    for r, c in anchor_points:
        # a. Place anchor color at the center
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = anchor_color
            
        # b. Place shape color at orthogonal neighbors (within bounds)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                output_grid[nr, nc] = shape_color
                
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
