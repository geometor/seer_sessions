
## train_1

**input:**
```
3 3 3 3 0 0 9 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 9 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 7 7 7 7 7 7 7 7 0 0 9 0 0
```


**output:**
```
0 0 0 7 7 7 7 7 7 7 7 9 0 0
```


## train_3

**input:**
```
0 0 0 0 3 3 3 3 3 0 0 9 0 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 3 9 0 0
```

*   **Perception of Elements:**
    *   The input and output are both single-row grids (1D arrays) of the same length (14 pixels).
    *   Each input grid contains a contiguous block of a single color (e.g., green '3' in train\_1, orange '7' in train\_2). This block is neither white ('0') nor maroon ('9').
    *   Each input grid also contains exactly one maroon ('9') pixel.
    *   The main colored block always appears before the maroon pixel.
    *   There may be white ('0') pixels before the main block, between the main block and the maroon pixel, and after the maroon pixel.
    *   In the output, the main colored block and the maroon pixel appear adjacent to each other, with any white pixels that were originally between them removed.
    *   This combined structure (main block + maroon pixel) is shifted two positions to the right compared to the starting position of the main block in the input.
    *   The positions to the left, vacated or shifted over, are filled with white ('0') pixels. Pixels to the right of the maroon pixel in the input seem to remain in their relative positions after the shifted structure.

*   **YAML Facts:**
    
```yaml
    task_type: array_transformation
    grid_dimensionality: 1D
    grid_size_input: [1, 14]
    grid_size_output: [1, 14]
    objects:
      - id: main_block
        description: A contiguous sequence of pixels of the same color, excluding white (0) and maroon (9).
        properties:
          color: variable (e.g., green, orange)
          contiguity: true
      - id: marker_pixel
        description: A single maroon (9) pixel.
        properties:
          color: maroon (9)
          count: 1
      - id: background_pixels
        description: White (0) pixels.
        properties:
          color: white (0)
    relationships:
      - type: relative_position
        object1: main_block
        object2: marker_pixel
        details: main_block appears before marker_pixel in the row.
      - type: separation
        object1: main_block
        object2: marker_pixel
        details: May be separated by one or more background_pixels (white).
    actions:
      - id: identify_main_block
        description: Locate the start and end indices of the main_block.
      - id: identify_marker
        description: Locate the index of the marker_pixel.
      - id: concatenate_structure
        description: Create a new sequence by taking the main_block immediately followed by the marker_pixel, removing any intervening background_pixels.
      - id: horizontal_shift
        description: Shift the concatenated structure horizontally to the right.
        details: The shift amount is 2 positions relative to the original starting index of the main_block.
      - id: padding
        description: Fill the positions to the left of the shifted structure with background_pixels (white).
      - id: construct_output
        description: Assemble the final output row by placing the padded background_pixels, the shifted structure, and any remaining background_pixels from the end of the input row.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid of the same dimensions as the input grid, filled with white (0) pixels.
    2.  Scan the input row to find the first pixel that is not white (0) and not maroon (9). This marks the start of the main colored block.
    3.  Identify the sequence of identical, non-white, non-maroon pixels that form the main block. Record its color and its pixel values. Let the starting index of this block be `start_index`.
    4.  Scan the input row starting from the end of the main block to find the index of the single maroon (9) pixel. Record its value (9).
    5.  Create a new temporary sequence consisting of the pixels from the main block followed immediately by the maroon pixel (9).
    6.  Calculate the target starting index in the output grid for this new sequence: `target_start_index = start_index + 2`.
    7.  Place the temporary sequence into the output grid, starting at `target_start_index`.
    8.  Ensure all positions in the output grid before `target_start_index` are filled with white (0) pixels.
    9.  Ensure all positions in the output grid after the placed sequence match the corresponding trailing white pixels from the input grid (if any remain after the shift). (Alternatively, Step 1 already initializes the whole output grid with white, so only the placement in step 7 is needed, overwriting the initial white pixels).
```python
import numpy as np
from typing import List, Tuple

"""
Transformation Rule:
1. Identify the contiguous block of non-white (0), non-maroon (9) pixels (the 'main block') and its starting index.
2. Identify the single maroon (9) pixel ('marker').
3. Create a new sequence by concatenating the main block's pixels followed immediately by the marker pixel.
4. Determine the target starting position for this new sequence by adding 2 to the original starting index of the main block.
5. Construct the output row by placing the new sequence at the target starting position, filling all preceding positions with white (0) pixels, and keeping the remaining positions (after the placed sequence) as white (0).
"""

def find_main_block(row: List[int]) -> Tuple[int, int, List[int]]:
    """
    Finds the main colored block (non-0, non-9) in the row.

    Args:
        row: The input row (list of integers).

    Returns:
        A tuple containing:
        - start_index: The starting index of the block.
        - end_index: The ending index (exclusive) of the block.
        - block_pixels: A list of the pixels in the block.
        Returns (-1, -1, []) if no such block is found.
    """
    start_index = -1
    block_color = -1
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 9:
            start_index = i
            block_color = pixel
            break
            
    if start_index == -1:
        return -1, -1, [] # No main block found

    end_index = start_index
    block_pixels = []
    while end_index < len(row) and row[end_index] == block_color:
        block_pixels.append(row[end_index])
        end_index += 1
        
    return start_index, end_index, block_pixels

def find_marker(row: List[int], search_start_index: int) -> int:
    """
    Finds the index of the marker pixel (9) starting from a given index.

    Args:
        row: The input row (list of integers).
        search_start_index: The index to start searching from.

    Returns:
        The index of the marker pixel (9), or -1 if not found.
    """
    for i in range(search_start_index, len(row)):
        if row[i] == 9:
            return i
    return -1

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list containing a single list representing the input row.

    Returns:
        A list containing a single list representing the transformed output row.
    """
    # Ensure input is a 1D array represented as a list of lists
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
         raise ValueError("Input must be a list of lists.")
         
    input_row = input_grid[0]
    n = len(input_row)
    
    # Initialize the output row with white (0) pixels
    output_row = [0] * n

    # 1. Find the main block
    start_index, end_index, main_block_pixels = find_main_block(input_row)
    
    # Handle cases where no main block is found (though unlikely based on examples)
    if start_index == -1:
        return [output_row] # Return default white row or handle error

    # 2. Find the marker pixel (9)
    # Search starts after the main block
    marker_index = find_marker(input_row, end_index)
    
    # Handle cases where no marker is found (though unlikely based on examples)
    if marker_index == -1:
         # Or potentially just use the block without the marker if rules allow?
         # Based on examples, the marker is always present.
         # For now, assume it's an error or return default.
        return [output_row] 
        
    # 3. Create the combined sequence
    combined_sequence = main_block_pixels + [9]

    # 4. Calculate the target starting index
    target_start_index = start_index + 2

    # 5. Place the combined sequence into the output row
    # Ensure the placement doesn't go out of bounds
    combined_len = len(combined_sequence)
    if target_start_index + combined_len <= n:
        for i in range(combined_len):
            output_row[target_start_index + i] = combined_sequence[i]
    else:
        # Handle edge case where shifted sequence would exceed bounds
        # Option 1: Truncate the sequence
        placeable_len = n - target_start_index
        for i in range(placeable_len):
             if target_start_index + i < n: # Double check bounds
                output_row[target_start_index + i] = combined_sequence[i]
        # Option 2: Error or return default (truncation seems more likely in ARC)
        pass # Current implementation truncates implicitly if target_start_index is near end


    # The rest of the output_row remains 0 (white) as initialized

    # Return the output row within a list
    return [output_row]

```
```python
"""
Transformation Rule:
1.  Identify the contiguous block of non-white (0), non-maroon (9) pixels (the 'main block') and its starting index in the input row.
2.  Identify the single maroon (9) pixel (the 'marker') in the input row, located after the main block.
3.  Create a new sequence by concatenating the main block's pixels followed immediately by the marker pixel (9).
4.  Determine the target starting position for this new sequence in the output row by adding 2 to the original starting index of the main block.
5.  Construct the output row (same length as the input) by:
    a. Initializing it with white (0) pixels.
    b. Placing the new combined sequence at the target starting position, overwriting the initial white pixels. Truncate the sequence if it extends beyond the row boundaries.
"""

import numpy as np
from typing import List, Tuple, Optional

def find_main_block_np(row: np.ndarray) -> Tuple[Optional[int], Optional[int], Optional[np.ndarray]]:
    """
    Finds the main colored block (non-0, non-9) in the NumPy row array.

    Args:
        row: The input row as a 1D NumPy array.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block, or None if not found.
        - end_index: The ending index (exclusive) of the block, or None if not found.
        - block_pixels: A NumPy array of the pixels in the block, or None if not found.
    """
    start_index = -1
    block_color = -1
    
    # Find the start of the block
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 9:
            start_index = i
            block_color = pixel
            break
            
    if start_index == -1:
        return None, None, None # No main block found

    # Find the end of the block
    end_index = start_index
    while end_index < len(row) and row[end_index] == block_color:
        end_index += 1
        
    block_pixels = row[start_index:end_index]
        
    return start_index, end_index, block_pixels

def find_marker_np(row: np.ndarray, search_start_index: int) -> Optional[int]:
    """
    Finds the index of the marker pixel (9) starting from a given index in the NumPy row.

    Args:
        row: The input row as a 1D NumPy array.
        search_start_index: The index to start searching from.

    Returns:
        The index of the marker pixel (9), or None if not found.
    """
    marker_indices = np.where(row[search_start_index:] == 9)[0]
    if len(marker_indices) > 0:
        return search_start_index + marker_indices[0] # Return the first occurrence
    return None


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list containing a single list representing the input row.

    Returns:
        A list containing a single list representing the transformed output row.
    """
    # Convert input list to NumPy array for efficient processing
    # Assuming input is always [1, N]
    if not input_grid or not input_grid[0]:
         # Handle empty input case if necessary, perhaps return empty grid?
         return [[]]
    input_row = np.array(input_grid[0], dtype=int)
    n = len(input_row)
    
    # Initialize the output row with white (0) pixels using NumPy
    output_row = np.zeros(n, dtype=int)

    # 1. Find the main block
    start_index, end_index, main_block_pixels = find_main_block_np(input_row)
    
    # Handle cases where no main block is found
    if start_index is None or main_block_pixels is None:
        # Return the initialized white row if no block found
        return [output_row.tolist()] 

    # 2. Find the marker pixel (9)
    # Search starts from the end of the main block
    marker_index = find_marker_np(input_row, end_index if end_index is not None else 0)
    
    # Handle cases where no marker is found
    if marker_index is None:
        # Return the initialized white row if no marker found
        # (or apply alternative logic if needed, but examples show marker always exists)
        return [output_row.tolist()] 
        
    # 3. Create the combined sequence using NumPy concatenation
    marker_pixel = np.array([9], dtype=int)
    combined_sequence = np.concatenate((main_block_pixels, marker_pixel))

    # 4. Calculate the target starting index
    target_start_index = start_index + 2

    # 5. Place the combined sequence into the output row using NumPy slicing
    # Calculate the actual end position, respecting array bounds
    combined_len = len(combined_sequence)
    place_end_index = min(target_start_index + combined_len, n)
    
    # Calculate how many elements of the sequence can actually be placed
    placeable_len = place_end_index - target_start_index

    if placeable_len > 0:
        # Place the (potentially truncated) sequence
        output_row[target_start_index:place_end_index] = combined_sequence[:placeable_len]

    # Convert the final NumPy array back to a list of lists for the return value
    return [output_row.tolist()]
```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
1.  Identify the contiguous block of non-white (0), non-maroon (9) pixels (the 'main block') and its starting index in the input row.
2.  Identify the single maroon (9) pixel (the 'marker') in the input row, located after the main block.
3.  Create a new sequence by concatenating the main block's pixels followed immediately by the marker pixel (9).
4.  Determine the target starting position for this new sequence in the output row by adding 2 to the original starting index of the main block.
5.  Construct the output row (same length as the input) by:
    a. Initializing it with white (0) pixels.
    b. Placing the new combined sequence at the target starting position, overwriting the initial white pixels. Truncate the sequence if it extends beyond the row boundaries.
"""

def find_main_block_np(row: np.ndarray) -> Tuple[Optional[int], Optional[int], Optional[np.ndarray]]:
    """
    Finds the main colored block (non-0, non-9) in the NumPy row array.

    Args:
        row: The input row as a 1D NumPy array.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block, or None if not found.
        - end_index: The ending index (exclusive) of the block, or None if not found.
        - block_pixels: A NumPy array of the pixels in the block, or None if not found.
    """
    start_index = -1
    block_color = -1
    
    # Find the start of the block
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 9:
            start_index = i
            block_color = pixel
            break
            
    if start_index == -1:
        return None, None, None # No main block found

    # Find the end of the block
    end_index = start_index
    while end_index < len(row) and row[end_index] == block_color:
        end_index += 1
        
    block_pixels = row[start_index:end_index]
        
    return start_index, end_index, block_pixels

def find_marker_np(row: np.ndarray, search_start_index: int) -> Optional[int]:
    """
    Finds the index of the marker pixel (9) starting from a given index in the NumPy row.

    Args:
        row: The input row as a 1D NumPy array.
        search_start_index: The index to start searching from.

    Returns:
        The index of the marker pixel (9), or None if not found.
    """
    # Use np.where to find indices of value 9 starting from search_start_index
    potential_indices = np.where(row[search_start_index:] == 9)[0]
    if len(potential_indices) > 0:
        # Return the absolute index (relative index + search_start_index)
        return search_start_index + potential_indices[0] 
    return None # Marker not found


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to NumPy array (assuming 1 row)
    if not input_grid or not input_grid[0]:
         return [[]] # Handle empty input
    input_row = np.array(input_grid[0], dtype=int)
    n = len(input_row)
    
    # Initialize the output row with white (0) pixels using NumPy
    output_row = np.zeros(n, dtype=int)

    # Step 1: Find the main block
    start_index, end_index, main_block_pixels = find_main_block_np(input_row)
    
    # Handle cases where no main block is found - return initialized white row
    # Check start_index directly, not main_block_pixels for boolean ambiguity
    if start_index is None:
        return [output_row.tolist()] 

    # Step 2: Find the marker pixel (9) starting search after the main block
    # Ensure end_index is valid before passing to find_marker_np
    search_start = end_index if end_index is not None else 0
    marker_index = find_marker_np(input_row, search_start)
    
    # Handle cases where no marker is found - return initialized white row
    if marker_index is None:
        return [output_row.tolist()] 
        
    # Step 3: Create the combined sequence using NumPy concatenation
    # Ensure main_block_pixels is a valid array before concatenating
    if main_block_pixels is not None:
        marker_pixel_arr = np.array([9], dtype=int)
        combined_sequence = np.concatenate((main_block_pixels, marker_pixel_arr))
    else:
        # This case should theoretically not be reached if start_index was found
        return [output_row.tolist()] 

    # Step 4: Calculate the target starting index
    target_start_index = start_index + 2

    # Step 5: Place the combined sequence into the output row using NumPy slicing
    # Calculate the actual end position for slicing, respecting array bounds
    combined_len = len(combined_sequence)
    place_end_index = min(target_start_index + combined_len, n)
    
    # Calculate how many elements of the sequence can actually be placed
    # This determines the slice size of the combined_sequence to use
    placeable_len = place_end_index - target_start_index

    # Only place if there's space and the target start is within bounds
    if placeable_len > 0 and target_start_index < n:
        # Place the (potentially truncated) sequence into the output row
        output_row[target_start_index:place_end_index] = combined_sequence[:placeable_len]

    # Convert the final NumPy array back to a list of lists for the return value
    return [output_row.tolist()]
```
