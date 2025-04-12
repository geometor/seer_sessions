
## train_1

**input:**
```
0 2 2 2 2 2 2 2
1 8 8 8 8 8 8 8
1 8 4 4 8 9 9 8
1 8 4 4 8 9 9 8
1 8 8 8 8 8 8 8
1 8 8 8 8 8 8 8
1 8 1 6 8 4 4 8
1 8 2 6 8 4 4 8
1 8 6 6 8 8 8 8
1 8 6 6 8 8 8 8
1 8 6 6 8 4 7 8
1 8 6 6 8 7 4 8
1 8 8 8 8 7 7 8
1 8 8 8 8 7 7 8
1 8 3 6 8 7 7 8
1 8 3 6 8 7 7 8
1 8 3 3 8 8 8 8
1 8 3 3 8 8 8 8
1 8 8 8 8 8 8 8
1 8 8 8 8 8 8 8
```


**output:**
```
8 8 4 4 8 8
8 8 4 4 8 8
6 6 6 6 6 6
1 2 6 6 6 6
8 6 6 3 3 8
8 3 3 3 3 8
8 8 9 9 8 8
8 8 9 9 8 8
8 8 4 4 8 8
8 8 4 4 8 8
7 4 7 7 7 7
4 7 7 7 7 7
```


## train_2

**input:**
```
0 1 1 1 1 1 1 1 1 1 1
2 8 8 8 8 8 8 8 8 8 8
2 8 3 3 8 8 4 4 4 4 8
2 8 3 3 8 8 4 4 4 4 8
2 8 8 8 8 8 8 8 8 8 8
2 8 6 6 8 8 9 9 8 8 8
2 8 6 6 8 8 9 9 8 8 8
2 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 3 3 8
8 3 3 8
4 4 4 4
4 4 4 4
8 6 6 8
8 6 6 8
8 9 9 8
8 9 9 8
```


## train_3

**input:**
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 8 3 3 3 3 3 3 3 3 8 8 9 9 8 8 7 7 7 7 8 8 4 4 4 4 8 8
2 8 3 3 3 3 3 3 3 3 8 8 9 9 8 8 7 7 7 7 8 8 4 4 4 4 8 8
2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 8 9 9 8 8 6 6 6 6 6 6 6 6 8 8 4 4 8 8 8 8 8 8 8 8 8 8
2 8 9 9 8 8 6 6 6 6 6 6 6 6 8 8 4 4 8 8 8 8 8 8 8 8 8 8
2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
8 8 8 9 9 8 8 8
8 8 8 9 9 8 8 8
8 8 7 7 7 7 8 8
8 8 7 7 7 7 8 8
8 8 4 4 4 4 8 8
8 8 4 4 4 4 8 8
8 8 8 9 9 8 8 8
8 8 8 9 9 8 8 8
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
8 8 8 4 4 8 8 8
8 8 8 4 4 8 8 8
```


## train_4

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2
8 3 3 3 3 3 3 8 8 7 7 8 8 3 3 8 8 4 4 4 4 8 2
8 3 3 3 3 3 3 8 8 7 7 8 8 3 3 8 8 4 4 4 4 8 2
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2
8 8 8 8 8 3 3 3 3 8 8 6 6 6 6 6 6 8 8 9 9 8 2
8 8 8 8 8 3 3 3 3 8 8 6 6 6 6 6 6 8 8 9 9 8 2
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2
```


**output:**
```
8 4 4 4 4 8
8 4 4 4 4 8
8 8 3 3 8 8
8 8 3 3 8 8
8 8 7 7 8 8
8 8 7 7 8 8
3 3 3 3 3 3
3 3 3 3 3 3
8 8 9 9 8 8
8 8 9 9 8 8
6 6 6 6 6 6
6 6 6 6 6 6
8 3 3 3 3 8
8 3 3 3 3 8
```

Okay, let's break down the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both inputs and outputs are grids of numbers (0-9).
2.  **Core Data vs. Borders:** The input grids have border rows/columns often marked with `0`, `1`, or `2`. The central part of the input grid, typically padded with `8`s, contains the essential information. The digit `8` seems to act as a background or separator color.
3.  **Objects:** Within the core input grid, there are distinct shapes or "objects" formed by connected cells containing digits other than `8`. These objects are composed of one or more non-`8` digits. Connectivity appears to be 4-way (up, down, left, right).
4.  **Transformation:** The core task is to identify these non-`8` objects, extract them, potentially resize/pad them, and arrange them vertically to form the output grid.
5.  **Padding:** Padding with the digit `8` is applied to some extracted objects to adjust their width.
6.  **Ordering:** The extracted and potentially padded objects are stacked vertically in the output. Their order seems determined by their original top-to-bottom, left-to-right position in the input grid.

**YAML Facts:**

```yaml
task_description: Extract connected non-background objects from a core grid, pad them to a consistent width determined by the widest object, and stack them vertically.

definitions:
  grid: A 2D array of digits.
  background_color: 8
  border_markers: [0, 1, 2] # Digits indicating border rows/columns
  core_grid: The portion of the input grid excluding border rows/columns and potentially outer layers of background_color.
  object: A connected component of cells in the core_grid containing digits other than the background_color. Connectivity is 4-way.
  bounding_box: The smallest rectangle enclosing an object.
  object_subgrid: The content of the grid within an object's bounding box.

actions:
  - identify_core_grid: Determine the relevant subgrid from the input, excluding borders.
  - find_objects: Locate all connected components of non-background_color digits within the core_grid.
  - extract_subgrids: For each object, extract the subgrid corresponding to its bounding_box.
  - determine_target_width: Find the maximum width among all extracted object_subgrids.
  - pad_subgrids: For each extracted object_subgrid whose width is less than the target_width, pad it symmetrically with the background_color on the left and right until its width equals the target_width.
  - order_subgrids: Arrange the (potentially padded) subgrids based on the top-left coordinate of their corresponding object's bounding_box in the core_grid (top-to-bottom, then left-to-right).
  - concatenate_subgrids: Stack the ordered subgrids vertically to create the final output grid.

relationships:
  - The output grid is composed of modified representations of the objects found in the input's core_grid.
  - The width of the output grid is determined by the width of the widest object found in the input's core_grid.
  - The order of object representations in the output corresponds to the spatial order of the objects in the input.
  - Padding uses the background_color (8).

observation_notes:
  - This rule accurately describes the transformation for examples train_2, train_3, and train_4.
  - Example train_1 appears anomalous under this rule. Its output width (6) does not match the maximum object width (2), and some output subgrids do not seem to result from simple padding of the extracted objects (e.g., `1 2 6 6 6 6` from `[[1,6],[2,6]]`). Further investigation might be needed for train_1, possibly involving a different padding rule or object manipulation based on aspect ratio or other properties specific to that example's border markers.
```

**Natural Language Program:**

1.  **Identify the Core Grid:** Examine the input grid. Ignore any border rows or columns potentially indicated by markers like 0, 1, or 2. The core grid is the central area containing patterns surrounded by the background color 8.
2.  **Find Objects:** Scan the core grid to find all connected areas (objects) made of digits *not* equal to 8. Use 4-way connectivity (up, down, left, right) to define connections. Keep track of the pixels belonging to each distinct object.
3.  **Extract Object Subgrids:** For each identified object, determine its bounding box (the smallest rectangle containing all its pixels). Extract the subgrid of digits within this bounding box.
4.  **Determine Target Width:** Examine all the extracted object subgrids and find the maximum width among them. This maximum width will be the target width for the output blocks.
5.  **Order Objects:** Sort the extracted object subgrids based on the original position of their corresponding object's top-left corner in the core grid. The primary sort key is the row index (top to bottom), and the secondary key is the column index (left to right).
6.  **Pad and Assemble:** Process the sorted object subgrids one by one:
    *   Take the current object subgrid.
    *   If its width is less than the target width calculated in step 4, add columns of the background color 8 symmetrically to its left and right sides until its width matches the target width. (If an odd number of padding columns are needed, add the extra column to the right).
    *   Append this (potentially padded) subgrid to the bottom of the final output grid being built.
7.  **Final Output:** The fully assembled grid after processing all objects is the final output.
```python
import numpy as np
from collections import deque

"""
Identifies connected components (objects) of digits other than 8 (background) in the input grid.
Calculates the bounding box for each object and extracts the corresponding subgrid from the original input grid.
Determines the maximum width among all extracted object subgrids.
Sorts the subgrids based on the top-left coordinate of their original bounding box (top-to-bottom, then left-to-right).
Pads each subgrid symmetrically with the background color (8) to match the maximum width.
Stacks the padded subgrids vertically in their sorted order to create the output grid.

Note: This logic is derived primarily from examples train_2, train_3, and train_4. 
Example train_1 appears to follow a different padding or width determination rule 
and may not be handled correctly by this implementation, as its output width (6) 
does not match the maximum width of its input objects (2).
"""

# Helper function to find connected components (objects) of non-background pixels using BFS
def _find_objects(grid_np: np.ndarray, background_color: int) -> list[dict]:
    """
    Finds all connected components of non-background pixels.

    Args:
        grid_np: The input grid as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'bounds' (min_r, max_r, min_c, max_c) and
        'top_left' coordinate (min_r, min_c) for sorting.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if we find a non-background cell that hasn't been visited
            if grid_np[r, c] != background_color and not visited[r, c]:
                component_pixels = [] # Store coordinates (r, c) of pixels in this component
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))

                    # Explore neighbors (4-way connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid_np[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_pixels:
                    # Calculate bounding box after finding all pixels for the component
                    obj_min_r = min(px[0] for px in component_pixels)
                    obj_max_r = max(px[0] for px in component_pixels)
                    obj_min_c = min(px[1] for px in component_pixels)
                    obj_max_c = max(px[1] for px in component_pixels)
                    
                    objects.append({
                        'bounds': (obj_min_r, obj_max_r, obj_min_c, obj_max_c),
                        'top_left': (obj_min_r, obj_min_c) # Use top-left for sorting
                    })

    # Sort objects based on their top-left corner (top-to-bottom, then left-to-right)
    objects.sort(key=lambda obj: obj['top_left'])
    return objects

# Helper function to extract the subgrid based on bounding box
def _extract_subgrid(grid_np: np.ndarray, bounds: tuple) -> np.ndarray:
    """
    Extracts the rectangular subgrid defined by the bounds from the grid.
    """
    min_r, max_r, min_c, max_c = bounds
    # Slice the numpy array to get the subgrid
    return grid_np[min_r:max_r+1, min_c:max_c+1]

# Helper function to pad a subgrid symmetrically to a target width
def _pad_subgrid(subgrid_np: np.ndarray, target_width: int, background_color: int) -> np.ndarray:
    """
    Pads a subgrid with the background color to reach the target width.
    Padding is applied symmetrically (left and right).
    """
    if subgrid_np is None or subgrid_np.size == 0:
        # Return an empty array or handle as error if needed
        return np.array([[]], dtype=int) 
        
    current_height, current_width = subgrid_np.shape

    if current_width == target_width:
        return subgrid_np # No padding needed
    elif current_width > target_width:
         # This case should not happen if target_width is the max width found
         # Return original subgrid if it does
         return subgrid_np

    # Calculate padding amounts
    padding_needed = target_width - current_width
    left_padding = padding_needed // 2
    right_padding = padding_needed - left_padding

    # Create padding arrays filled with the background color
    left_pad_arr = np.full((current_height, left_padding), background_color, dtype=subgrid_np.dtype)
    right_pad_arr = np.full((current_height, right_padding), background_color, dtype=subgrid_np.dtype)

    # Concatenate horizontally: left_padding + subgrid + right_padding
    padded_subgrid = np.concatenate((left_pad_arr, subgrid_np, right_pad_arr), axis=1)
    return padded_subgrid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by extracting non-background objects, padding them
    to a uniform width (based on the widest object), and stacking them vertically.
    """
    
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []

    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    background_color = 8

    # --- Step 1: Find all non-background objects and their bounding boxes ---
    # Objects are returned sorted by their top-left position.
    objects = _find_objects(input_np, background_color)

    # Handle case where no objects are found
    if not objects:
        return [] 

    # --- Step 2: Extract the subgrid for each object ---
    extracted_subgrids = []
    for obj in objects:
        subgrid = _extract_subgrid(input_np, obj['bounds'])
        extracted_subgrids.append(subgrid)

    # --- Step 3: Determine the target width (max width among all extracted subgrids) ---
    if not extracted_subgrids:
         return [] # Should be caught by object check, but defensive programming
    
    max_width = 0
    for subgrid in extracted_subgrids:
        # Check if subgrid is valid and has 2 dimensions before accessing shape[1]
        if subgrid is not None and subgrid.ndim == 2 and subgrid.shape[1] > 0:
             max_width = max(max_width, subgrid.shape[1])
        # Consider 1D arrays or single elements if they could occur (width 1)
        elif subgrid is not None and subgrid.size > 0:
             max_width = max(max_width, 1) # Width is 1 for a 1D array or single element

    # If max_width remains 0 (e.g., all objects were empty?), return empty
    if max_width == 0:
        return []

    # --- Step 4: Pad each extracted subgrid to the determined maximum width ---
    # The order of subgrids matches the sorted order of objects found earlier.
    padded_subgrids = []
    for subgrid in extracted_subgrids:
         # Ensure subgrid is valid before padding
         if subgrid is not None and subgrid.size > 0:
            padded = _pad_subgrid(subgrid, max_width, background_color)
            padded_subgrids.append(padded)

    # --- Step 5: Concatenate padded subgrids vertically to form the output grid ---
    if not padded_subgrids:
        return [] # No valid subgrids to stack

    # Use numpy's vstack for vertical concatenation
    output_np = np.vstack(padded_subgrids)

    # --- Step 6: Convert the final numpy array back to a list of lists ---
    output_grid = output_np.tolist()

    return output_grid
```
