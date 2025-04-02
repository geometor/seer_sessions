
## train_1

**input:**
```
0 2 2 2 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 6 6 6 0 0 0 0 6 0 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 0 0 6 6 6 0 6 6 6 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 4 4 4 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the transformation logic for this task.

**Perception of Elements:**

1.  **Grid Structure:** The examples use 1-dimensional grids (rows). The input and output grids have the same dimensions.
2.  **Color Palette:** Each example uses white (0) and one other color (red=2, magenta=6, yellow=4).
3.  **Key Features:**
    *   **Pattern Segment:** In each input, there is a contiguous horizontal segment of 3 identical non-white pixels (e.g., `2 2 2`, `6 6 6`, `4 4 4`). This seems to be the defining pattern. It's always the first non-white group encountered.
    *   **Target Pixels:** Elsewhere in the input row, there are isolated single pixels of the *same* non-white color as the pattern segment. These single pixels are surrounded horizontally by white (0) pixels.
4.  **Transformation:** The core transformation involves replacing the isolated single target pixels. The original pattern segment remains untouched. The white pixels also remain untouched unless they are overwritten during the replacement.
5.  **Replacement Mechanism:** Each target pixel is replaced by a *copy* of the pattern segment. The replacement seems to be centered horizontally on the position of the original target pixel. Since the pattern segment has length 3, the replacement overwrites the target pixel and its immediate left and right neighbors.

**YAML Facts:**


```yaml
task_description: Replace isolated pixels of a specific color with the first encountered contiguous segment of that same color, centering the segment on the isolated pixel's position.

elements:
  - element_type: grid
    properties:
      - description: Input and output are 1D grids (rows) of the same size.
      - background_color: white (0)

  - element_type: object
    description: Pattern Segment
    properties:
      - identification: The first contiguous horizontal sequence of non-white pixels.
      - color: Varies per example (red, magenta, yellow).
      - shape: Always a 1x3 segment in the examples (e.g., [color, color, color]).
      - role: Defines the pattern to be replicated.
      - persistence: Remains unchanged in the output.

  - element_type: object
    description: Target Pixel
    properties:
      - identification: A single non-white pixel whose horizontal neighbors are white (0) or grid boundaries.
      - color: Must match the color of the Pattern Segment.
      - location: Varies within the grid.
      - role: Marks the locations for replacement.

actions:
  - action_type: find
    description: Locate the Pattern Segment (first non-white contiguous horizontal block) and its color.
    inputs:
      - input grid
    outputs:
      - pattern_segment (pixel sequence)
      - pattern_color
      - pattern_length

  - action_type: find
    description: Locate all Target Pixels (isolated pixels matching pattern_color).
    inputs:
      - input grid
      - pattern_color
    outputs:
      - list_of_target_locations (indices)

  - action_type: replace
    description: Replace pixels in the output grid based on target locations.
    details: For each target_location (column index 'c'), place the pattern_segment onto the grid such that it is centered horizontally at 'c'. The placement starts at column 'c - floor(pattern_length / 2)'.
    inputs:
      - target_locations
      - pattern_segment
      - pattern_length
      - input grid (or a copy)
    outputs:
      - output grid

relationships:
  - type: color_match
    description: Target Pixels must have the same color as the Pattern Segment.
  - type: spatial
    description: Target Pixels are isolated horizontally (neighbors are white or boundary).
  - type: transformation
    description: Target Pixels are replaced by the Pattern Segment, centered at the target location.

invariants:
  - The original Pattern Segment's location and pixels remain unchanged.
  - White (0) pixels remain unchanged unless overwritten by a replacement action.
  - Pixels that are neither part of the original Pattern Segment nor part of a replacement area remain unchanged.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid row from left to right to find the first sequence of one or more connected non-white pixels. Store this sequence as the `pattern_segment` and note its color (`pattern_color`) and length (`pattern_length`).
3.  Iterate through each column index `c` of the input grid row.
4.  Check if the pixel at index `c` in the input grid matches the `pattern_color` AND if it is isolated horizontally (i.e., the pixel at `c-1` is white or off-grid, AND the pixel at `c+1` is white or off-grid).
5.  If both conditions in step 4 are true, this pixel is a `target_pixel`. Calculate the starting column index for the replacement: `start_col = c - floor(pattern_length / 2)`.
6.  Place the `pattern_segment` onto the *output* grid, starting at `start_col` and extending for `pattern_length` columns, overwriting any existing values in the output grid at those positions. Ensure the placement stays within the grid's column boundaries.
7.  After checking all columns, return the final output grid.
```python
import numpy as np
import math

"""
Transformation Rule:

1.  Identify the first contiguous horizontal segment of non-white (non-zero) pixels in the input grid row. This is the 'pattern segment'. Note its color, length, and start/end indices.
2.  Initialize the output grid as a copy of the input grid.
3.  Iterate through each pixel in the input grid row.
4.  If a pixel has the same color as the pattern segment AND it is horizontally isolated (its left and right neighbors are white (0) or grid boundaries) AND it is *not* part of the original pattern segment identified in step 1, then it is a 'target pixel'.
5.  For each target pixel found at column index 'c', replace the corresponding segment in the *output* grid with the 'pattern segment'. The replacement should be centered horizontally at index 'c'. This means the pattern segment will overwrite the pixels in the output grid starting from column `c - floor(pattern_length / 2)` for `pattern_length` columns. Handle boundary conditions where the pattern might extend beyond the grid edges.
6.  Return the modified output grid.
"""

def find_first_pattern(grid_row):
    """
    Finds the first contiguous sequence of non-zero pixels in a 1D array.

    Args:
        grid_row (np.array): A 1D numpy array representing the grid row.

    Returns:
        tuple: (pattern_segment, pattern_color, pattern_length, start_index, end_index)
               Returns (None, -1, 0, -1, -1) if no pattern is found.
    """
    pattern_segment = None
    pattern_color = -1
    pattern_length = 0
    start_index = -1
    end_index = -1
    width = len(grid_row)

    in_pattern = False
    for j in range(width):
        pixel = grid_row[j]
        if not in_pattern and pixel != 0:
            # Start of a new pattern
            in_pattern = True
            start_index = j
            pattern_color = pixel
        elif in_pattern:
            if pixel != pattern_color:
                # End of the pattern
                end_index = j # exclusive index
                pattern_segment = grid_row[start_index:end_index]
                pattern_length = len(pattern_segment)
                return pattern_segment, pattern_color, pattern_length, start_index, end_index
            elif j == width - 1:
                 # Pattern ends at the edge of the grid
                 end_index = width # exclusive index
                 pattern_segment = grid_row[start_index:end_index]
                 pattern_length = len(pattern_segment)
                 return pattern_segment, pattern_color, pattern_length, start_index, end_index


    # If the loop finishes and we were in a pattern (single pixel pattern at end)
    # This case is actually covered by the elif j == width - 1 case above
    # If no non-zero pixel was found at all
    if not in_pattern:
        return None, -1, 0, -1, -1

    # This return should ideally not be reached due to logic inside loop,
    # but included for completeness if edge cases missed.
    # This handles case where pattern is the very last pixel and loop finishes
    if in_pattern and end_index == -1: # Should be caught by j == width - 1 check
        end_index = width
        pattern_segment = grid_row[start_index:end_index]
        pattern_length = len(pattern_segment)
        return pattern_segment, pattern_color, pattern_length, start_index, end_index

    return None, -1, 0, -1, -1 # Default if no pattern

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the grid.
                                     Expected to be 1xN for this specific task.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    # Assuming input is always 1xN based on examples
    if not input_grid or not input_grid[0]:
        return []
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # --- This task specifically works on a single row ---
    if height != 1:
        # Handle unexpected input dimensions if necessary,
        # but for now, assume height is 1 based on examples.
        # For generality, could loop through rows, but problem seems 1D.
         pass # Or raise error, or adapt logic for 2D

    grid_row = input_np[0]
    output_row = output_np[0]

    # 1. Find the first pattern segment
    pattern_segment, pattern_color, pattern_length, pattern_start_idx, pattern_end_idx = find_first_pattern(grid_row)

    # If no pattern found, return the original grid
    if pattern_segment is None:
        return output_np.tolist()

    # 2. Iterate through pixels to find isolated target pixels
    for c in range(width):
        # 3. Skip if the current pixel is part of the original pattern
        if pattern_start_idx <= c < pattern_end_idx:
            continue

        # 4. Check if the pixel matches pattern color and is isolated
        if grid_row[c] == pattern_color:
            is_left_isolated = (c == 0) or (grid_row[c - 1] == 0)
            is_right_isolated = (c == width - 1) or (grid_row[c + 1] == 0)

            if is_left_isolated and is_right_isolated:
                # This is a target pixel
                # 5. Calculate replacement indices, centered at 'c'
                center_offset = pattern_length // 2 # floor division for centering
                replace_start = c - center_offset
                replace_end = replace_start + pattern_length

                # Perform the replacement on the output_row, handling boundaries
                for i in range(pattern_length):
                    write_col = replace_start + i
                    # Ensure the write index is within the grid bounds
                    if 0 <= write_col < width:
                        output_row[write_col] = pattern_segment[i]

    # Return the modified grid as a list of lists
    return output_np.tolist()
```
