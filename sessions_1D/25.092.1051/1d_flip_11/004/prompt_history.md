
## train_1

**input:**
```
0 7 6 6 6 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 7 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 8 1 1 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 8 0 0 0 0
```


## train_3

**input:**
```
7 6 6 6 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 7 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

## Perception

1.  **Grid Structure:** The input and output grids are single rows (1D arrays represented within a 2D structure). The length of the row remains constant between input and output.
2.  **Color Palette:** The grids use white (0) as a background color. Other colors observed are orange (7), magenta (6), azure (8), and blue (1).
3.  **Key Objects:** In each input, there appear to be two distinct non-white objects:
    *   A single pixel of one color (e.g., orange 7 in train_1, azure 8 in train_2, orange 7 in train_3). Let's call this the "singleton".
    *   A contiguous horizontal block of one or more pixels of another color (e.g., magenta 6 in train_1 and train_3, blue 1 in train_2). Let's call this the "block".
4.  **Relationship:** The singleton pixel is always immediately adjacent (horizontally) to the block.
5.  **Transformation:** The core transformation involves the singleton pixel changing its position relative to the block. It moves from one side of the block (e.g., left) to the immediately adjacent position on the *other* side of the block (e.g., right).
6.  **Background/Other Pixels:** The white (0) background pixels remain unchanged. The pixels forming the block also remain in their original positions. The original position of the singleton pixel becomes white (0) in the output.

## Facts


```yaml
task_type: object_manipulation
grid_properties:
  dimensionality: 1D (represented as single row)
  size_preservation: True
  background_color: 0 # white
objects:
  - name: singleton
    count: 1
    properties:
      - color: non-white (e.g., 7, 8)
      - size: 1 pixel
      - unique_color_instance: True # only one pixel of this color in the input
  - name: block
    count: 1
    properties:
      - color: non-white (e.g., 6, 1), different from singleton color
      - shape: contiguous horizontal line
      - size: 1 or more pixels
relationships:
  - type: adjacency
    subject: singleton
    object: block
    details: The singleton is immediately adjacent (left or right) to the block.
actions:
  - name: move_singleton
    target: singleton
    details:
      - The singleton pixel moves its position.
      - The original position of the singleton becomes the background color (0).
      - The new position is immediately adjacent to the block, but on the side opposite its original position.
      - The block itself does not move or change color.
invariants:
  - background_pixels: Unchanged
  - block_pixels: Position and color unchanged
  - grid_dimensions: Unchanged
```


## Natural Language Program

1.  Identify all non-white pixels in the input grid.
2.  Find the pixel whose color appears only once in the grid; this is the 'singleton'.
3.  Find the contiguous horizontal block of pixels of another single non-white color; this is the 'block'.
4.  Verify that the 'singleton' is horizontally adjacent to the 'block'.
5.  Determine if the 'singleton' is to the left or right of the 'block'.
6.  Create a copy of the input grid to serve as the basis for the output grid.
7.  In the output grid, change the color of the 'singleton's original position to white (0).
8.  If the 'singleton' was originally to the left of the 'block', place the 'singleton' pixel immediately to the right of the 'block' in the output grid.
9.  If the 'singleton' was originally to the right of the 'block', place the 'singleton' pixel immediately to the left of the 'block' in the output grid.
10. Return the modified grid as the output.
```python
import numpy as np
from collections import Counter

"""
Transformation Rule:
Identify two non-white objects in the 1D input grid: a 'singleton' (a single pixel of one color) and a 'block' (a contiguous horizontal line of one or more pixels of another color). The singleton is always adjacent to the block. Move the singleton pixel from its original position to the position immediately adjacent to the block on the opposite side. The original position of the singleton becomes white (0). The block and background pixels remain unchanged.
"""

def find_objects_1d(row):
    """Finds the singleton and block objects in a 1D row."""
    non_white_indices = [i for i, pixel in enumerate(row) if pixel != 0]
    if not non_white_indices:
        return None, None, None, None # No objects found

    non_white_colors = [row[i] for i in non_white_indices]
    color_counts = Counter(non_white_colors)

    singleton_color = None
    block_color = None
    singleton_index = -1

    for color, count in color_counts.items():
        if count == 1:
            singleton_color = color
            # Find the index of the singleton
            for i in non_white_indices:
                if row[i] == singleton_color:
                    singleton_index = i
                    break
            break # Assume only one singleton color exists

    if singleton_color is None:
        # Handle cases where maybe there isn't a singleton (though examples suggest there always is)
        return None, None, None, None

    # The other non-white color must be the block color
    block_color = next((c for c in color_counts if c != singleton_color), None)
    
    if block_color is None:
         # Handle cases where maybe there isn't a block (though examples suggest there always is)
         # Could be just a singleton
         if len(non_white_indices) == 1:
             # If only a singleton exists, maybe it doesn't move? Return original state.
             # Or maybe this case doesn't happen based on examples. 
             # For now, let's assume block always exists if singleton does based on examples.
             return None, None, None, None
         else: # Should not happen if logic above is correct
             return None, None, None, None


    block_indices = [i for i in non_white_indices if row[i] == block_color]

    # Check for contiguity (although sorting by index effectively does this for 1D)
    if not block_indices:
        return None, None, None, None # Should not happen
        
    block_indices.sort()
    # Basic contiguity check for 1D
    if len(block_indices) > 1 and not all(block_indices[j] == block_indices[0] + j for j in range(len(block_indices))):
         print(f"Warning: Block pixels for color {block_color} are not contiguous.") # Or raise error
         return None, None, None, None

    block_start_index = block_indices[0]
    block_end_index = block_indices[-1]

    return singleton_color, singleton_index, block_color, block_indices

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to be effectively 1D (1 row).

    Returns:
        list of lists: The transformed grid.
    """
    # Ensure input is treated as 1D for simplicity, take the first row
    # Add checks for multi-row inputs if necessary, but examples are 1-row
    if len(input_grid) != 1:
        # Handle error or unexpected input format if necessary
        # For now, assume it's always 1 row based on examples
        pass 
        
    input_row = np.array(input_grid[0]) # Work with the first row as a numpy array
    output_row = input_row.copy()

    # Find the singleton and block objects
    singleton_color, singleton_index, block_color, block_indices = find_objects_1d(output_row)

    # If objects aren't found as expected, return the original grid
    if singleton_color is None or not block_indices:
        print("Warning: Could not identify singleton and block as expected.")
        return input_grid # Return original if pattern doesn't match

    block_start_index = block_indices[0]
    block_end_index = block_indices[-1]

    # Determine the new position for the singleton
    new_singleton_index = -1
    is_left = False
    # Check if singleton is to the left of the block
    if singleton_index == block_start_index - 1:
        new_singleton_index = block_end_index + 1
        is_left = True
    # Check if singleton is to the right of the block
    elif singleton_index == block_end_index + 1:
        new_singleton_index = block_start_index - 1
        is_left = False
    else:
        # Singleton is not adjacent to the block, which contradicts observations. Return original.
        print("Warning: Singleton is not adjacent to the block.")
        return input_grid

    # Check if the new position is within the grid bounds
    if 0 <= new_singleton_index < len(output_row):
        # Perform the move
        # 1. Make the original singleton position white (0)
        output_row[singleton_index] = 0
        # 2. Place the singleton color at the new position
        output_row[new_singleton_index] = singleton_color
    else:
        # New position is out of bounds, shouldn't happen with these examples
        # but handle defensively - return original
         print(f"Warning: Calculated new position {new_singleton_index} is out of bounds.")
         return input_grid


    # Convert the result back to the list of lists format
    output_grid = [output_row.tolist()]

    return output_grid
```
```python
import numpy as np
from collections import Counter

"""
Transformation Rule:
Identify a 'singleton' pixel (unique non-white color) and a 'block' of contiguous pixels (another non-white color) which are adjacent to each other, forming a combined contiguous 'span'. Rotate the sequence of pixels within this span by one position. If the singleton was originally at the left end of the span, rotate right (last element becomes first). If the singleton was at the right end, rotate left (first element becomes last). Place the rotated sequence back into the same span location in the output grid. Background pixels remain unchanged.
"""

def find_span_and_singleton_pos(row):
    """
    Identifies the combined span of the singleton and block, and the singleton's position.

    Args:
        row (np.array): The 1D input row.

    Returns:
        tuple: (span_start, span_end, singleton_pos) or (None, None, None) if pattern not found.
               singleton_pos is 'left' or 'right'.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) < 2: # Need at least one singleton and one block pixel
        return None, None, None

    non_white_colors = row[non_white_indices]
    color_counts = Counter(non_white_colors)

    singleton_color = None
    block_color = None
    singleton_index = -1

    # Identify singleton and block colors
    for color, count in color_counts.items():
        if count == 1:
            if singleton_color is not None: return None, None, None # More than one singleton type
            singleton_color = color
        else: # count > 1 implies block color (assuming only 2 non-white colors)
             if block_color is not None: return None, None, None # More than one block type
             block_color = color

    if singleton_color is None or block_color is None:
        return None, None, None # Pattern needs one singleton and one block

    # Find the index of the singleton
    try:
        # Find the index within the non_white_indices array first
        s_idx_in_non_white = np.where(non_white_colors == singleton_color)[0][0]
        singleton_index = non_white_indices[s_idx_in_non_white]
    except IndexError:
        return None, None, None # Should not happen if color_counts was correct

    # Determine span boundaries (min and max of all non-white indices)
    span_start = np.min(non_white_indices)
    span_end = np.max(non_white_indices)

    # Verify combined span contiguity
    expected_len = span_end - span_start + 1
    if len(non_white_indices) != expected_len:
        # Implies gaps or non-contiguity of the combined object
        return None, None, None

    # Determine singleton position within the span
    if singleton_index == span_start:
        singleton_pos = 'left'
    elif singleton_index == span_end:
        singleton_pos = 'right'
    else:
        # Singleton is not at either end, which contradicts the observed pattern
        return None, None, None

    return span_start, span_end, singleton_pos


def transform(input_grid):
    """
    Applies the span rotation transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.
                                     Expected to be effectively 1D (1 row).

    Returns:
        list of lists: The transformed grid.
    """
    # --- Input Validation and Initialization ---
    if not isinstance(input_grid, list) or not input_grid:
        return [] # Handle empty input
    if len(input_grid) != 1:
         # This specific task seems focused on 1-row grids based on examples.
         # If multi-row grids were possible, logic would need adjustment.
         # For now, assume valid input is 1xN. Return original if not.
         print("Warning: Input grid has more than one row. Returning original.")
         return input_grid
    if not isinstance(input_grid[0], list):
         return [] # Handle malformed input

    input_row = np.array(input_grid[0])
    output_row = input_row.copy() # Create a copy to modify

    # --- Find the Span and Singleton Position ---
    span_start, span_end, singleton_pos = find_span_and_singleton_pos(output_row)

    # If the expected pattern (singleton + adjacent block) isn't found, return original
    if span_start is None:
        # print("Pattern (singleton adjacent to block) not found. Returning original.")
        return input_grid

    # --- Extract and Rotate the Span ---
    # Extract the sequence of pixels within the identified span
    span_sequence = output_row[span_start : span_end + 1]

    # Perform rotation based on the singleton's original position
    rotated_sequence = np.zeros_like(span_sequence)
    if singleton_pos == 'left':
        # Rotate right: last element moves to the first position
        rotated_sequence = np.roll(span_sequence, 1)
    elif singleton_pos == 'right':
        # Rotate left: first element moves to the last position
        rotated_sequence = np.roll(span_sequence, -1)
    else:
         # Should not happen due to checks in find_span_and_singleton_pos
         print("Error: Invalid singleton position detected.")
         return input_grid # Return original on error

    # --- Update Output Grid ---
    # Place the rotated sequence back into the output row at the original span location
    output_row[span_start : span_end + 1] = rotated_sequence

    # --- Format and Return Output ---
    # Convert the modified numpy row back to a list and wrap in a list
    output_grid = [output_row.tolist()]

    return output_grid
```
