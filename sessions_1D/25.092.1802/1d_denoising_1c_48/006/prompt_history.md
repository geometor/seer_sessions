
## train_1

**input:**
```
0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0
```


## train_2

**input:**
```
0 0 0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 6 0 0 0 6 0 0 0 0 6 0 0 0 0
```


**output:**
```
0 0 0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 8 0 0 8 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
```

*   **Perception:** The task involves transforming an input grid into an output grid. Both input and output grids seem to have the same dimensions (likely 4x8 based on the 32 elements provided). The input grids contain a background color (white, 0) and one other foreground color (blue, magenta, or azure). The transformation appears to isolate a single row from the input grid and place it in the corresponding position in the output grid, while all other rows in the output grid are filled with the background color (white). The key is to determine which row from the input is selected. By analyzing the examples, it appears the row selected is the one containing the highest count of the foreground color. If multiple rows share the highest count, the topmost (first) of these rows is selected.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    grid_properties:
      dimensionality: 2D
      background_color: 0 # white
    input_characteristics:
      - contains_background: true
      - contains_single_foreground_color: true # Based on examples
      - foreground_colors_observed: [1, 6, 8] # blue, magenta, azure
    output_characteristics:
      - contains_background: true
      - contains_single_row_from_input: true
      - other_rows_are_background: true
    transformation_logic:
      selection_criterion: row_based
      criterion_details:
        - identify_foreground_color: Determine the non-white color present.
        - count_pixels: Count the occurrences of the foreground color in each row.
        - find_max_count: Determine the maximum count among all rows.
        - select_row: Choose the first row (from top to bottom) that achieves the maximum count.
      output_construction:
        - copy_selected_row: Place the selected row into the corresponding row of the output grid.
        - fill_background: Set all other rows in the output grid to the background color (0).
    uncertainties:
      - behavior_with_multiple_foreground_colors: Not observed in examples. Assuming only one foreground color exists per input.
      - grid_dimensions: Assumed based on data length (32 -> 4x8). Need confirmation if other dimensions are possible.

    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (height `H` and width `W`) of the input grid.
    2.  Identify the primary foreground color (any color other than white/0) present in the input grid. Assume there is only one such color.
    3.  Initialize variables: `max_count` to -1, `selected_row_index` to -1.
    4.  Iterate through each row of the input grid from top to bottom (index `r` from 0 to `H-1`).
        a.  Count the number of pixels in the current row (`r`) that match the identified foreground color. Let this be `current_count`.
        b.  If `current_count` is greater than `max_count`:
            i.  Update `max_count` to `current_count`.
            ii. Update `selected_row_index` to `r`.
    5.  Create a new output grid of the same dimensions (`H` x `W`), initially filled with the background color (white, 0).
    6.  If a `selected_row_index` was found (i.e., `selected_row_index` is not -1, meaning there was at least one foreground pixel):
        a.  Copy the row from the input grid at index `selected_row_index` to the output grid at the same index `selected_row_index`.
    7.  Return the generated output grid.
```python
import numpy as np
import collections

"""
Identify the primary foreground color (non-white/0) in the input grid.
Iterate through each row of the input grid and count the occurrences of this foreground color.
Determine the row index that contains the maximum count of the foreground color. If multiple rows share the maximum count, select the topmost row (smallest row index).
Create an output grid of the same dimensions as the input, filled entirely with the background color (white/0).
Copy the selected row from the input grid into the corresponding row of the output grid.
Return the modified output grid.
"""

def find_foreground_color(grid):
    """Finds the first non-zero color in the grid."""
    for row in grid:
        for pixel in row:
            if pixel != 0:
                return pixel
    return 0 # Return background color if no foreground color is found

def transform(input_grid):
    """
    Transforms the input grid by selecting the row with the most foreground pixels
    and placing it in an otherwise background-filled grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize output_grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Identify the foreground color
    # Assumes only one foreground color exists besides background (0)
    foreground_color = find_foreground_color(input_array)

    # If no foreground color exists (grid is all background), return the all-background grid
    if foreground_color == 0:
        return output_array.tolist()

    # Initialize variables to track the row with the maximum count
    max_count = -1
    selected_row_index = -1

    # Iterate through each row to find the one with the most foreground pixels
    for r in range(height):
        # Count occurrences of the foreground color in the current row
        current_count = np.count_nonzero(input_array[r, :] == foreground_color)

        # Update max_count and selected_row_index if current count is higher
        # We only update if strictly greater, ensuring the first row is kept in case of ties
        if current_count > max_count:
            max_count = current_count
            selected_row_index = r

    # If a row with foreground pixels was found (max_count > 0 implies selected_row_index is valid)
    if selected_row_index != -1:
        # Copy the selected row from the input to the output grid
        output_array[selected_row_index, :] = input_array[selected_row_index, :]

    # Convert the numpy array back to a list of lists for the standard ARC format
    return output_array.tolist()
```
```python
import numpy as np
import collections

"""
Identify the primary foreground color (non-white/0) in the input grid.
Iterate through each row of the input grid and count the occurrences of this foreground color.
Determine the row index that contains the maximum count of the foreground color. 
If multiple rows share the maximum count, select the topmost row (the one with the smallest row index).
Create an output grid of the same dimensions as the input, filled entirely with the background color (white/0).
Copy the selected row (the topmost row with the maximum foreground pixel count) from the input grid into the corresponding row of the output grid.
Return the modified output grid.
"""

def find_foreground_color(grid):
    """
    Finds the first non-zero (non-background) color encountered in the grid.
    Assumes there is at most one non-background color per grid based on examples.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The foreground color value, or 0 if only background is present.
    """
    for row in grid:
        for pixel in row:
            if pixel != 0:
                return pixel
    return 0 # Return background color (0) if no foreground color is found

def transform(input_grid):
    """
    Transforms the input grid by selecting the topmost row with the maximum 
    count of the foreground color and placing it in an otherwise background-filled grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input grid case
    if input_array.size == 0:
        return []
        
    height, width = input_array.shape

    # Initialize output_grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Identify the foreground color
    # Assumes only one foreground color exists besides background (0) based on examples.
    foreground_color = find_foreground_color(input_array)

    # If no foreground color exists (grid is all background), 
    # return the already initialized all-background grid.
    if foreground_color == 0:
        return output_array.tolist()

    # Initialize variables to track the row with the maximum count
    max_count = -1  # Start with -1 to ensure any count >= 0 is initially larger
    selected_row_index = -1 # Initialize to invalid index

    # Iterate through each row to find the *first* one with the maximum foreground pixel count
    for r in range(height):
        # Count occurrences of the foreground color in the current row
        current_count = np.count_nonzero(input_array[r, :] == foreground_color)

        # Update max_count and selected_row_index if the current count is strictly greater
        # than the current maximum. This automatically selects the topmost row in case of ties,
        # as later rows with the same count won't overwrite the selected_row_index.
        if current_count > max_count:
            max_count = current_count
            selected_row_index = r

    # If a row with at least one foreground pixel was found (meaning selected_row_index is valid)
    # The check `max_count > 0` ensures we don't copy an all-background row if that happened
    # to be selected (e.g., if input had only background but find_foreground_color returned something else erroneously).
    # The check selected_row_index != -1 is redundant if max_count > 0 but good for clarity.
    if selected_row_index != -1 and max_count > 0:
        # Copy the selected row from the input to the output grid at the same row index
        output_array[selected_row_index, :] = input_array[selected_row_index, :]

    # Convert the resulting numpy array back to a list of lists for the standard ARC format
    return output_array.tolist()
```
```python
import numpy as np
from collections import deque

"""
Identify the single foreground color (C) in the input grid.
Find all distinct connected objects composed of this foreground color C, using cardinal (4-way) adjacency.
Determine the row index ('max_row_idx') that contains the highest count of color C. If multiple rows share the highest count, select the topmost row (smallest index).
Identify the specific object(s) that have at least one pixel located within 'max_row_idx'.
Create an output grid of the same dimensions as the input, filled entirely with the background color (0).
Copy only the pixels belonging to the identified target object(s) from the input grid to the corresponding positions in the output grid.
"""

def find_foreground_color(grid):
    """
    Finds the first non-zero (non-background) color encountered in the grid.
    Assumes there is at most one non-background color per grid based on examples.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The foreground color value, or 0 if only background is present.
    """
    for pixel in grid.flat:
        if pixel != 0:
            return pixel
    return 0 # Return background color (0) if no foreground color is found

def find_max_row(grid, foreground_color):
    """
    Finds the index of the row containing the maximum number of foreground_color pixels.
    Ties are broken by choosing the lowest row index (topmost).

    Args:
        grid (np.array): The input grid.
        foreground_color (int): The color to count.

    Returns:
        int: The index of the row with the maximum count, or -1 if the color is not found.
    """
    max_count = -1
    max_row_idx = -1
    height = grid.shape[0]

    if foreground_color == 0: # Cannot find max row for background color meaningfully in this context
        return -1

    for r in range(height):
        current_count = np.count_nonzero(grid[r, :] == foreground_color)
        if current_count > max_count:
            max_count = current_count
            max_row_idx = r
            
    # If max_count is still 0 after checking all rows, the color wasn't present
    if max_count == 0:
      return -1
      
    return max_row_idx

def find_connected_components(grid, foreground_color):
    """
    Finds all connected components (objects) of a given foreground color using BFS.
    Connectivity is 4-directional (cardinal).

    Args:
        grid (np.array): The input grid.
        foreground_color (int): The color of the objects to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of pixels in a connected component.
                   Returns an empty list if foreground_color is 0 or not found.
    """
    if foreground_color == 0:
        return []
        
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] == foreground_color and not visited[r, c]:
                # Start BFS for a new object
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if it's a valid, unvisited pixel of the object
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == foreground_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append(current_object_coords)
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on selecting the object(s) connected
    to the row with the most foreground pixels.
    """
    # Convert input to numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input grid case
    if input_array.size == 0:
        return []
        
    height, width = input_array.shape

    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array)

    # Find the foreground color
    foreground_color = find_foreground_color(input_array)

    # If no foreground color, return the background grid
    if foreground_color == 0:
        return output_array.tolist()

    # Find the row with the maximum count of the foreground color
    max_row_idx = find_max_row(input_array, foreground_color)

    # If the foreground color wasn't actually found (e.g., max count was 0), return background
    if max_row_idx == -1:
         return output_array.tolist()

    # Find all connected components (objects) of the foreground color
    all_objects = find_connected_components(input_array, foreground_color)

    # Identify target objects: those intersecting the max_row_idx
    target_objects_pixels = set()
    for obj_coords in all_objects:
        # Check if any pixel in this object lies on the max_row_idx
        intersects_max_row = any(r == max_row_idx for r, c in obj_coords)
        if intersects_max_row:
            # Add all pixels of this object to the set of pixels to keep
            target_objects_pixels.update(obj_coords)

    # Populate the output grid with the pixels from the target objects
    for r, c in target_objects_pixels:
        # Ensure coordinates are valid just in case (should be by construction)
        if 0 <= r < height and 0 <= c < width:
             output_array[r, c] = foreground_color

    # Convert back to list of lists and return
    return output_array.tolist()
```
