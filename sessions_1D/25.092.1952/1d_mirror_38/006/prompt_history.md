
## train_1

**input:**
```
0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 4 4 4 4 4 4 4 0 0 0
```


## train_2

**input:**
```
0 5 5 5 5 5 5 5 5 5 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 9 0 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 1 1 1 1 1 1 1 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0
```

**Perception**

1.  **Input/Output Format:** The input and output are single rows (1xN grids) of pixels.
2.  **Key Elements:** Each grid contains:
    *   Background pixels (white, 0).
    *   A single unique 'pivot' pixel (maroon, 9).
    *   A single contiguous block of identical colored pixels (yellow, gray, or blue in the examples), which are neither white nor maroon.
3.  **Transformation:** The core transformation involves moving the contiguous colored block. In the input, this block always appears *before* the maroon pixel. In the output, this block is moved to the position immediately *after* the maroon pixel.
4.  **Structure Preservation:** The relative order of all other pixels (white background pixels and the maroon pivot pixel) is preserved. The dimensions of the grid remain unchanged.

**Facts**


```yaml
task_type: rearrangement
grid_dimensionality: 1D (represented as 1xN)
objects:
  - id: background
    color: white (0)
    role: fills empty space
  - id: pivot
    color: maroon (9)
    count: 1
    role: defines the target location for rearrangement
  - id: colored_block
    color: any color except white (0) or maroon (9)
    count: 1
    properties:
      - contiguous sequence of identical pixels
    role: the object being moved
relationship:
  - type: spatial order (input)
    description: The 'colored_block' appears somewhere before the 'pivot' pixel in the linear sequence.
  - type: spatial order (output)
    description: The 'colored_block' appears immediately after the 'pivot' pixel in the linear sequence.
action:
  - type: move
    target: colored_block
    details: The block is extracted from its original position and reinserted immediately after the pivot pixel. All other pixels maintain their relative order.
constraints:
  - Exactly one pivot pixel exists.
  - Exactly one contiguous block of a single color (not white or maroon) exists.
  - The colored block initially precedes the pivot pixel.
```


**Natural Language Program**

1.  Identify the index (position) of the single maroon (9) pixel in the input row.
2.  Identify the contiguous block of pixels that are neither white (0) nor maroon (9). Record the sequence of pixels forming this block and their start and end indices in the input row.
3.  Create a new sequence (list) of pixels by removing the identified colored block from the input row.
4.  Find the index of the maroon (9) pixel within this new, shorter sequence.
5.  Insert the recorded colored block sequence immediately after the maroon pixel's position in the new sequence.
6.  The resulting sequence is the final output row.
```python
import numpy as np
from typing import List, Tuple

"""
1. Identify the index (position) of the single maroon (9) pixel in the input row.
2. Identify the contiguous block of pixels that are neither white (0) nor maroon (9). Record the sequence of pixels forming this block and their start and end indices in the input row.
3. Create a new sequence (list) of pixels by removing the identified colored block from the input row.
4. Find the index of the maroon (9) pixel within this new, shorter sequence.
5. Insert the recorded colored block sequence immediately after the maroon pixel's position in the new sequence.
6. The resulting sequence is the final output row.
"""

def find_pivot_index(row: List[int], pivot_color: int = 9) -> int:
    """Finds the index of the pivot color in the row."""
    for i, pixel in enumerate(row):
        if pixel == pivot_color:
            return i
    raise ValueError(f"Pivot color {pivot_color} not found in the row.")

def find_colored_block(row: List[int], background_color: int = 0, pivot_color: int = 9) -> Tuple[List[int], int, int]:
    """Finds the contiguous block of non-background, non-pivot color."""
    block = []
    start_index = -1
    end_index = -1
    in_block = False

    for i, pixel in enumerate(row):
        if pixel != background_color and pixel != pivot_color:
            if not in_block:
                start_index = i
                in_block = True
            block.append(pixel)
            end_index = i # Keep updating end index while in block
        elif in_block:
            # Found the end of the block
            break # Assume only one block exists as per priors

    if not block:
        raise ValueError("Colored block not found in the row.")

    return block, start_index, end_index


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by moving a colored block to the position
    immediately after a pivot pixel (maroon, 9).
    """
    # Ensure input is a 1xN grid
    if len(input_grid) != 1:
        raise ValueError("Input grid must have exactly one row.")

    input_row = input_grid[0]

    # 1. Identify the index of the single maroon (9) pixel (handled later in step 4)
    # We need to find it in the modified list later.

    # 2. Identify the contiguous block of pixels (not white 0 or maroon 9)
    colored_block, block_start_index, block_end_index = find_colored_block(input_row)

    # 3. Create a new sequence by removing the identified colored block
    temp_row = []
    for i, pixel in enumerate(input_row):
        if not (block_start_index <= i <= block_end_index):
            temp_row.append(pixel)

    # 4. Find the index of the maroon (9) pixel within this new, shorter sequence.
    pivot_index_in_temp = find_pivot_index(temp_row)

    # 5. Insert the recorded colored block sequence immediately after the maroon pixel's position
    output_row = temp_row[:pivot_index_in_temp + 1] + colored_block + temp_row[pivot_index_in_temp + 1:]

    # 6. Format the resulting sequence as the output grid (1xN)
    output_grid = [output_row]

    return output_grid
```
```python
"""
Transforms a 1xN input grid by rearranging specific components.
The transformation identifies a contiguous block of a single color (not white 0 or maroon 9),
a single pivot pixel (maroon 9), and the sequence of background pixels (white 0) between them (the gap).
It then reconstructs the row by placing the elements before the block (prefix), followed by the pivot,
the gap, the colored block, and finally the elements after the pivot (suffix).
Essentially, the pivot and the colored block swap positions relative to each other, preserving the gap between them.
"""

import numpy as np
from typing import List, Tuple, Dict, Any

def find_components(row: List[int], background_color: int = 0, pivot_color: int = 9) -> Dict[str, Any]:
    """
    Identifies the pivot, colored block, gap, prefix, and suffix in the row.

    Args:
        row: The input list of pixel values.
        background_color: The value representing the background.
        pivot_color: The value representing the pivot pixel.

    Returns:
        A dictionary containing:
        - 'pivot_index': Index of the pivot pixel.
        - 'block': List of pixels in the colored block.
        - 'block_start': Start index of the colored block.
        - 'block_end': End index of the colored block.
        - 'gap': List of pixels in the gap between block and pivot.
        - 'prefix': List of pixels before the colored block.
        - 'suffix': List of pixels after the pivot pixel.
    Raises:
        ValueError: If the pivot or colored block is not found, or if the input assumptions are violated.
    """
    pivot_index = -1
    block = []
    block_start = -1
    block_end = -1
    in_block = False
    block_color = -1

    # First pass: Find pivot and potential block
    for i, pixel in enumerate(row):
        if pixel == pivot_color:
            if pivot_index != -1:
                raise ValueError("More than one pivot pixel found.")
            pivot_index = i
        elif pixel != background_color and pixel != pivot_color:
            if not in_block: # Start of a potential block
                 # Check if we already found a block and are starting another
                if block_start != -1:
                     raise ValueError("More than one colored block found.")
                block_start = i
                block_color = pixel
                in_block = True
                block.append(pixel)
                block_end = i
            elif in_block and pixel == block_color: # Continue the block
                block.append(pixel)
                block_end = i
            elif in_block and pixel != block_color: # End of the block (different color)
                in_block = False
        elif in_block: # End of the block (background or pivot)
            in_block = False

    # Validate findings
    if pivot_index == -1:
        raise ValueError(f"Pivot color {pivot_color} not found.")
    if not block:
        raise ValueError("Colored block not found.")
    if block_end >= pivot_index:
         raise ValueError("Colored block must precede the pivot pixel in the input.")

    # Identify components based on indices
    prefix = row[:block_start]
    # The gap is strictly between the block end and pivot start
    gap = row[block_end + 1 : pivot_index]
    # Ensure gap contains only background color (as per observed examples)
    if any(p != background_color for p in gap):
        # This check might be too strict based on problem description,
        # but matches the training examples provided.
        # If requirements change, this check might need removal/modification.
         print(f"Warning: Gap contains non-background pixels: {gap}")
         # Decide how to handle: raise ValueError("Gap contains non-background pixels.") or proceed

    suffix = row[pivot_index + 1:]

    return {
        'pivot_index': pivot_index,
        'pivot_value': pivot_color, # Store the actual pivot value
        'block': block,
        'block_start': block_start,
        'block_end': block_end,
        'gap': gap,
        'prefix': prefix,
        'suffix': suffix
    }


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid according to the described rearrangement rule.
    """
    # Validate input format
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        raise ValueError("Input grid must be a list containing a single list (1xN).")

    input_row = input_grid[0]

    # 1. Parse the input row to identify components
    try:
        components = find_components(input_row)
    except ValueError as e:
        print(f"Error processing input row: {e}")
        # Depending on ARC evaluation rules, might need to return input or handle differently
        return input_grid # Return original grid if components aren't found as expected

    # Extract components for clarity
    prefix = components['prefix']
    pivot_value = components['pivot_value'] # Use the actual value found
    gap = components['gap']
    colored_block = components['block']
    suffix = components['suffix']

    # 2. Construct the output row by concatenating in the new order
    # Order: prefix + pivot + gap + colored_block + suffix
    output_row = prefix + [pivot_value] + gap + colored_block + suffix

    # 3. Return the newly constructed row as the output grid
    output_grid = [output_row]

    # Optional: Validate output length matches input length
    if len(output_row) != len(input_row):
         print(f"Warning: Output length ({len(output_row)}) differs from input length ({len(input_row)}).")
         # This might indicate an error in component identification or concatenation logic.

    return output_grid
```
```python
"""
Transforms a 1xN input grid by rearranging specific components.
The transformation identifies a contiguous block of a single color (not white 0 or maroon 9),
a single pivot pixel (maroon 9), and the sequence of pixels (the gap) between them.
It then reconstructs the row by placing the elements before the block (prefix), followed by the pivot,
the gap, the colored block, and finally the elements after the pivot (suffix).
Essentially, the pivot and the colored block swap positions relative to each other, preserving the gap and all other elements' relative order.
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Union

def find_components_1d(row: List[int], background_color: int = 0, pivot_color: int = 9) -> Dict[str, Any]:
    """
    Identifies the pivot, colored block, gap, prefix, and suffix in a 1D row.

    Args:
        row: The input list of pixel values.
        background_color: The value representing the background.
        pivot_color: The value representing the pivot pixel.

    Returns:
        A dictionary containing:
        - 'pivot_index': Index of the pivot pixel.
        - 'pivot_value': Value of the pivot pixel (should be pivot_color).
        - 'block': List of pixels in the colored block.
        - 'block_start': Start index of the colored block.
        - 'block_end': End index of the colored block.
        - 'gap': List of pixels in the gap between block and pivot.
        - 'prefix': List of pixels before the colored block.
        - 'suffix': List of pixels after the pivot pixel.
    Raises:
        ValueError: If the pivot or colored block is not found, or if the input assumptions are violated (e.g., block not before pivot).
    """
    pivot_index = -1
    block = []
    block_start = -1
    block_end = -1
    in_block = False
    block_color = -1

    # First pass: Find pivot and the single colored block
    for i, pixel in enumerate(row):
        if pixel == pivot_color:
            if pivot_index != -1:
                raise ValueError("More than one pivot pixel found.")
            pivot_index = i
        elif pixel != background_color and pixel != pivot_color:
            current_pixel_color = pixel
            if not in_block: # Start of a potential block
                # Check if we already found a block and are starting another distinct one
                if block_start != -1:
                     raise ValueError("More than one colored block found or block is non-contiguous.")
                block_start = i
                block_color = current_pixel_color
                in_block = True
                block.append(pixel)
                block_end = i
            elif in_block and pixel == block_color: # Continue the block
                block.append(pixel)
                block_end = i
            elif in_block and pixel != block_color: # End of the block (different non-bg/pivot color)
                # This implies a second block or non-contiguous block, which violates assumptions
                raise ValueError("Found second colored block or non-contiguous block.")
        elif in_block: # End of the block (background or pivot detected after being in_block)
            in_block = False # Reset flag, the block definition is complete

    # Validate findings
    if pivot_index == -1:
        raise ValueError(f"Pivot color {pivot_color} not found.")
    if not block:
        raise ValueError("Colored block not found.")
    if block_end >= pivot_index:
         raise ValueError("Colored block must precede the pivot pixel in the input.")

    # Identify components based on indices
    prefix = row[:block_start]
    gap = row[block_end + 1 : pivot_index] # Gap is between block end and pivot start
    suffix = row[pivot_index + 1:]
    pivot_value = row[pivot_index] # Store the actual pivot value found

    return {
        'pivot_index': pivot_index,
        'pivot_value': pivot_value,
        'block': block,
        'block_start': block_start,
        'block_end': block_end,
        'gap': gap,
        'prefix': prefix,
        'suffix': suffix
    }


def transform(input_grid: Union[np.ndarray, List[List[int]]]) -> Union[np.ndarray, List[List[int]]]:
    """
    Applies the rearrangement transformation to the input grid.

    Args:
        input_grid: A 1xN grid, represented as a numpy array or list of lists.

    Returns:
        The transformed 1xN grid in the same format as the input.
    """
    # --- Input Handling ---
    is_numpy = isinstance(input_grid, np.ndarray)
    
    # Convert numpy array to list of lists for consistent processing
    if is_numpy:
        # Ensure it's 2D, even if 1xN
        if input_grid.ndim == 1:
             input_list = [input_grid.tolist()] # Treat 1D array as single row
        elif input_grid.ndim == 2:
             input_list = input_grid.tolist()
        else:
            raise ValueError("Input grid must be 1D or 2D.")
    elif isinstance(input_grid, list) and isinstance(input_grid[0], list):
         input_list = input_grid
    else:
         # Handle case where input might be just a flat list like [0, 0, 1, 1, 0, 9, 0]
         if isinstance(input_grid, list) and all(isinstance(x, int) for x in input_grid):
             input_list = [input_grid]
             is_numpy = False # Treat it as list of list conceptually
         else:
            raise TypeError("Input must be a numpy array or list of lists representing the grid.")

    # --- Validation ---
    if len(input_list) != 1:
        raise ValueError("Input grid must contain exactly one row.")
    
    input_row = input_list[0]
    if not input_row: # Handle empty row case
        # Decide behavior: return empty or raise error? Returning empty seems safer.
        return np.array([[]]) if is_numpy else [[]]

    # --- Core Logic ---
    try:
        # 1. Parse the input row to identify components
        components = find_components_1d(input_row)
    except ValueError as e:
        # Handle cases where the expected structure isn't found
        print(f"Warning: Could not find expected components in input row: {e}. Returning original grid.")
        # Depending on ARC rules, returning original might be necessary
        return input_grid

    # 2. Extract components for clarity
    prefix = components['prefix']
    pivot_value = components['pivot_value']
    gap = components['gap']
    colored_block = components['block']
    suffix = components['suffix']

    # 3. Construct the output row by concatenating in the new order
    # Order: prefix + pivot + gap + colored_block + suffix
    output_row = prefix + [pivot_value] + gap + colored_block + suffix

    # --- Output Formatting ---
    # 4. Format the resulting row back into the original grid structure
    if is_numpy:
        output_grid = np.array([output_row], dtype=input_grid.dtype) # Preserve dtype
    else:
        # Check if original input was list of list or just flat list
        if isinstance(input_grid, list) and isinstance(input_grid[0], list):
             output_grid = [output_row]
        else: # Original was likely a flat list
             output_grid = output_row # Return as flat list


    # --- Final Validation (Optional) ---
    # Ensure output has same length as input row if input wasn't empty
    if input_row and len(output_row) != len(input_row):
         print(f"Warning: Output length ({len(output_row)}) differs from input length ({len(input_row)}). This might indicate an error.")
         # Could raise error here, or return original, depending on desired strictness

    return output_grid
```
