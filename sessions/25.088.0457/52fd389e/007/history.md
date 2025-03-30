
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
## General Assessment

The previous code failed because it incorrectly assumed that the triggering object must be a *solid* yellow rectangle. The examples show that the object is a contiguous group of yellow pixels which may contain "holes" filled with other colors. The transformation rule applies if these "holes" (internal pixels that are not yellow and not white) within the bounding box of the yellow component *all share the same color*. The number of these internal pixels determines the thickness of the border, and their shared color determines the border color.

The strategy is to:
1.  Correctly identify contiguous components of yellow pixels.
2.  Determine the bounding box for each yellow component.
3.  Identify all non-yellow, non-white pixels strictly *within* that bounding box.
4.  Verify if these internal pixels exist and all share a single color.
5.  If the condition is met, calculate the border thickness (count of internal pixels) and color (shared color of internal pixels).
6.  Draw the border by expanding the bounding box outwards by the calculated thickness, filling the new area with the border color.
7.  Ensure the original yellow pixels within the bounding box remain yellow in the final output.

## Metrics and Observations

**Example 1:**

*   **Input:** Contains two yellow components.
    *   Component 1 (Top): Bounding box (rows 2-4, cols 3-5). Contains 1 internal non-yellow/non-white pixel: Green (3) at (3,4).
    *   Component 2 (Bottom): Bounding box (rows 12-17, cols 11-17). Contains 4 internal non-yellow/non-white pixels: Red (2) at (13,13), (15,16), (16,12), (16,16).
*   **Expected Output:**
    *   Component 1: Gets a Green (3) border of thickness 1.
    *   Component 2: Gets a Red (2) border of thickness 4.
*   **Analysis:** The internal pixels for each component share a single color (Green for component 1, Red for component 2). The border thickness matches the count of internal pixels for each component.

**Example 2:**

*   **Input:** Contains two yellow components.
    *   Component 1 (Top): Bounding box (rows 2-7, cols 2-7). Contains 2 internal non-yellow/non-white pixels: Red (2) at (3,3) and (6,5).
    *   Component 2 (Bottom): Bounding box (rows 15-20, cols 13-20). Contains 3 internal non-yellow/non-white pixels: Blue (1) at (16,16), (18,14), (19,16).
*   **Expected Output:**
    *   Component 1: Gets a Red (2) border of thickness 2.
    *   Component 2: Gets a Blue (1) border of thickness 3.
*   **Analysis:** The internal pixels for each component share a single color (Red for component 1, Blue for component 2). The border thickness matches the count of internal pixels for each component.

**Example 3:**

*   **Input:** Contains two yellow components.
    *   Component 1 (Top): Bounding box (rows 2-5, cols 6-9). Contains 1 internal non-yellow/non-white pixel: Blue (1) at (3,7).
    *   Component 2 (Bottom): Bounding box (rows 12-19, cols 8-17). Contains 4 internal non-yellow/non-white pixels: Azure (8) at (13,10), (14,14), (16,11), (18,14).
*   **Expected Output:**
    *   Component 1: Gets a Blue (1) border of thickness 1.
    *   Component 2: Gets an Azure (8) border of thickness 4.
*   **Analysis:** The internal pixels for each component share a single color (Blue for component 1, Azure for component 2). The border thickness matches the count of internal pixels for each component.

## YAML Fact Sheet


```yaml
task_context:
  description: Draw a border around specific yellow structures based on internal pixels.
  input_grid: Represents a 2D space with colored pixels (0-9).
  output_grid: Input grid modified by adding colored borders around qualifying structures.

objects:
  - object: yellow_component
    description: A contiguous group of yellow (4) pixels (connected via 4-way adjacency). It may not form a solid rectangle.
    properties:
      - color: yellow (4)
      - coordinates: Set of (row, col) tuples for each yellow pixel in the component.
      - bounding_box: The minimum rectangle enclosing all pixels of the yellow component (min_row, min_col, max_row, max_col).
  - object: internal_pixel
    description: A pixel located within the bounding box of a yellow component that is NOT yellow (4) and NOT white (0).
    properties:
      - color: Any color except yellow (4) or white (0).
      - location: (row, col) coordinate within the yellow component's bounding box.
  - object: border
    description: A colored frame drawn around the bounding box of a qualifying yellow component.
    properties:
      - color: Determined by the shared color of the internal pixels of the associated yellow component.
      - thickness: Determined by the count of internal pixels of the associated yellow component.
      - location: The area between the original bounding box and an expanded bounding box.

actions:
  - action: identify_yellow_components
    description: Find all distinct contiguous groups of yellow pixels in the input grid.
    inputs: input_grid
    outputs: List of yellow_component objects (including their coordinates and bounding_box).
  - action: find_internal_pixels
    description: For a given yellow component's bounding box, find all pixels within that box that are neither yellow nor white.
    inputs: input_grid, bounding_box
    outputs: List of internal_pixel objects (including their color and location).
  - action: check_conditions_for_border
    description: Determine if a yellow component qualifies for a border.
    inputs: List of internal_pixels found for a yellow component.
    outputs: Boolean (True if internal pixels exist AND they all share the same color).
    conditions:
      - Must be at least one internal_pixel.
      - All internal_pixels must have the same color value.
  - action: calculate_border_properties
    description: Determine the color and thickness of the border.
    inputs: List of internal_pixels for a qualifying yellow component.
    outputs: border_color (the shared color), border_thickness (the count of internal pixels).
  - action: draw_border
    description: Modify the output grid to add the border.
    inputs: output_grid, bounding_box, border_color, border_thickness
    process:
      - Calculate the expanded bounding box by extending the original bounding box outwards by 'border_thickness'.
      - Fill pixels in the output_grid that are within the expanded bounding box but outside the original bounding box with the 'border_color'.
  - action: preserve_yellow_component
    description: Ensure the original yellow pixels of the component are retained in the output grid.
    inputs: output_grid, coordinates of the yellow_component
    process: Set the color of pixels at the yellow component's coordinates back to yellow (4). This handles cases where the border might overwrite parts of the component.

workflow:
  - Initialize output_grid as a copy of input_grid.
  - Identify all yellow_components in the input_grid.
  - Create a list to store components that qualify for a border and their border properties.
  - For each yellow_component:
    - Find its internal_pixels using its bounding_box.
    - Check if the component qualifies for a border based on its internal_pixels.
    - If it qualifies:
      - Calculate the border_color and border_thickness.
      - Store the component's bounding_box, original yellow coordinates, border_color, and border_thickness.
  - For each qualifying component (from the stored list):
    - draw_border onto the output_grid using its bounding_box, border_color, and border_thickness.
  - For each qualifying component (from the stored list):
    - preserve_yellow_component by setting its original yellow coordinates back to yellow (4) on the output_grid.
  - Return the final output_grid.

```


## Natural Language Program

1.  **Initialization**: Create an output grid as an exact copy of the input grid.
2.  **Identify Yellow Components**: Find all distinct, contiguous groups of yellow (4) pixels in the input grid using 4-way adjacency. For each component found:
    a.  Record the set of coordinates `(r, c)` for all yellow pixels belonging to this component.
    b.  Determine the minimal bounding box `(min_r, min_c, max_r, max_c)` that encloses all yellow pixels of this component.
3.  **Analyze Each Component**: For every identified yellow component and its bounding box:
    a.  **Find Internal Pixels**: Search within the component's bounding box `(min_r, min_c, max_r, max_c)` in the *input* grid. Identify all pixels whose color is *not* yellow (4) and *not* white (0). Record the color and coordinates of each such internal pixel found.
    b.  **Check Border Conditions**: Examine the list of internal pixels found for the component:
        i.  If no internal pixels were found, this component does not get a border. Proceed to the next component.
        ii. If internal pixels *were* found, check if they *all* share the exact same color.
        iii.If they do not all share the same color, this component does not get a border. Proceed to the next component.
    c.  **Qualify for Border**: If internal pixels exist and they all share the same single color (let's call this the `inner_color`), then this component qualifies for a border.
        i.  **Calculate Thickness**: The border thickness (`T`) is equal to the total *number* of internal pixels found for this component.
        ii. **Store Information**: Keep track of the component's original yellow pixel coordinates, its bounding box, the calculated `inner_color`, and the calculated thickness `T`.
4.  **Draw Borders**: After analyzing all yellow components, iterate through the list of *qualifying* components:
    a.  For each qualifying component, retrieve its bounding box `(min_r, min_c, max_r, max_c)`, `inner_color`, and thickness `T`.
    b.  **Calculate Expanded Box**: Determine the coordinates of an expanded bounding box by extending the original bounding box outwards by `T` pixels in all four directions (up, down, left, right). Ensure these coordinates stay within the grid boundaries (clamp at 0 and grid dimension minus 1). Let the expanded box be `(exp_min_r, exp_min_c, exp_max_r, exp_max_c)`.
    c.  **Fill Border Area**: Iterate through all coordinates `(r, c)` within the *expanded* bounding box. If a coordinate `(r, c)` falls *outside* the *original* bounding box (`r < min_r` or `r > max_r` or `c < min_c` or `c > max_c`), set the color of the pixel at `(r, c)` in the *output* grid to the `inner_color`.
5.  **Preserve Original Yellow**: After drawing all borders, iterate through the list of *qualifying* components again:
    a.  For each qualifying component, retrieve the set of its original yellow pixel coordinates.
    b.  For every coordinate `(r, c)` in this set, set the color of the pixel at `(r, c)` in the *output* grid back to yellow (4). This ensures the original yellow shape is preserved and corrects any pixels that might have been overwritten by a border.
6.  **Final Output**: Return the modified output grid.
