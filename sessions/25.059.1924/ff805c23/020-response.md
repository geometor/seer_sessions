# ff805c23 • 020 • refine_coder

---
```python
"""
1.  **Identify the Grey Object:** Find the contiguous block of grey (value 5) pixels in the input grid.  This forms the "target object".
2.  **Determine Bounding Box:** Calculate the bounding box of the *target object*. This is the smallest rectangle that fully encloses all grey pixels of the target object.
3.  **Create Output Grid:** Create an output grid with dimensions equal to the height and width of the bounding box.
4.  **Copy Pixels within Bounding Box:** Iterate through each cell within the bounding box in the *input* grid. Copy the color of the pixel at that location to the corresponding location in the *output* grid. The top-left corner of the bounding box in the input maps to position (0, 0) in the output grid.
5. **Ignore the isolated grey objects**: Grey objects that do not form a contiguous object with any other color should be ignored.
"""

import numpy as np

def find_grey_object_bounding_box(grid):
    # Find all grey pixels
    grey_coords = np.argwhere(grid == 5)
    if grey_coords.size == 0:
        return None, 0, 0, 0, 0

    # Check for contiguity with other colors
    contiguous_grey_coords = []
    rows, cols = grid.shape
    for r, c in grey_coords:
        is_contiguous = False
        # Check neighbors (including diagonals)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nr, nc = r + i, c + j
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != 5 and grid[nr,nc] != 0:
                    is_contiguous = True
                    break
            if is_contiguous:
                break
        if is_contiguous:
            contiguous_grey_coords.append((r, c))
    
    if not contiguous_grey_coords:
         return None, 0, 0, 0, 0

    contiguous_grey_coords = np.array(contiguous_grey_coords)
    # Calculate bounding box
    min_row = np.min(contiguous_grey_coords[:, 0])
    max_row = np.max(contiguous_grey_coords[:, 0])
    min_col = np.min(contiguous_grey_coords[:, 1])
    max_col = np.max(contiguous_grey_coords[:, 1])

    return contiguous_grey_coords, min_row, min_col, max_row - min_row + 1, max_col - min_col + 1

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the grey object's bounding box
    object_coords, min_row, min_col, obj_height, obj_width = find_grey_object_bounding_box(input_grid)

    if object_coords is None:
        return input_grid.tolist() # Return original if no suitable grey object
    # Create output grid with bounding box dimensions
    output_grid = np.zeros((obj_height, obj_width), dtype=int)

    # Copy pixels within the bounding box
    for r in range(obj_height):
        for c in range(obj_width):
            input_row = min_row + r
            input_col = min_col + c
            if 0 <= input_row < input_grid.shape[0] and 0<= input_col < input_grid.shape[1]:
                output_grid[r, c] = input_grid[input_row, input_col]

    return output_grid.tolist()
```
