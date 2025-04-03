import numpy as np

"""
Move a single 'marker' pixel from the position immediately before a contiguous block of different-colored pixels to the position immediately after that block within a single row.
"""

def find_pattern_indices(row):
    """
    Finds the index of the marker pixel and the start/end indices of the object block.

    Args:
        row (list or np.array): The input row of pixels.

    Returns:
        tuple: (marker_idx, block_start_idx, block_end_idx) or None if pattern not found.
    """
    for i in range(len(row) - 1):
        # Check for a non-white pixel followed by a different non-white pixel
        if row[i] != 0 and row[i+1] != 0 and row[i] != row[i+1]:
            marker_idx = i
            block_start_idx = i + 1
            block_color = row[block_start_idx]

            # Find the end of the block
            block_end_idx = block_start_idx
            for j in range(block_start_idx + 1, len(row)):
                if row[j] == block_color:
                    block_end_idx = j
                else:
                    break  # End of the block
            
            return marker_idx, block_start_idx, block_end_idx
            
    return None # Pattern not found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (single row).

    1. Finds the marker pixel and the adjacent object block.
    2. Rearranges the row to move the marker pixel after the object block.

    Args:
        input_grid (list or np.array): A single row represented as a list or numpy array.

    Returns:
        list or np.array: The transformed row.
    """
    # Ensure input is a list for easier manipulation if it's numpy
    input_row = list(input_grid) 
    
    # Find the indices of the marker and the block
    indices = find_pattern_indices(input_row)

    if indices is None:
        # If the pattern isn't found, return the original row (or handle as error)
        # Based on examples, the pattern should always exist.
        return input_row 

    marker_idx, block_start_idx, block_end_idx = indices

    # Extract the marker pixel value
    marker_pixel_value = input_row[marker_idx]

    # Construct the output row
    output_row = []
    
    # 1. Add pixels before the marker
    output_row.extend(input_row[:marker_idx])
    
    # 2. Add the object block
    output_row.extend(input_row[block_start_idx : block_end_idx + 1])
    
    # 3. Add the marker pixel
    output_row.append(marker_pixel_value)
    
    # 4. Add pixels after the object block
    output_row.extend(input_row[block_end_idx + 1:])

    # Convert back to numpy array if the original input was numpy
    if isinstance(input_grid, np.ndarray):
        return np.array(output_row, dtype=input_grid.dtype)
    else:
         return output_row
