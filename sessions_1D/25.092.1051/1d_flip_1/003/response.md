```python
import numpy as np
import collections

"""
Transforms the input grid by identifying a contiguous non-white segment 
in the first row, finding a single 'singleton' pixel and a contiguous 'block' 
of another color within that segment, and then swapping their relative positions. 
Background pixels (color 0) remain unchanged.

The transformation logic assumes the input is a 1xN grid (or processes only 
the first row) and the non-white segment contains exactly one singleton pixel 
and one block of pixels of another color, positioned adjacently at the ends 
of the segment.
"""

def find_non_white_segment_info(row):
    """
    Finds the start, end indices and extracts the contiguous non-white segment 
    from a 1D row (list or numpy array). Also checks for contiguity.
    
    Args:
        row (np.array or list): A 1D array/list of integers representing a row.

    Returns:
        tuple: (start_index, end_index, segment_array) or (None, None, None) if 
               no non-white segment is found or it's not contiguous.
    """
    # Find indices of non-white pixels
    non_white_indices = np.where(np.array(row) != 0)[0]
    
    if non_white_indices.size == 0:
        # No non-white pixels found
        return None, None, None
        
    start = non_white_indices.min()
    end = non_white_indices.max()
    
    # Check for contiguity: the number of non-white pixels should match the span
    if (end - start + 1) != non_white_indices.size:
         # The non-white pixels are not in a single contiguous block
        return None, None, None

    # Extract the segment as a numpy array
    segment = np.array(row)[start : end + 1]
    return start, end, segment

def analyze_segment_and_swap(segment):
    """
    Analyzes a non-white segment to find singleton and block, then constructs
    the swapped segment.

    Args:
        segment (np.array): The numpy array of non-white pixels forming the segment.

    Returns:
        np.array: The segment with singleton and block positions swapped, 
                  or None if the segment doesn't fit the expected pattern.
    """
    if segment.size < 2: # Need at least one singleton and one block pixel
        return None

    # Count occurrences of each color in the segment
    unique_colors, counts = np.unique(segment, return_counts=True)
    
    # Expecting exactly two distinct non-white colors
    if unique_colors.size != 2: 
        return None

    singleton_color = None
    block_color = None
    block_length = 0
    
    # Identify singleton (count=1) and block (count>1) colors
    for color, count in zip(unique_colors, counts):
        if count == 1:
            singleton_color = color
        elif count > 1:
            block_color = color
            block_length = count
        # Note: We already checked unique_colors.size == 2, so other counts aren't possible

    # Check if we successfully identified both
    if singleton_color is None or block_color is None:
        return None # Should not happen if unique_colors.size == 2

    # Find the position index of the singleton within the segment
    # np.where returns a tuple of arrays, we need the first element of the first array
    singleton_index_in_segment = np.where(segment == singleton_color)[0]
    
    # Check if singleton was found and there's only one
    if singleton_index_in_segment.size != 1:
         return None # Should not happen if counts were correct

    singleton_index_in_segment = singleton_index_in_segment[0]
    segment_length = segment.size

    # Construct the new segment with swapped positions
    new_segment_list = []
    
    # Check if singleton is at the beginning of the segment
    if singleton_index_in_segment == 0:
        # Place block first, then singleton
        new_segment_list.extend([block_color] * block_length)
        new_segment_list.append(singleton_color)
    # Check if singleton is at the end of the segment
    elif singleton_index_in_segment == segment_length - 1:
        # Place singleton first, then block
        new_segment_list.append(singleton_color)
        new_segment_list.extend([block_color] * block_length)
    else:
        # Singleton is in the middle - not expected by examples
        return None

    # Safety check: ensure the new segment has the correct length
    if len(new_segment_list) != segment_length:
        return None # Logic error

    return np.array(new_segment_list)


def transform(input_grid):
    """
    Applies the singleton-block swap transformation to the input grid.
    Handles NumPy array input and returns a list of lists.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # Handle empty or non-2D input
    if input_np.ndim != 2 or input_np.shape[0] == 0 or input_np.shape[1] == 0:
        # Return input as list of lists if it's invalid/empty
        return input_grid 

    # Work primarily on the first row as per examples
    input_row = input_np[0]
    # Create a mutable copy for the output
    output_row = input_row.copy() 

    # 1. Identify the contiguous segment of non-white pixels
    start, end, segment = find_non_white_segment_info(input_row)

    # If no valid segment found, return the original grid unchanged
    if start is None:
        # Convert back to list of lists format
        return input_np.tolist()

    # 2. Analyze the segment and create the swapped version
    new_segment = analyze_segment_and_swap(segment)
    
    # If segment analysis or swap fails (doesn't match pattern), return original
    if new_segment is None:
        return input_np.tolist()

    # 3. Place the newly constructed segment back into the output row
    output_row[start : end + 1] = new_segment

    # 4. Construct the final output grid (currently assuming 1 row input)
    # If input had more rows, they should be preserved.
    output_np = input_np.copy() # Start with a copy of the original grid
    output_np[0] = output_row   # Update the first row

    # 5. Return the modified grid as a list of lists
    return output_np.tolist()
```