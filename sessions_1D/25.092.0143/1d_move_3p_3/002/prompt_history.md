
## train_1

**input:**
```
0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 0 0
```

*   **Perception**: The input and output are both single rows of pixels. Each input contains a contiguous block of a single non-white color surrounded by white pixels. The output shows the same colored block shifted three positions to the right, with the rest of the row remaining white. The color and length of the block are preserved.

*   **Facts**:
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively a 1D array or list
    components:
      - object: colored_block
        count: 1
        properties:
          - color: non-white (red, orange, magenta in examples)
          - shape: contiguous horizontal segment
          - size: variable length (11, 10, 6 in examples)
          - location: variable start index within the row
      - object: background
        count: 1
        properties:
          - color: white (0)
          - location: fills the rest of the row
    actions:
      - name: shift_right
        target: colored_block
        parameters:
          - distance: 3 positions
    relationships:
      - type: embedding
        object1: colored_block
        object2: background
        details: The colored block is located within the background.
    constraints:
      - The color of the block remains unchanged.
      - The length of the block remains unchanged.
      - The length of the row remains unchanged.
      - There is only one colored block per input.
    ```


*   **Natural Language Program**:
    1.  Identify the single contiguous block of non-white pixels in the input row. Note its color, its starting index, and its length.
    2.  Create a new output row of the same length as the input row, initially filled entirely with white pixels (0).
    3.  Calculate the new starting index for the colored block by adding 3 to its original starting index.
    4.  Place the identified colored block (with its original color and length) into the output row starting at the calculated new index.
```python
import numpy as np
import sys
from pathlib import Path

# Add the directory containing grid_utils.py to the Python path
# (Assuming grid_utils.py is in the same directory as this script)
sys.path.append(str(Path(__file__).parent))

# Attempt to import grid_utils, handle potential ImportError
try:
    from grid_utils import find_objects_by_color # Assuming a utility function exists
except ImportError:
    # Define a basic find_objects function if grid_utils is not available
    # This is a placeholder; a more robust implementation might be needed.
    def find_objects_by_color(grid, color_predicate, connect_diagonally=False, min_size=1):
        """Finds connected objects of specified colors."""
        # Basic implementation placeholder - finds first contiguous block in a row
        objects = []
        rows, cols = grid.shape
        for r in range(rows):
            start_col = -1
            obj_color = 0
            for c in range(cols):
                pixel_color = grid[r, c]
                if color_predicate(pixel_color):
                    if start_col == -1:
                        start_col = c
                        obj_color = pixel_color
                    # Check if color changes mid-potential block (shouldn't happen based on task description)
                    elif pixel_color != obj_color:
                         # Found the end of the previous block
                        objects.append({'color': obj_color, 'points': [(r, col) for col in range(start_col, c)]})
                        start_col = c # Start new block
                        obj_color = pixel_color

                elif start_col != -1:
                    # Found the end of the block
                    objects.append({'color': obj_color, 'points': [(r, col) for col in range(start_col, c)]})
                    start_col = -1 # Reset

            # If a block extends to the end of the row
            if start_col != -1:
                 objects.append({'color': obj_color, 'points': [(r, col) for col in range(start_col, cols)]})

        # Filter by min_size (though task description implies only one object)
        objects = [obj for obj in objects if len(obj['points']) >= min_size]
        return objects


"""
Identifies the single contiguous block of non-white pixels in the input row.
Shifts this block 3 positions to the right, preserving its color and length.
The rest of the row remains white.
"""

def find_colored_block(row):
    """
    Finds the start index, end index (exclusive), and color of the first
    contiguous non-white block in a 1D numpy array (row).

    Args:
        row (np.ndarray): A 1D numpy array representing the row.

    Returns:
        tuple: (start_index, end_index, color) or None if no block is found.
    """
    start_index = -1
    color = 0
    for i, pixel in enumerate(row):
        if pixel != 0: # Found a non-white pixel
            if start_index == -1: # Start of a potential block
                start_index = i
                color = pixel
            # Ensure the block is contiguous and has the same color
            elif pixel != color:
                 # This case should not happen based on task description (single block)
                 # If it did, this means the previous block ended at i-1
                 return start_index, i, color
        elif start_index != -1: # Found white pixel after a block started
            # End of the block found
            return start_index, i, color

    # If the block extends to the very end of the row
    if start_index != -1:
        return start_index, len(row), color

    # No non-white block found
    return None


def transform(input_grid):
    """
    Shifts the single colored block in a 1xN grid 3 positions to the right.

    Args:
        input_grid (list[list[int]]): A list containing a single list (the row).

    Returns:
        list[list[int]]: The transformed grid with the block shifted.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)

    # Ensure input is effectively 1D (1 row)
    if input_array.shape[0] != 1:
        # Handle cases with more than one row if necessary,
        # but based on examples, assume 1 row.
        # For now, just process the first row if multiple exist.
        # Or raise an error: raise ValueError("Input grid must have exactly one row")
        pass # Assume processing first row is okay if this happens unexpectedly

    row = input_array[0]
    row_length = len(row)

    # Initialize output row with white (0)
    output_row = np.zeros(row_length, dtype=int)

    # Find the colored block
    block_info = find_colored_block(row)

    if block_info:
        start_index, end_index, color = block_info
        length = end_index - start_index

        # Calculate new position
        new_start_index = start_index + 3
        new_end_index = new_start_index + length

        # Ensure the new indices are within the bounds of the row
        # If the new end index exceeds the length, the slice will automatically truncate.
        actual_new_end = min(new_end_index, row_length)
        actual_length_to_copy = actual_new_end - new_start_index

        if actual_length_to_copy > 0:
             # Place the block in the new position in the output row
             # Use the original color and calculate the actual length that fits
             output_row[new_start_index:actual_new_end] = color

    # Convert the output row back to the required list of lists format
    output_grid = [output_row.tolist()]

    return output_grid
```
