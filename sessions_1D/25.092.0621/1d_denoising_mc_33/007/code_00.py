"""
Homogenizes the colors within the active segment (first to last non-white 
pixel) of a single-row NumPy grid. It identifies the most frequent non-white 
color (dominant_color) within this segment. Then, it iterates through the segment 
in a copy of the grid, replacing any pixel that is not white (0) and not the 
dominant_color with the dominant_color. Pixels outside the segment (padding) 
and white pixels within the segment remain unchanged.
"""

import numpy as np
from collections import Counter

def find_active_segment(row):
    """
    Finds the start and end indices (inclusive) of the segment containing 
    non-white pixels in a 1D NumPy array (row).

    Args:
        row (np.ndarray): A 1D NumPy array representing the pixel colors in the row.

    Returns:
        tuple: A tuple (start_index, end_index). Returns (None, None) if 
               no non-white pixels are found. Indices are inclusive.
    """
    non_zero_indices = np.where(row != 0)[0] # Get indices of non-zero elements
    
    if len(non_zero_indices) == 0:
        return None, None # No non-white pixels found
        
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1] # Inclusive end index
    
    return start_index, end_index

def find_dominant_color_in_segment(row, start_index, end_index):
    """
    Determines the most frequent non-zero color within a specified segment 
    of a 1D NumPy array (row).

    Args:
        row (np.ndarray): The 1D NumPy array representing the full row.
        start_index (int): The starting index of the segment (inclusive).
        end_index (int): The ending index of the segment (inclusive).

    Returns:
        int or None: The most frequent non-zero color value within the segment, 
                     or None if the segment contains only zeros, is invalid, 
                     or if start/end indices are None.
    """
    # Validate indices
    if start_index is None or end_index is None or start_index > end_index:
        return None 

    # Extract the segment using inclusive slicing for NumPy
    # Need end_index + 1 because Python/NumPy slicing is exclusive at the end
    segment = row[start_index : end_index + 1] 
    
    # Filter out zeros (white) and count remaining colors
    non_zero_segment = segment[segment != 0]

    # If no non-zero colors were found after filtering
    if len(non_zero_segment) == 0:
        return None 
        
    # Count frequencies
    color_counts = Counter(non_zero_segment)
        
    # Find the most frequent color. most_common(1) returns a list [(color, count)]
    dominant_color, _ = color_counts.most_common(1)[0]
    return dominant_color

def transform(input_grid):
    """
    Applies the color normalization transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 1xN NumPy array representing the input row.

    Returns:
        np.ndarray: The transformed 1xN NumPy array.
    """
    # Ensure input is a NumPy array and has at least one row
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] == 0:
        # Or handle potential 1D array input if needed based on testing environment
        if isinstance(input_grid, np.ndarray) and input_grid.ndim == 1:
             # Reshape 1D array to 2D (1xN)
             input_grid = input_grid.reshape(1, -1)
        else:
             # Return empty array or raise error for unexpected input types/shapes
             print(f"Warning: Unexpected input type/shape: {type(input_grid)}, shape: {getattr(input_grid, 'shape', 'N/A')}")
             # Returning input shape might be safer if empty is wrong
             return np.array([[]], dtype=int) if input_grid.ndim == 2 else np.array([], dtype=int)


    # Handle empty row case specifically if shape is (1, 0)
    if input_grid.shape[1] == 0:
        return np.array([[]], dtype=int) # Return 1x0 array

    # Select the first (and only) row
    input_row = input_grid[0]

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    output_row = output_grid[0] # Get a reference to the row in the copy

    # 1. Identify the active segment (indices of first to last non-white pixels)
    start_index, end_index = find_active_segment(input_row)

    # 2. If no non-white segment exists (row is all white or empty), return the original copy
    if start_index is None:
        return output_grid 

    # 3. Determine the dominant color within the identified active segment
    dominant_color = find_dominant_color_in_segment(input_row, start_index, end_index)
    
    # 4. If a dominant color is found, normalize the segment in the output row
    if dominant_color is not None:
        # Iterate *only* through the indices corresponding to the active segment (inclusive)
        for i in range(start_index, end_index + 1):
            # Check if the current pixel in the segment is not white (0) 
            # AND is not the dominant color.
            if output_row[i] != 0 and output_row[i] != dominant_color:
                 # Replace this 'impurity' pixel with the dominant color
                output_row[i] = dominant_color
                # Pixels that are 0 or already the dominant color within the segment are unchanged.
                
    # 5. Return the modified output grid. Pixels outside the segment (padding) were never touched.
    return output_grid