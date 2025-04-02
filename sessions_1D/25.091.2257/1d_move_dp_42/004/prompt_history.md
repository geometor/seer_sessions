
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 6
```


**output:**
```
0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 6
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0 0 0 0 0 6
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 6
```


## train_3

**input:**
```
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 6 0 0
```

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Data Structure:** The input and output data appear to be one-dimensional arrays or lists of integers, representing pixel colors.
2.  **Key Colors:**
    *   White (0) seems to function as a background or empty space.
    *   Magenta (6) appears in every example and seems to be a fixed marker or anchor point. Its position relative to the end of the array seems consistent within each example pair (though its absolute index might differ if the array length changes).
    *   Other colors (Red=2, Orange=7, Blue=1) form contiguous blocks.
3.  **Core Transformation:** The central action is the movement of a contiguous block of non-white, non-magenta pixels. This block shifts rightwards.
4.  **Shift Target:** The block moves until its rightmost pixel is immediately adjacent to the left side of the magenta (6) pixel.
5.  **Space Filling:** The space between the original position of the colored block and the magenta pixel, which initially contained white pixels (0), appears to be swapped with the colored block. Essentially, the colored block moves right, displacing the white pixels to its left.
6.  **Boundary Pixels:** Pixels to the left of the colored block's original position and pixels to the right of the magenta pixel (if any) seem to remain unchanged in their positions.

**YAML Facts:**


```yaml
task_description: "Shift a contiguous block of non-background pixels rightwards until it touches a specific marker pixel."
elements:
  - type: array
    description: "A 1D array of pixel colors."
  - type: pixel
    color: white (0)
    role: background/empty_space
  - type: pixel
    color: magenta (6)
    role: marker/anchor
    properties:
      - "Appears once in each array."
      - "Acts as the target boundary for the shift operation."
      - "Its position relative to surrounding non-moving elements remains fixed."
  - type: object
    description: "A contiguous block of pixels with colors other than white (0) and magenta (6)."
    identifier: "payload_block"
    properties:
      - "Can be of various colors (red, orange, blue observed)."
      - "Can be of various lengths."
      - "Is the primary element being moved."
  - type: object
    description: "A contiguous block of white (0) pixels located between the payload_block and the magenta marker."
    identifier: "gap_block"
    properties:
      - "Its length determines the shift distance of the payload_block."
      - "It is moved to the original starting position of the payload_block."
actions:
  - action: identify
    target: magenta (6) pixel
    result: marker_index
  - action: identify
    target: payload_block
    result: payload_block_pixels, payload_start_index, payload_end_index
  - action: identify
    target: gap_block (white pixels between payload_end_index and marker_index)
    result: gap_block_pixels
  - action: rearrange
    description: "Construct the output array by reordering segments of the input array."
    steps:
      - "Take pixels from start of input up to payload_start_index."
      - "Append gap_block_pixels."
      - "Append payload_block_pixels."
      - "Append the magenta (6) pixel."
      - "Append pixels from input that were originally after the magenta pixel."
relationships:
  - type: spatial
    description: "The payload_block is initially separated from the magenta marker by the gap_block."
  - type: spatial
    description: "In the output, the payload_block is immediately adjacent to the left of the magenta marker."
  - type: positional_swap
    description: "The payload_block and the gap_block effectively swap their positions relative to the start of the array and the marker pixel."

```


**Natural Language Program:**

1.  Receive the input array of pixels.
2.  Locate the single magenta pixel (color 6) and note its index (`marker_index`).
3.  Scan the array from the beginning up to `marker_index` to find the contiguous sequence of pixels that are *not* white (color 0). This is the "payload block". Record the pixels in this block (`payload_pixels`), its starting index (`payload_start`), and its ending index (`payload_end`).
4.  Identify the sequence of white pixels (color 0) that exists in the input array between `payload_end + 1` and `marker_index - 1`. This is the "gap block". Record the pixels in this block (`gap_pixels`).
5.  Create a new output array.
6.  Copy the pixels from the input array from index 0 up to (but not including) `payload_start` into the output array.
7.  Append the `gap_pixels` to the output array.
8.  Append the `payload_pixels` to the output array.
9.  Append the magenta pixel (color 6) to the output array.
10. Copy any remaining pixels from the input array (from index `marker_index + 1` to the end) and append them to the output array.
11. Return the completed output array.
```python
import numpy as np
from typing import List, Tuple

"""
Shift a contiguous block of non-background (non-zero) pixels rightwards until 
its right edge is immediately adjacent to the left side of a specific marker 
pixel (magenta, color 6). The white (zero) pixels originally between the 
block and the marker are moved to occupy the original starting position of the block.
"""

def find_marker(input_array: np.ndarray, marker_color: int = 6) -> int:
    """Finds the index of the marker pixel."""
    marker_indices = np.where(input_array == marker_color)[0]
    if len(marker_indices) == 0:
        raise ValueError(f"Marker color {marker_color} not found in input array.")
    # Assuming only one marker as per examples
    return marker_indices[0]

def find_payload_block(input_array: np.ndarray, marker_index: int) -> Tuple[int, int, np.ndarray]:
    """
    Finds the contiguous block of non-zero, non-marker pixels before the marker.
    Returns the start index, end index (inclusive), and the block pixels.
    """
    in_block = False
    start_index = -1
    end_index = -1
    payload_pixels = []

    for i in range(marker_index):
        pixel = input_array[i]
        # Start of block found
        if not in_block and pixel != 0:
            in_block = True
            start_index = i
            payload_pixels.append(pixel)
        # Continue block
        elif in_block and pixel != 0:
            payload_pixels.append(pixel)
        # End of block (hit a zero after being in a block)
        elif in_block and pixel == 0:
            end_index = i - 1
            break # Stop searching once the first block is found and ended
        # If we reach the marker while in a block, the block ends just before it
        if in_block and i == marker_index - 1:
             end_index = i


    # Handle case where block runs right up to marker or starts at index 0
    if in_block and end_index == -1:
         end_index = marker_index - 1
         
    if start_index == -1:
         # No payload found before marker
         return -1, -1, np.array([])


    return start_index, end_index, np.array(payload_pixels)


def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input list by shifting a colored block next to the marker.

    Args:
        input_grid: A list of integers representing pixel colors.

    Returns:
        A list of integers representing the transformed pixel colors.
    """
    # Convert input list to numpy array for easier processing
    input_array = np.array(input_grid)
    
    # 1. Locate the magenta marker (6)
    try:
        marker_index = find_marker(input_array, 6)
    except ValueError as e:
        print(f"Error: {e}")
        # Return input unchanged if marker not found (or handle as appropriate)
        return input_grid 

    # 2. Find the payload block (non-zero pixels before the marker)
    payload_start, payload_end, payload_pixels = find_payload_block(input_array, marker_index)

    # Handle case where no payload block is found
    if payload_start == -1:
        # No block to move, return original array
        return input_grid

    # 3. Identify the prefix (pixels before the payload)
    prefix_pixels = input_array[:payload_start]

    # 4. Identify the gap (zero pixels between payload and marker)
    gap_pixels = input_array[payload_end + 1 : marker_index]

    # 5. Identify the suffix (pixels after the marker)
    suffix_pixels = input_array[marker_index + 1:]
    
    # 6. Get the marker pixel itself
    marker_pixel = np.array([input_array[marker_index]])

    # 7. Construct the output array by rearranging parts
    # Order: prefix, gap, payload, marker, suffix
    output_array = np.concatenate((prefix_pixels, gap_pixels, payload_pixels, marker_pixel, suffix_pixels))

    # Convert back to list for the return type
    return output_array.tolist()

```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Shift the first contiguous block of non-background (non-zero) pixels found before a magenta marker (color 6) rightwards, placing it immediately before the marker. The background pixels (color 0) originally located between this block and the marker are moved to fill the space vacated by the block at its original starting position. Pixels before the block's original start and after the marker remain in their relative positions.
"""

def find_marker(input_array: np.ndarray, marker_color: int = 6) -> Optional[int]:
    """
    Finds the index of the first occurrence of the marker pixel.

    Args:
        input_array: The numpy array to search within.
        marker_color: The integer value of the marker pixel.

    Returns:
        The index of the marker pixel, or None if not found.
    """
    marker_indices = np.where(input_array == marker_color)[0]
    if len(marker_indices) == 0:
        return None
    return marker_indices[0] # Return the first occurrence

def find_first_payload_block(input_array: np.ndarray, end_scan_index: int) -> Tuple[Optional[int], Optional[int], Optional[np.ndarray]]:
    """
    Finds the first contiguous block of non-zero pixels before a given index.

    Args:
        input_array: The numpy array to search within.
        end_scan_index: The index before which to search (exclusive).

    Returns:
        A tuple containing:
        - start_index (int): The starting index of the block, or None if not found.
        - end_index (int): The ending index (inclusive) of the block, or None if not found.
        - payload_pixels (np.ndarray): The pixels of the block, or None if not found.
    """
    start_index = None
    end_index = None
    payload_pixels = []
    in_block = False

    for i in range(end_scan_index):
        pixel = input_array[i]
        # Start of a new block
        if not in_block and pixel != 0:
            in_block = True
            start_index = i
            payload_pixels.append(pixel)
        # Continue the current block
        elif in_block and pixel != 0:
            payload_pixels.append(pixel)
        # End of the current block (hit a zero or end scan)
        elif in_block and pixel == 0:
            end_index = i - 1
            break # Found the first block, stop searching

    # If still in block when loop finishes, the block ends right before end_scan_index
    if in_block and end_index is None:
        end_index = end_scan_index - 1

    if start_index is None:
        return None, None, None
    else:
        return start_index, end_index, np.array(payload_pixels)


def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input list based on the defined rule.

    Args:
        input_grid: A list of integers representing pixel colors.

    Returns:
        A list of integers representing the transformed pixel colors.
    """
    # Convert input list to numpy array for easier processing
    input_array = np.array(input_grid)
    
    # 1. Locate the magenta marker (6)
    marker_index = find_marker(input_array, 6)
    
    # If marker not found, return original grid
    if marker_index is None:
        # Consider raising an error or logging, but for ARC, returning original might be safer
        return input_grid 

    # 2. Find the first payload block (non-zero pixels before the marker)
    payload_start, payload_end, payload_pixels = find_first_payload_block(input_array, marker_index)

    # Handle case where no payload block is found before the marker
    if payload_start is None:
        # No block to move, return original array
        return input_grid

    # 3. Identify the prefix (pixels before the payload)
    prefix_pixels = input_array[:payload_start]

    # 4. Identify the gap (pixels between payload end and marker)
    # These should be background pixels (0) based on the task description
    gap_pixels = input_array[payload_end + 1 : marker_index]

    # 5. Identify the suffix (pixels after the marker)
    suffix_pixels = input_array[marker_index + 1:]
    
    # 6. Get the marker pixel itself
    marker_pixel = np.array([input_array[marker_index]])

    # 7. Construct the output array by rearranging parts
    # Order: prefix, gap, payload, marker, suffix
    output_array = np.concatenate((prefix_pixels, gap_pixels, payload_pixels, marker_pixel, suffix_pixels))

    # Convert back to list for the return type
    return output_array.tolist()
```
