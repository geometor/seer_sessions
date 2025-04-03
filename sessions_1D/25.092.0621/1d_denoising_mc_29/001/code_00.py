import numpy as np
from collections import Counter

def find_non_white_block_indices(arr):
    """Finds the start and end indices of the contiguous non-white block."""
    non_white_indices = np.where(arr != 0)[0]
    if len(non_white_indices) == 0:
        return None, None  # No non-white pixels found
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)
    return start_index, end_index

def find_dominant_color(arr_slice):
    """Finds the most frequent color in a given array slice."""
    if len(arr_slice) == 0:
        return None # Should not happen if block indices are valid
    
    # Filter out any potential zeros if the block definition was loose, though shouldn't be needed
    non_white_pixels = arr_slice[arr_slice != 0]
    if len(non_white_pixels) == 0:
         # This case means the block identified only contained zeros, which contradicts
         # find_non_white_block_indices logic unless input was malformed.
         # Or, perhaps the block was identified, but only had one element which was zero?
         # Revisit if this causes issues. Based on description, block is non-white.
         # If the original block definition means "span containing all non-white pixels",
         # it *could* contain zeros. Let's stick to the definition "contiguous non-white".
         # If we only count non-white pixels for dominance:
         counts = Counter(non_white_pixels)
         if not counts: # If block was e.g. [0, 5, 0] -> non_white is [5] -> counts is {5:1}
             # If the slice itself was only zeros, non_white_pixels is empty.
             # This scenario needs clarification based on task constraints.
             # Let's assume the block extraction guarantees non-zero elements based on step 2.
             # Fallback: If somehow only zeros were in the slice, return 0? Seems unlikely.
              return 0 # Or raise error?
         else:
              dominant_color = counts.most_common(1)[0][0]

    else:
        # Count frequencies of all non-white colors within the identified block slice
        counts = Counter(non_white_pixels)
        # Determine the mode (most frequent color)
        # most_common(1) returns a list of tuples [(element, count)], we take the first one
        dominant_color = counts.most_common(1)[0][0]
        
    return dominant_color

def transform(input_grid):
    """
    Identifies a contiguous block of non-white pixels (1-9) in a 1D input array.
    Determines the most frequent color (mode) within this block.
    Replaces all pixels within the block in the output array with this dominant color.
    Pixels outside the block (typically white/0) remain unchanged.
    """
    
    # Convert input list to numpy array for easier processing
    input_arr = np.array(input_grid, dtype=int)
    
    # Handle empty input case
    if input_arr.size == 0:
        return [] # Or input_grid directly

    # Find the start and end indices of the contiguous non-white block
    start_index, end_index = find_non_white_block_indices(input_arr)

    # If no non-white block is found, return the original array
    if start_index is None:
        return input_grid # Return in original format (list)

    # Extract the sub-array corresponding to the non-white sequence (inclusive)
    # Note: Slicing in numpy is exclusive for the end index, so add 1
    block_slice = input_arr[start_index : end_index + 1]
    
    # Find the dominant color within this block slice (only considering non-white pixels for mode calculation)
    dominant_color = find_dominant_color(block_slice)

    # Create a copy of the input array to modify
    output_arr = input_arr.copy()

    # Replace all pixels within the identified block boundaries with the dominant color
    # Iterate from start_index to end_index (inclusive)
    # This step homogenizes the block including any original zeros within the min/max non-zero range
    # Revised understanding: The examples suggest *only* the non-white segment needs homogenizing.
    # Let's refine: Replace elements within the identified *span* (start to end index) with the dominant color.
    output_arr[start_index : end_index + 1] = dominant_color

    # Return the modified array converted back to a list
    return output_arr.tolist()