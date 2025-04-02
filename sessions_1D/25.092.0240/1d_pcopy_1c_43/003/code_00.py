import numpy as np

"""
Transforms a 1D input grid based on a pattern replacement rule.

1.  Identify the "pattern": Find the first contiguous horizontal sequence of 
    identical non-white pixels (color C) with a length (L) greater than 1, 
    scanning from left to right.
2.  If no such pattern exists, return the input grid unchanged.
3.  Identify "target" pixels: Locate all single pixels in the *input* grid 
    that have the same color (C) as the pattern. A pixel at index 'i' is 
    considered single if it's not adjacent (horizontally) to another pixel 
    of the same color C (i.e., pixel i-1 (if exists) != C and 
    pixel i+1 (if exists) != C).
4.  Replace targets in the output grid: For each target pixel found at index 'i' 
    in the input grid, determine the replacement start position `start_pos = max(0, i - 1)`. 
    Replace the segment of the *output* grid from `start_pos` up to 
    `min(width, start_pos + L)` with the pattern color (C).
5.  Return the modified grid, preserving the original shape (1D or single-row 2D).
"""

def find_pattern_sequence(grid_1d):
    """
    Finds the first sequence longer than 1 pixel in a 1D grid.
    
    Args:
        grid_1d: A 1D numpy array representing the grid row.

    Returns:
        A tuple (color, length) of the first pattern sequence found, 
        or (None, None) if no sequence longer than 1 exists.
    """
    n = len(grid_1d)
    i = 0
    while i < n:
        color = grid_1d[i]
        # Skip background color
        if color == 0: 
            i += 1
            continue
        
        # Found a non-white pixel, track sequence start
        start_index = i
        j = i + 1
        # Find the end of the sequence of this color
        while j < n and grid_1d[j] == color:
            j += 1
        
        length = j - start_index
        
        # Check if this sequence is the pattern (length > 1)
        if length > 1:
            return color, length # Found the pattern
            
        # Move the main index past the sequence just checked
        i = j 
        
    # No pattern sequence found
    return None, None 

def transform(input_grid):
    """
    Applies the pattern replacement transformation to the input grid.
    """
    # Convert input to numpy array and ensure it's effectively 1D
    input_np = np.array(input_grid, dtype=int)
    original_shape = input_np.shape 
    
    # Handle 1D or single-row 2D arrays
    if input_np.ndim == 1:
        grid_1d = input_np
    elif input_np.ndim == 2 and input_np.shape[0] == 1:
        grid_1d = input_np.flatten()
    else:
        # If input is not 1D or single-row 2D, return it unchanged
        # as the logic is defined for 1D sequences.
        # print(f"Warning: Input grid shape {original_shape} is not 1D or single-row 2D. Returning input unchanged.")
        return input_grid

    width = len(grid_1d)
    
    # Initialize output_grid as a copy of the 1D input
    output_grid_1d = grid_1d.copy()

    # Step 1: Find the pattern sequence (color C, length L)
    pattern_color, pattern_length = find_pattern_sequence(grid_1d)

    # Step 2: If no pattern found, return the original input (reshaped)
    if pattern_color is None:
        return output_grid_1d.reshape(original_shape)

    # Step 3 & 4: Find single target pixels in the *input* grid 
    #             and perform replacement in the *output* grid
    i = 0
    while i < width:
        # Check if current pixel in the input grid matches pattern color
        if grid_1d[i] == pattern_color:
            # Check if it's a single pixel sequence in the input grid
            is_single = True
            # Check left neighbor (if exists)
            if i > 0 and grid_1d[i-1] == pattern_color:
                is_single = False
            # Check right neighbor (if exists)
            if i < width - 1 and grid_1d[i+1] == pattern_color:
                is_single = False
            
            # If it's a single target pixel
            if is_single:
                # Calculate the start position for replacement in the output grid
                start_index = max(0, i - 1)
                # Calculate the end index (exclusive) for replacement, capped by grid width
                end_index = min(width, start_index + pattern_length)
                # Replace the segment in the output grid
                output_grid_1d[start_index:end_index] = pattern_color
                # Move to the next pixel in the input grid
                i += 1 
            else:
                # It's part of a longer sequence in the input, just move to the next pixel
                i += 1
        else:
            # Not the pattern color, move to the next pixel in the input grid
            i += 1

    # Step 5: Reshape the output to match the original input shape and return
    return output_grid_1d.reshape(original_shape)