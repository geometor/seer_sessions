
## train_1

**input:**
```
0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 3 3 8 8 0 8 8 8 0 8 0 3 0 0
0 0 0 0 0 0 0 3 8 0 8 8 0 8 8 8 8 3 0 0
0 0 0 0 0 0 0 3 0 8 0 0 6 0 0 8 0 3 0 0
0 0 0 0 0 0 0 3 8 8 6 6 6 6 0 8 8 3 3 0
0 0 0 0 0 0 0 3 8 0 0 6 0 6 0 0 8 3 0 0
0 0 0 0 0 0 0 3 8 8 0 6 6 6 6 8 8 3 3 0
0 0 0 0 0 0 0 3 0 8 0 0 6 0 0 8 0 3 0 0
0 0 0 0 0 0 3 3 8 8 8 8 0 8 8 8 8 3 0 0
0 0 0 0 0 0 0 3 0 8 0 8 8 8 0 8 0 3 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0 0 0 0 3 0 0
0 3 3 3 3 3 3 3 3 3 3 3 0
0 3 0 8 0 8 8 8 0 8 0 3 3
0 3 8 8 8 8 0 8 8 8 8 3 0
0 3 0 8 0 0 6 0 0 8 0 3 3
3 3 8 8 6 6 6 6 0 8 8 3 0
3 3 8 0 0 6 0 6 0 0 8 3 0
0 3 8 8 0 6 6 6 6 8 8 3 0
0 3 0 8 0 0 6 0 0 8 0 3 0
0 3 8 8 8 8 0 8 8 0 8 3 0
0 3 0 8 0 8 8 8 0 8 8 3 0
0 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 3 0 3 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 0 5 5 5 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 3 3 3 3 0 0 5 0 0 0 0
0 0 0 0 0 0 0 3 3 0 4 0 0 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 3 0 4 4 0 3 3 0 0 0 0 0
0 0 0 0 0 0 5 0 3 0 4 4 4 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 3 0 0 0 0 3 0 5 0 0 0 0
0 0 0 0 0 0 5 0 0 3 3 3 3 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 5 5 0 5 5 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 5 0 5 5 5 5 0 5
0 0 0 0 0 0 3 0 0 0
5 0 0 3 3 3 3 0 0 5
0 0 3 0 0 0 0 3 3 5
5 3 3 0 4 4 4 3 0 0
5 0 3 0 4 4 0 3 0 5
5 0 3 0 4 0 0 3 0 5
5 0 0 3 3 3 3 0 0 5
0 0 0 0 0 3 0 0 0 0
5 0 5 5 0 5 5 5 0 5
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 1 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 1 0 0 1 1 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 1 2 2 0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 4 1 0 2 2 1 0 0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 1 1 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 1 1 0 0 0 4 0 0 0 0 0 0 0 0 0
0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 4 0 4 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0
0 4 0 1 1 0 0 0 0 4
4 0 0 1 0 1 0 0 4 0
0 4 1 0 2 2 0 1 0 4
4 0 0 0 2 2 1 1 4 0
0 4 0 1 1 0 1 0 0 4
4 0 0 0 0 1 0 0 4 0
0 4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4 0
```

*   **Perception:** The input grids contain various colored pixels (non-white) scattered on a white background. In each example, there is one prominent, large, contiguous object composed of non-white pixels, along with some smaller, isolated non-white pixels or small groups. The output grid is always a cropped version of the input grid, containing only the largest contiguous object found in the input. The cropping dimensions precisely match the bounding box of this largest object.

*   **YAML Facts:**
    
```yaml
    task_type: object_extraction
    input_properties:
      - background_color: white (0)
      - contains_multiple_objects: true
      - objects_are_contiguous_non_white_pixels: true
      - objects_can_be_different_colors: true
      - objects_vary_in_size: true
    output_properties:
      - background_color: not guaranteed (depends on extracted object)
      - contains_single_object: true (the largest from the input)
      - grid_size: variable (matches bounding box of the extracted object)
    transformation:
      - identify_objects: Find all contiguous regions of non-white pixels in the input.
      - filter_objects: Select the object with the largest area (pixel count).
      - determine_bounds: Find the minimum and maximum row and column indices (bounding box) of the selected largest object.
      - crop_input: Extract the subgrid from the input corresponding to the calculated bounding box.
      - result: The extracted subgrid is the output.
    relationships:
      - The output grid is a subgrid of the input grid.
      - The content of the output grid corresponds exactly to the largest contiguous non-white object from the input, including any white pixels within its bounding box.
      - Smaller non-white objects or pixels outside the bounding box of the largest object are discarded.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all distinct contiguous areas (objects) formed by connected non-white pixels (pixels with values 1 through 9). Consider pixels connected if they are adjacent horizontally or vertically.
    2.  Calculate the size (number of pixels) for each identified object.
    3.  Determine which object has the largest size. If there's a tie, any of the largest objects can be chosen (though the examples don't show ties).
    4.  Find the bounding box of this largest object: determine its minimum row index, maximum row index, minimum column index, and maximum column index.
    5.  Create a new grid whose dimensions are determined by the height (max_row - min_row + 1) and width (max_col - min_col + 1) of the bounding box.
    6.  Copy the pixels from the input grid within the range [min_row, max_row] and [min_col, max_col] into the new output grid, preserving their relative positions.
```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous areas (objects) formed by connected non-white pixels (values 1-9), 
considering horizontal and vertical adjacency. Calculate the size (pixel count) of each object. 
Select the object with the largest size. Determine the bounding box (min/max row and column indices) 
of this largest object. Extract the subgrid from the input corresponding to this bounding box and 
return it as the output.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-white pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-white pixel and not visited yet, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if the neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_object_pixels:
                    objects.append(current_object_pixels)
    return objects

def get_bounding_box(pixels):
    """
    Calculates the bounding box for a list of pixel coordinates.

    Args:
        pixels (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_row, max_row, min_col, max_col)
    """
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Transforms the input grid by extracting the largest contiguous non-white object.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the cropped output grid containing the largest object.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Find all non-white objects
    objects = find_objects(input_np)

    # Handle case where there are no non-white objects
    if not objects:
        # Return an empty grid or the original grid based on interpretation?
        # The examples suggest there's always an object to find.
        # Returning an empty grid might be safer if this case is possible.
         return [[]] # Or potentially return input_grid? Let's assume extraction is always possible based on examples.

    # Find the largest object based on pixel count
    largest_object = max(objects, key=len)

    # Determine the bounding box of the largest object
    min_r, max_r, min_c, max_c = get_bounding_box(largest_object)

    # Crop the input grid using the bounding box coordinates
    # Slicing is [start_row:end_row+1, start_col:end_col+1]
    output_np = input_np[min_r:max_r+1, min_c:max_c+1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```
```python
import numpy as np
import itertools

"""
Identify the bounding box corresponding to the primary cluster of non-white pixels 
by analyzing projections. Find the longest contiguous range of rows containing 
at least one non-white pixel, and the longest contiguous range of columns 
containing at least one non-white pixel. The intersection of these ranges defines 
the bounding box. Extract the subgrid from the input corresponding to this 
bounding box.
"""

def find_longest_contiguous_run(counts):
    """
    Finds the start and end indices of the longest contiguous run of non-zero values.
    If multiple runs have the same max length, returns the first one found.

    Args:
        counts (np.array): A 1D array of counts or indicators (e.g., 0 or 1).

    Returns:
        tuple: (start_index, end_index) of the longest run, or (0, -1) if no non-zero elements.
               The end_index is inclusive.
    """
    max_len = 0
    best_start = 0
    best_end = -1 # Use -1 to indicate no run found yet

    current_len = 0
    current_start = 0

    for i, count in enumerate(counts):
        if count > 0:
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                best_start = current_start
                best_end = i - 1 # Run ended at previous index
            current_len = 0 # Reset run

    # Check if the longest run extends to the end of the array
    if current_len > max_len:
        max_len = current_len
        best_start = current_start
        best_end = len(counts) - 1

    return best_start, best_end


def transform(input_grid):
    """
    Extracts the subgrid corresponding to the primary cluster of non-white pixels.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the cropped output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Handle empty input
    if rows == 0 or cols == 0:
        return [[]]

    # Find non-white pixels
    non_white_pixels = np.argwhere(input_np != 0)

    # Handle case with no non-white pixels
    if non_white_pixels.shape[0] == 0:
        # Return based on expected behavior - maybe empty grid? Or original?
        # Examples imply non-empty output. Let's assume empty grid.
        return [[]] 

    # Project onto rows: count non-white pixels per row
    row_counts = np.zeros(rows, dtype=int)
    unique_rows = np.unique(non_white_pixels[:, 0])
    for r in unique_rows:
        row_counts[r] = 1 # Just need to know if row has > 0 non-white pixels
        
    # Find longest contiguous run of rows with non-white pixels
    min_r, max_r = find_longest_contiguous_run(row_counts)

    # Project onto columns: count non-white pixels per column
    col_counts = np.zeros(cols, dtype=int)
    unique_cols = np.unique(non_white_pixels[:, 1])
    for c in unique_cols:
        col_counts[c] = 1 # Just need to know if col has > 0 non-white pixels

    # Find longest contiguous run of columns with non-white pixels
    min_c, max_c = find_longest_contiguous_run(col_counts)
    
    # Check if valid ranges were found
    if max_r < min_r or max_c < min_c:
        # This shouldn't happen if there are non-white pixels, but as a safeguard
        return [[]] 

    # Crop the input grid using the bounding box coordinates
    # Slicing is [start_row : end_row+1, start_col : end_col+1]
    output_np = input_np[min_r : max_r + 1, min_c : max_c + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```
