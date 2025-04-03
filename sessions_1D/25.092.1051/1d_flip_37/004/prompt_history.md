
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 8 7 7 7 7 7 7 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 8 0 0 0
```


## train_2

**input:**
```
8 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 6 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 4 6 6 6 6 6 6 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 6 6 4 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Input Structure:** The inputs are single-row grids (1D arrays).
2.  **Content:** Each input primarily consists of white pixels (0). There is a single contiguous segment of non-white pixels within each row.
3.  **Non-White Segment:** This segment is composed of two distinct non-white colors. One color appears only once (let's call it the 'head'), and the other color appears multiple times consecutively (let's call it the 'body'). The head pixel is always located at one end of the body segment.
4.  **Transformation:** The core transformation involves repositioning the 'head' pixel. In the output, the head pixel is moved to the opposite end of the 'body' segment.
5.  **Preservation:** The colors themselves, the length of the body segment, and the surrounding white pixels remain unchanged. The overall position of the non-white segment within the row is also preserved.

## Facts


```yaml
task_type: object_manipulation
grid_dimensionality: 1D (row)
background_color: white (0)
objects:
  - name: colored_segment
    description: A single contiguous block of non-white pixels.
    properties:
      colors: Exactly two distinct non-white colors.
      structure: Consists of two parts:
        - name: head
          description: A single pixel of one color.
          location: At one end of the segment.
        - name: body
          description: Multiple contiguous pixels of the second color.
          location: Adjacent to the head.
    count_per_example: 1
actions:
  - name: move_head
    object: colored_segment
    description: The head pixel is moved from its original end of the body segment to the opposite end.
    details:
      - The sequence of body pixels remains unchanged relative to each other.
      - The head pixel retains its color.
      - The body pixels retain their color.
      - The overall start and end position of the reconstructed segment within the row remains the same as the original segment.
relationships:
  - type: adjacency
    between: head, body
    description: The head pixel is directly adjacent to the body segment in the input.
  - type: order_reversal
    target: head position relative to body
    description: The position of the head relative to the body segment is reversed (e.g., from leading to trailing, or vice-versa).
invariants:
  - Background pixels (white) remain unchanged.
  - The colors used for the head and body remain the same.
  - The number of body pixels remains the same.
  - The total length of the colored segment remains the same.
  - The position of the segment within the row (start and end indices) remains the same.
```


## Natural Language Program

1.  Identify the contiguous segment of non-white pixels in the input row.
2.  Within this segment, identify the unique 'head' pixel (the color that appears only once) and the repeated 'body' pixels (the color that appears multiple times). Note the color and count of the body pixels.
3.  Determine the position (start and end indices) of the non-white segment in the original row.
4.  Construct the output row:
    a.  Keep all white pixels outside the segment's original position unchanged.
    b.  Reconstruct the segment at its original position by placing the sequence of 'body' pixels first, followed immediately by the single 'head' pixel. Ensure the total length and position match the original segment. If the head was originally at the beginning of the segment, place it at the end in the output. If it was originally at the end, place it at the beginning in the output.
```python
import numpy as np
from collections import Counter

"""
Identifies a contiguous segment of non-white pixels in a 1D input grid.
Within this segment, it finds a unique 'head' pixel (color appears once) 
and multiple 'body' pixels (color appears more than once).
The transformation moves the 'head' pixel to the opposite end of the 'body' pixels 
within the segment's original location in the grid.
"""

def find_non_white_segment(grid_row):
    """
    Finds the start index, end index, and the subarray of the first contiguous 
    non-white segment.
    Returns (start_index, end_index, segment_array) or (None, None, None) if no 
    segment found.
    """
    non_white_indices = np.where(grid_row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None, None
    
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    
    # Check for contiguity (though problem description implies it)
    if not np.all(np.diff(non_white_indices) == 1):
         # Handle potential gaps if needed, but based on examples, assume contiguity
         # For now, we trust the segment is contiguous if non_white_indices exist
         pass 

    segment = grid_row[start_index : end_index + 1]
    return start_index, end_index, segment

def identify_head_body(segment):
    """
    Identifies the head color, body color, and the index of the head within the segment.
    Returns (head_color, body_color, head_index_in_segment) or (None, None, None) if 
    pattern not matched.
    """
    if len(segment) < 2:
        return None, None, None # Segment needs at least a head and a body pixel

    counts = Counter(segment)
    
    head_color = None
    body_color = None
    
    for color, count in counts.items():
        if count == 1:
            head_color = color
        elif count > 1:
            body_color = color
        # else: # handle unexpected counts if necessary

    if head_color is None or body_color is None:
         # Pattern doesn't match (e.g., all unique, all same, >2 colors)
        return None, None, None

    # Find the index of the head pixel
    head_index_in_segment = np.where(segment == head_color)[0][0] 

    # Validate head is at an end
    if head_index_in_segment != 0 and head_index_in_segment != len(segment) - 1:
        # Head is not at either end, pattern violation
        return None, None, None 

    return head_color, body_color, head_index_in_segment

def transform(input_grid):
    """
    Transforms the input grid by reversing the position of the 'head' pixel 
    relative to the 'body' pixels within the non-white segment.
    
    Args:
        input_grid (list or np.ndarray): A 1D list or array representing the input row.

    Returns:
        np.ndarray: The transformed 1D array.
    """
    # Convert input to numpy array for easier manipulation
    input_row = np.array(input_grid)
    
    # Initialize output grid as a copy of the input
    output_grid = input_row.copy()

    # 1. Identify the contiguous segment of non-white pixels
    start_index, end_index, segment = find_non_white_segment(input_row)

    if segment is None:
        # No segment found, return the original grid
        return output_grid

    # 2. Identify the head and body within the segment
    head_color, body_color, head_index_in_segment = identify_head_body(segment)

    if head_color is None:
        # Pattern not matched within the segment, return original
        # Or handle error appropriately
        print(f"Warning: Segment pattern (head/body) not matched in {segment}")
        return output_grid

    # 3. Determine the position and length of the segment (already have start/end indices)
    segment_len = len(segment)
    body_len = segment_len - 1

    # 4. Construct the transformed segment
    transformed_segment = np.full(segment_len, body_color) # Fill with body color

    if head_index_in_segment == 0:
        # Head was at the start, move it to the end
        transformed_segment[-1] = head_color
    else: # head_index_in_segment == segment_len - 1
        # Head was at the end, move it to the start
        transformed_segment[0] = head_color
        
    # 5. Place the transformed segment back into the output grid
    output_grid[start_index : end_index + 1] = transformed_segment

    return output_grid.tolist() # Return as list to match input format if needed, or np.array
```
```python
import numpy as np
from collections import Counter

"""
Transforms a 1D input grid by locating a single contiguous segment of non-white pixels. 
This segment must contain exactly two distinct non-white colors: one 'head' color appearing once 
at either end, and one 'body' color appearing multiple times. The transformation moves the 
'head' pixel to the opposite end of the segment, keeping the body pixels, segment length, 
and overall segment position within the grid unchanged.
"""

def find_non_white_segment(grid_row):
    """
    Finds the start index, end index, and the subarray of the first contiguous 
    non-white segment in a 1D numpy array.

    Args:
        grid_row (np.ndarray): The 1D input grid row.

    Returns:
        tuple: (start_index, end_index, segment_array) or (None, None, None) if no 
               segment found or segment is not contiguous.
    """
    non_white_indices = np.where(grid_row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None, None
    
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    
    # Check for contiguity: difference between consecutive indices should always be 1
    if len(non_white_indices) > 1 and not np.all(np.diff(non_white_indices) == 1):
         # If there are multiple non-white pixels but they aren't contiguous
         return None, None, None 

    segment = grid_row[start_index : end_index + 1]
    return start_index, end_index, segment

def analyze_segment(segment):
    """
    Analyzes a segment to identify head and body colors and the head's position.
    Checks if the segment matches the expected pattern: two colors, one unique (head) 
    at an end, one repeated (body).

    Args:
        segment (np.ndarray): The segment subarray.

    Returns:
        tuple: (head_color, body_color, head_index_in_segment) or 
               (None, None, None) if the pattern is not matched.
    """
    if segment is None or len(segment) < 2:
        return None, None, None # Segment needs at least a head and a body pixel

    counts = Counter(segment)
    
    # Check for exactly two distinct colors
    if len(counts) != 2:
        return None, None, None

    head_color = None
    body_color = None
    
    # Identify head (count 1) and body (count > 1) colors
    for color, count in counts.items():
        if count == 1:
            head_color = color
        elif count > 1:
            body_color = color
        else: # Should not happen if len(counts) == 2 and len(segment) >= 2
             return None, None, None

    # Ensure both head and body were found
    if head_color is None or body_color is None:
        return None, None, None

    # Find the index of the head pixel within the segment
    try:
        head_index_in_segment = np.where(segment == head_color)[0][0] 
    except IndexError: # Should not happen if head_color was identified
        return None, None, None

    # Validate head is at one of the ends
    if head_index_in_segment != 0 and head_index_in_segment != len(segment) - 1:
        # Head is not at either end, pattern violation
        return None, None, None 

    return head_color, body_color, head_index_in_segment

def transform(input_grid):
    """
    Applies the head-reversal transformation to the input grid.

    Args:
        input_grid (list): A 1D list representing the input row.

    Returns:
        list: The transformed 1D list, or the original list if the
              pattern wasn't found or matched.
    """
    # Convert input to numpy array for easier manipulation
    input_row = np.array(input_grid)
    
    # Initialize output grid as a copy of the input
    output_grid = input_row.copy()

    # 1. Identify the contiguous segment of non-white pixels
    start_index, end_index, segment = find_non_white_segment(input_row)

    # If no valid segment found, return the original grid
    if segment is None:
        return output_grid.tolist()

    # 2. Analyze the segment for the head/body pattern
    analysis_result = analyze_segment(segment)

    # If pattern not matched within the segment, return original
    if analysis_result is None:
        return output_grid.tolist()
        
    head_color, body_color, head_index_in_segment = analysis_result

    # 3. Get segment length
    segment_len = len(segment)

    # 4. Construct the transformed segment
    # Create a new array filled with the body color
    transformed_segment = np.full(segment_len, body_color, dtype=segment.dtype) 

    # Determine the new position for the head and place it
    if head_index_in_segment == 0:
        # Head was at the start, move it to the end
        transformed_segment[-1] = head_color
    else: # head_index_in_segment == segment_len - 1
        # Head was at the end, move it to the start
        transformed_segment[0] = head_color
        
    # 5. Place the transformed segment back into the output grid
    output_grid[start_index : end_index + 1] = transformed_segment

    # Return the result as a list
    return output_grid.tolist() 
```
