
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 1 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 1 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 6 6 6 6 6 6 6 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 4 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception of Task Elements:**

1.  **Grid Structure:** All examples involve 1xN grids (single rows).
2.  **Colors:** The grids primarily consist of the background color white (0).
3.  **Objects:** Within each row, there's a distinct pattern: a single pixel of one color (e.g., red in train_1, blue in train_2, yellow in train_3) immediately followed by a contiguous sequence of pixels of another, consistent color (e.g., orange in train_1 and train_2, magenta in train_3).
4.  **Transformation:** The core transformation appears to be a positional swap or movement. The single, unique-colored pixel (let's call it the 'marker') moves from the left end of the colored sequence to the right end. The sequence itself seems to shift one position to the left to accommodate this move. The background pixels remain unchanged.

**YAML Fact Documentation:**


```yaml
task_description: "Move a single 'marker' pixel from the left side of an adjacent horizontal sequence of identical pixels to its right side."
grid_properties:
  dimensionality: 1D (represented as 1xN grid)
  background_color: 0 (white)
objects:
  - id: marker_pixel
    description: "A single pixel with a unique color, different from the background and the sequence color."
    properties:
      color: variable (e.g., red, blue, yellow)
      shape: single pixel
      position: Immediately to the left of the sequence_object.
  - id: sequence_object
    description: "A contiguous horizontal sequence of pixels of the same color."
    properties:
      color: variable (e.g., orange, magenta), consistent within the sequence, different from background and marker.
      shape: horizontal line segment (1xM)
      position: Immediately to the right of the marker_pixel.
relationships:
  - type: adjacency
    object1: marker_pixel
    object2: sequence_object
    details: The marker_pixel is immediately adjacent to the left end of the sequence_object.
actions:
  - action: relocate
    object: marker_pixel
    details: The marker_pixel is moved from its initial position to the position immediately following the right end of the sequence_object's original span.
  - action: shift
    object: sequence_object
    details: The sequence_object effectively shifts one position to the left, occupying the original position of the marker_pixel.
invariants:
  - background_color remains unchanged.
  - color and length of the sequence_object remain unchanged.
  - color of the marker_pixel remains unchanged.
  - pixels outside the combined marker+sequence area remain unchanged.
```


**Natural Language Program:**

1.  Identify the background color (white, 0).
2.  Scan the input row to find the first non-background pixel. This is the 'marker' pixel. Store its color and its index (position).
3.  Starting from the position immediately after the 'marker' pixel, identify the contiguous sequence of identical, non-background pixels. This is the 'sequence'. Store its color, its length, and the index of its last pixel.
4.  Create a copy of the input grid to serve as the output grid.
5.  In the output grid, place the color of the *first pixel of the sequence* at the original index of the 'marker' pixel.
6.  Shift the rest of the sequence one position to the left: for each pixel in the sequence (starting from the second one), place its color at the index one position to its left.
7.  Place the stored color of the 'marker' pixel at the index immediately following the original last index of the sequence.
8.  Return the modified output grid.
```python
import copy
import numpy as np # Using numpy for easier array handling, though lists work too

"""
Move a single 'marker' pixel from the left side of an adjacent horizontal sequence of identical pixels to its right side.

1. Identify the background color (white, 0).
2. Scan the input row to find the first non-background pixel. This is the 'marker' pixel. Store its color and its index.
3. Starting from the position immediately after the 'marker' pixel, identify the contiguous sequence of identical, non-background pixels. This is the 'sequence'. Store its color and the index of its last pixel.
4. Create a copy of the input grid to serve as the output grid.
5. In the output grid:
    a. Place the color of the sequence at the original index of the 'marker' pixel.
    b. Ensure the pixels corresponding to the original sequence (excluding the last one) retain the sequence color.
    c. Place the stored color of the 'marker' pixel at the index corresponding to the original last index of the sequence.
6. Return the modified output grid.
"""

def find_pattern_segment(row):
    """
    Finds the marker pixel and the adjacent sequence of identical pixels.

    Args:
        row (list): A list of integers representing a row of the grid.

    Returns:
        dict: A dictionary containing information about the marker and sequence,
              or None if the pattern is not found.
              Keys: 'marker_idx', 'marker_color', 'seq_start_idx', 'seq_end_idx', 'seq_color'
    """
    marker_idx = -1
    marker_color = -1
    seq_start_idx = -1
    seq_end_idx = -1
    seq_color = -1

    # Find the first non-background pixel (marker)
    for i, pixel in enumerate(row):
        if pixel != 0:
            marker_idx = i
            marker_color = pixel
            break

    # If no marker is found, return None
    if marker_idx == -1:
        # print("Debug: No marker found.")
        return None

    # Check if there's a pixel immediately following the marker and it's non-background
    if marker_idx + 1 >= len(row) or row[marker_idx + 1] == 0:
        # According to examples, a sequence always follows the marker.
        # print(f"Debug: No sequence found immediately after marker at index {marker_idx}.")
        return None # Pattern requires a sequence

    # Identify the sequence starting right after the marker
    seq_start_idx = marker_idx + 1
    seq_color = row[seq_start_idx]
    
    # The sequence must have a different color than the marker based on examples
    # if seq_color == marker_color:
    #     print(f"Debug: Sequence color same as marker color at index {seq_start_idx}.")
    #     return None # Pattern requires different colors for marker and sequence

    seq_end_idx = seq_start_idx # Initialize end index to the start of the sequence

    # Find the end of the contiguous sequence of seq_color
    for i in range(seq_start_idx + 1, len(row)):
        if row[i] == seq_color:
            seq_end_idx = i
        else:
            break # End of sequence found

    return {
        "marker_idx": marker_idx,
        "marker_color": marker_color,
        "seq_start_idx": seq_start_idx,
        "seq_end_idx": seq_end_idx,
        "seq_color": seq_color
    }


def transform(input_grid):
    """
    Transforms the input grid by moving the marker pixel to the end of its adjacent sequence.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid. 
                                       Expected to be 1xN based on examples.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Ensure input is not empty and is a list of lists
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        # Handle invalid input if necessary, returning input or raising error
        return input_grid 

    # Work with a copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)
    
    # Task examples show 1xN grids, operate on the first row
    if len(output_grid) == 1:
        row = output_grid[0]
        
        # Find the marker and sequence pattern
        segment_info = find_pattern_segment(row)

        # If the specific pattern is found, apply the transformation
        if segment_info:
            # Extract information
            marker_idx = segment_info["marker_idx"]
            marker_color = segment_info["marker_color"]
            # seq_start_idx = segment_info["seq_start_idx"] # Not directly needed for modification
            seq_end_idx = segment_info["seq_end_idx"]
            seq_color = segment_info["seq_color"]

            # Perform the swap:
            # 1. Put sequence color where the marker was
            row[marker_idx] = seq_color
            
            # 2. Put marker color where the sequence ended
            #    The sequence pixels in between remain the sequence color (already handled by deepcopy)
            row[seq_end_idx] = marker_color
            
            # No explicit shift needed, just swapping the end colors of the segment.
            # Ensure intermediate sequence pixels are correct (covered by copy and step 1)
            # for i in range(segment_info["seq_start_idx"], seq_end_idx):
            #    row[i] = seq_color # This should already be true from the copy

    # Return the modified grid
    return output_grid

```
```python
import copy

"""
Swap the first and last pixels of a contiguous horizontal segment composed of a 
single 'marker' pixel followed by a sequence of identical pixels of a different color.

1.  Accept the input grid (expected 1xN).
2.  Create a deep copy for the output grid.
3.  Access the row.
4.  Find the index (`marker_idx`) and color (`marker_color`) of the first non-background pixel.
5.  If no marker found, return copy.
6.  Check the pixel immediately following the marker. If invalid (out of bounds, background, or same color as marker), return copy.
7.  Identify the sequence color (`sequence_color`) and find the end index (`sequence_end_idx`) of the contiguous sequence starting after the marker.
8.  If a valid sequence is found, swap the colors:
    a.  Place `sequence_color` at `marker_idx` in the output row.
    b.  Place `marker_color` at `sequence_end_idx` in the output row.
9.  Return the modified output grid.
"""

def find_pattern_indices(row):
    """
    Finds the indices of the marker pixel and the end of its adjacent sequence.

    Args:
        row (list): A list of integers representing a row of the grid.

    Returns:
        tuple: A tuple containing (marker_idx, sequence_end_idx), 
               or (None, None) if the pattern is not found.
    """
    marker_idx = -1
    marker_color = -1
    sequence_end_idx = -1
    
    # 1. Find the marker pixel (first non-zero)
    for i, pixel in enumerate(row):
        if pixel != 0:
            marker_idx = i
            marker_color = pixel
            break
            
    # If no marker found, pattern doesn't exist
    if marker_idx == -1:
        return None, None
        
    # 2. Check the pixel immediately following the marker
    seq_start_idx = marker_idx + 1
    if seq_start_idx >= len(row): # Check bounds
        return None, None
        
    sequence_color = row[seq_start_idx]
    
    # Check if the next pixel is background or same color as marker
    if sequence_color == 0 or sequence_color == marker_color:
        return None, None
        
    # 3. Find the end of the contiguous sequence
    sequence_end_idx = seq_start_idx # Initialize end index to the start of the sequence
    for i in range(seq_start_idx + 1, len(row)):
        if row[i] == sequence_color:
            sequence_end_idx = i
        else:
            # End of sequence (or end of row)
            break 
            
    # Pattern requires at least one sequence pixel, which is guaranteed by checks above
    return marker_idx, sequence_end_idx


def transform(input_grid):
    """
    Transforms the input grid by swapping the marker pixel color with the color 
    of the last pixel in its adjacent sequence.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid. 
                                       Expected to be 1xN based on examples.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Basic input validation
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        return input_grid # Return input as is if format is unexpected

    # Create a deep copy to modify
    output_grid = copy.deepcopy(input_grid)

    # Check if it's a single-row grid as expected from examples
    if len(output_grid) == 1:
        row = output_grid[0]
        
        # Find the indices defining the pattern
        marker_idx, sequence_end_idx = find_pattern_indices(row)
        
        # If the pattern was found, perform the swap
        if marker_idx is not None and sequence_end_idx is not None:
            # Store original colors before modifying the row
            marker_color = row[marker_idx]
            # Sequence color is the color of the pixel *after* the marker
            sequence_color = row[marker_idx + 1] 
            
            # Perform the swap in the output grid's row
            row[marker_idx] = sequence_color
            row[sequence_end_idx] = marker_color
            
    # Return the modified grid (or the original copy if no transformation occurred)
    return output_grid
```
