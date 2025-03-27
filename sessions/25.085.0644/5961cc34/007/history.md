
Previous Code:
```python
import numpy as np
import math

"""
Transforms an input grid based on blue/green shapes and a yellow marker.

1.  Initialize the output grid with the same dimensions as the input, filled with azure (8).
2.  Identify all distinct contiguous shapes composed of blue (1) or green (3) pixels using 8-way connectivity. Let N be the number of shapes found. Calculate the bounding box for each shape.
3.  Locate the single yellow (4) marker pixel at position (mr, mc).
4.  Calculate the minimum Manhattan distance (min_dist) from the marker's position (mr, mc) to any pixel location covered by any of the shapes' bounding boxes.
5.  Apply rules based on the number of shapes (N):
    *   If N > 1:
        *   Fill the bounding box of every blue/green shape with red (2).
        *   Fill the entire column mc (the marker's column) with red (2), overwriting previous fills.
    *   If N == 1:
        *   Check the marker's proximity:
            *   If min_dist <= 2:
                *   Calculate the centroid (average row, average column) of the single shape's pixels. Determine the centroid's column index cc (floor of the average column value).
                *   Fill the shape's bounding box with red (2).
                *   Fill the entire column cc (the centroid's column index) with red (2), overwriting previous fills.
            *   If min_dist > 2:
                *   Fill only the single pixel at the marker's original position (mr, mc) with red (2).
6.  Return the final output grid.
"""

def find_shapes_and_bboxes(input_grid_np, shape_colors):
    """
    Identifies contiguous shapes of specified colors using 8-way connectivity
    and calculates their bounding boxes and pixel coordinates.

    Args:
        input_grid_np (np.array): The input grid.
        shape_colors (list): List of colors that constitute shapes.

    Returns:
        tuple: (list_of_shapes, num_shapes)
            list_of_shapes: A list where each element is a dict:
                            {'pixels': set((r, c), ...), 'bbox': (rmin, rmax, cmin, cmax)}
            num_shapes: The total number of distinct shapes found.
    """
    rows, cols = input_grid_np.shape
    shape_mask = np.isin(input_grid_np, shape_colors)
    labeled_grid = np.zeros_like(input_grid_np, dtype=int)
    visited = np.zeros_like(shape_mask, dtype=bool)
    current_label = 0
    shapes = []

    for r in range(rows):
        for c in range(cols):
            if shape_mask[r, c] and not visited[r, c]:
                current_label += 1
                component_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r, min_c, max_c = r, r, c, c

                while q:
                    row, col = q.pop(0) # Use queue for BFS-like exploration
                    labeled_grid[row, col] = current_label
                    component_pixels.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               shape_mask[nr, nc] and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                shapes.append({
                    'pixels': component_pixels,
                    'bbox': (min_r, max_r, min_c, max_c) # inclusive max
                })

    return shapes, current_label

def calculate_min_manhattan_dist(marker_pos, shapes):
    """
    Calculates the minimum Manhattan distance from the marker position
    to any point within any of the shapes' bounding boxes.

    Args:
        marker_pos (tuple): (row, col) of the marker.
        shapes (list): List of shape dictionaries, each with a 'bbox'.

    Returns:
        float: Minimum Manhattan distance, or infinity if no shapes.
    """
    if not shapes:
        return float('inf')
        
    mr, mc = marker_pos
    min_dist = float('inf')

    for shape in shapes:
        rmin, rmax, cmin, cmax = shape['bbox']
        
        # Find the closest point (pr, pc) in the bbox rectangle to (mr, mc)
        pr = max(rmin, min(mr, rmax))
        pc = max(cmin, min(mc, cmax))
        
        # Calculate Manhattan distance to this closest point
        dist = abs(mr - pr) + abs(mc - pc)
        min_dist = min(min_dist, dist)
        
    return min_dist

def calculate_centroid_column(pixels):
    """
    Calculates the floor of the average column index for a set of pixels.

    Args:
        pixels (set): Set of (row, col) tuples.

    Returns:
        int: The floor of the average column index, or -1 if no pixels.
    """
    if not pixels:
        return -1
    
    avg_c = sum(c for r, c in pixels) / len(pixels)
    return math.floor(avg_c)


def transform(input_grid):
    """
    Applies the transformation rule based on shapes, marker, and distance.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    background_color = 8
    fill_color = 2
    shape_colors = [1, 3] # blue, green
    marker_color = 4 # yellow

    # 1. Initialize output_grid with background color
    output_grid = np.full_like(input_grid_np, background_color)

    # 2. Identify shapes and their properties
    shapes, num_shapes = find_shapes_and_bboxes(input_grid_np, shape_colors)

    # 3. Locate the marker
    marker_coords = np.argwhere(input_grid_np == marker_color)
    if marker_coords.size == 0:
        # If no marker, maybe return background? Or handle as error?
        # Based on examples, marker is always present. Assume it exists.
        # If it *could* be absent, rules need clarification.
        # Let's proceed assuming it's found.
        print("Warning: Marker not found!") # Or raise error
        return output_grid.tolist() # Return background for now

    marker_pos = tuple(marker_coords[0]) # (mr, mc)
    mr, mc = marker_pos

    # Handle N=0 case explicitly if needed (though not seen in examples)
    if num_shapes == 0:
         # Rule unclear for N=0. Maybe fill marker pos? Or just background?
         # Let's stick to background as safest default.
         # output_grid[mr, mc] = fill_color # Alternative: fill marker pos
         return output_grid.tolist()


    # 4. Calculate minimum distance from marker to any shape bbox
    min_dist = calculate_min_manhattan_dist(marker_pos, shapes)

    # 5. Apply rules based on number of shapes (N)
    if num_shapes > 1:
        # 5a. N > 1: Fill all bboxes + marker column
        for shape in shapes:
            rmin, rmax, cmin, cmax = shape['bbox']
            output_grid[rmin:rmax+1, cmin:cmax+1] = fill_color
        output_grid[:, mc] = fill_color # Overwrite column mc
        
    elif num_shapes == 1:
        # 5b. N == 1: Check distance
        single_shape = shapes[0]
        
        if min_dist <= 2:
            # Marker "close": Fill bbox + centroid column
            rmin, rmax, cmin, cmax = single_shape['bbox']
            cc = calculate_centroid_column(single_shape['pixels'])
            
            if cc != -1: # Ensure centroid column is valid
               output_grid[rmin:rmax+1, cmin:cmax+1] = fill_color
               output_grid[:, cc] = fill_color # Overwrite column cc
            else:
                 # Should not happen if num_shapes == 1
                 print("Warning: Could not calculate centroid column for single shape.")
        
        else: # min_dist > 2
            # Marker "distant": Fill only marker position
            output_grid[mr, mc] = fill_color

    # 6. Return the modified output grid
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.30769230769232

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 3 3 8 8 8 8
8 1 1 1 1 8 8 8 1 1 1 3 8 8 8 8 8 8 1 1 1 1 8 8 8
8 1 1 1 1 8 8 8 1 1 1 3 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 1 1 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 2 2 2 2 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 62
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 21.565217391304344

## Example 3:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 1 1 1 1 1 1 8 8 8 8 8 8 3 1 1 1 1 1 8 8
8 8 1 1 1 1 1 1 8 8 8 8 8 8 3 1 1 1 1 1 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 2 2 2 2 2 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
```
Match: False
Pixels Off: 62
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.505928853754938

## Example 4:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 3 1 1 1 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 55
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 21.739130434782624
