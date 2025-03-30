
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Create an output grid as a copy of the input grid.
2. Identify all distinct, contiguous, rectangular blocks composed solely of yellow (4) pixels in the input grid. These are the "yellow rectangles".
3. For each identified yellow rectangle:
    a. Determine its bounding box.
    b. Find all pixels within this bounding box in the input grid that are *not* yellow (4) and *not* white (0). These are the "internal pixels". Note: These internal pixels are within the area covered by the yellow rectangle's bounding box but are not part of the yellow rectangle itself.
    c. Check if any internal pixels were found.
    d. If internal pixels exist, check if they *all* share the same single color (the "inner color").
    e. If internal pixels exist and all share the same inner color:
        i. Count the number of internal pixels (N). This count determines the "border thickness" (T = N).
        ii. Calculate the coordinates of an expanded bounding box by extending the original bounding box outwards by the border thickness T in all four directions (up, down, left, right), ensuring the coordinates stay within the grid limits.
        iii. In the output grid, fill all pixels that are within the *expanded* bounding box but *outside* the *original* bounding box with the inner color.
        iv. In the output grid, ensure all pixels that were part of the original yellow rectangle (i.e., yellow pixels found in step 2) are set back to yellow (4). This preserves the yellow rectangle shape and overwrites any border pixels that might have overlapped with the original yellow area.
4. Yellow rectangles that do not have internal pixels, or whose internal pixels have multiple different colors, do not get a border drawn around them. Their yellow pixels are retained in the output unless overwritten by a border from another qualifying rectangle.
5. Return the modified output grid.
"""

def find_yellow_rectangles(grid):
    """
    Finds all connected components of yellow (4) pixels that form a solid rectangle.
    Uses 4-way connectivity.
    Returns a list of dictionaries, each containing the coordinates ('coords')
    and bounding box ('bbox') of a yellow rectangle.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []
    yellow_color = 4

    for r in range(height):
        for c in range(width):
            if grid[r, c] == yellow_color and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_coords.add((r, c))
                min_r, min_c, max_r, max_c = r, c, r, c # Keep track for bbox

                while q:
                    row, col = q.popleft()
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == yellow_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_coords.add((nr, nc))

                # Verify if the component *itself* forms a solid rectangle
                # Check if the number of yellow pixels found matches the area of their bounding box.
                bbox_height = max_r - min_r + 1
                bbox_width = max_c - min_c + 1
                if len(component_coords) == bbox_height * bbox_width:
                    # Further check: ensure all pixels within this bbox *in the component* are yellow
                    # This check is implicitly covered by the BFS finding only yellow connected pixels
                    # and the size check confirming it fills the bounding box derived *from those pixels*.
                    is_solid_rect = True # If size matches bbox area, it must be solid.

                    # Original code had a check here that iterated grid[r_rect, c_rect] != color,
                    # which was incorrect as it rejected rectangles containing internal non-yellow pixels.
                    # The current logic correctly identifies solid rectangles *of yellow*.

                    if is_solid_rect and component_coords:
                         rectangles.append({
                             'coords': component_coords, # The set of (r, c) for yellow pixels
                             'bbox': (min_r, min_c, max_r, max_c) # Bbox of the yellow pixels
                         })
    return rectangles

def find_internal_pixels(grid, bbox):
    """
    Finds pixels strictly inside the bbox that are not yellow (4) or white (0).
    """
    min_r, min_c, max_r, max_c = bbox
    internal_pixels = []
    # Iterate within the bounding box defined by the yellow pixels.
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check if the current coordinate (r,c) is actually part of the yellow rectangle pixels
            # This isn't strictly needed if find_yellow_rectangles ensures solid yellow shapes,
            # but it clarifies that we are looking for non-yellow/non-white *within* the rectangle's area.
             color = grid[r, c]
             # Rule 3b: internal pixels are NOT yellow (4) and NOT white (0)
             if color != 4 and color != 0:
                 # We only count pixels that are geometrically within the yellow rectangle's footprint
                 internal_pixels.append({'coord': (r, c), 'color': color})

    return internal_pixels

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    # Step 1: Initialize output grid as a copy of the input
    output_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Step 2: Identify yellow rectangular components and get their bounding boxes
    yellow_rectangles_data = find_yellow_rectangles(input_grid_np)

    objects_to_process = []

    # Step 3: Analyze each yellow rectangle
    for rect_data in yellow_rectangles_data:
        yellow_coords = rect_data['coords'] # The actual coordinates of the yellow pixels
        bbox = rect_data['bbox'] # Bbox of the yellow pixels themselves (min_r, min_c, max_r, max_c)

        # Step 3b: Find internal pixels within this bounding box
        # These are non-yellow, non-white pixels located within the rectangle's area
        internal_pixels = find_internal_pixels(input_grid_np, bbox)

        # Step 3c & 3d: Check if internal pixels exist and share the same color
        if not internal_pixels:
            continue # No internal pixels, skip border drawing for this object

        first_inner_color = internal_pixels[0]['color']
        all_same_color = all(p['color'] == first_inner_color for p in internal_pixels)

        # Step 3e: If conditions met, prepare object data for processing
        if all_same_color:
            inner_color = first_inner_color
            # Step 3.e.i: Border thickness = count of internal pixels
            thickness_t = len(internal_pixels)
            objects_to_process.append({
                'bbox': bbox,
                'inner_color': inner_color,
                'thickness': thickness_t,
                'yellow_coords': yellow_coords # Store the original yellow coords
            })

    # Process the qualified objects. A two-pass approach helps handle overlaps.
    # Pass 1 (Step 3.e.iii): Draw borders onto the output grid
    for obj in objects_to_process:
        min_r, min_c, max_r, max_c = obj['bbox']
        inner_color = obj['inner_color']
        thickness = obj['thickness']

        # Step 3.e.ii: Calculate expanded bounding box coordinates, clamped to grid boundaries
        exp_min_r = max(0, min_r - thickness)
        exp_min_c = max(0, min_c - thickness)
        exp_max_r = min(height - 1, max_r + thickness)
        exp_max_c = min(width - 1, max_c + thickness)

        # Draw the border: fill pixels in the expanded box BUT outside the original box
        for r in range(exp_min_r, exp_max_r + 1):
            for c in range(exp_min_c, exp_max_c + 1):
                # Check if the pixel (r, c) is outside the original bounding box
                is_outside_original_bbox = (r < min_r or r > max_r or c < min_c or c > max_c)
                if is_outside_original_bbox:
                    output_grid_np[r, c] = inner_color

    # Pass 2 (Step 3.e.iv): Ensure the original yellow pixels are restored to yellow
    # This corrects cases where a border might have overwritten part of the yellow shape
    # or if the internal pixels were near the edge and got painted over.
    for obj in objects_to_process:
        yellow_coords = obj['yellow_coords']
        for r, c in yellow_coords:
            # Check bounds just in case, though coords should be valid
            if 0 <= r < height and 0 <= c < width:
                 output_grid_np[r, c] = 4 # Set back to yellow

    # Step 5: Return the modified grid
    return output_grid_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 3 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 2 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 2 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 2 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 4 4 4 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 4 3 4 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 4 4 4 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 4 4 4 4 4 4 4 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 4 4 2 4 4 4 4 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 4 4 4 4 4 4 4 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 4 4 4 4 4 2 4 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 4 2 4 4 4 4 4 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 4 4 4 4 4 4 4 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 3 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 2 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 2 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 2 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 130
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 41.599999999999994

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 2 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 1 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 1 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 1 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 4 4 4 4 4 4 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 4 2 4 4 4 4 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 4 4 4 4 4 4 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 4 4 4 4 4 4 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 4 4 4 2 4 4 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 4 4 4 4 4 4 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 4 4 4 4 4 4 4 4 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 4 4 4 1 4 4 4 4 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 4 4 4 4 4 4 4 4 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 4 1 4 4 4 4 4 4 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 4 4 4 1 4 4 4 4 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 4 4 4 4 4 4 4 4 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 2 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 1 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 1 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 1 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 184
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 58.879999999999995

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 1 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 8 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 8 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 8 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 8 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 4 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 4 1 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 4 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 4 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 4 4 4 4 4 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 8 4 4 4 4 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 4 4 4 4 8 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 4 4 4 4 4 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 4 8 4 4 4 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 4 4 4 4 4 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 4 4 4 4 8 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 4 4 4 4 4 4 4 4 4 4 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 1 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 8 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 8 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 8 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 8 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 228
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 72.96000000000001
