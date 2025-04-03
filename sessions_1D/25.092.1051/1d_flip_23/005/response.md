```python
import numpy as np
import copy

"""
Swap the colors of the first and last pixels of a specific contiguous horizontal segment 
within a single-row grid. The segment is defined as the first non-background pixel 
(marker) followed immediately by a sequence of one or more pixels of a single, 
different, non-background color (sequence). All other pixels remain unchanged.
"""

def find_pattern_segment_indices(row):
    """
    Finds the indices of the marker pixel and the end of its adjacent sequence.

    Args:
        row (np.array): A 1D NumPy array representing a row of the grid.

    Returns:
        tuple: A tuple containing (marker_idx, sequence_end_idx), 
               or (None, None) if the required pattern is not found.
    """
    marker_idx = -1
    marker_color = -1
    sequence_end_idx = -1
    
    # 1. Find the marker pixel (first non-zero element)
    non_zero_indices = np.where(row != 0)[0]
    if len(non_zero_indices) == 0:
        # No non-background pixels found
        return None, None
        
    marker_idx = non_zero_indices[0]
    marker_color = row[marker_idx]
        
    # 2. Check the pixel immediately following the marker
    seq_start_idx = marker_idx + 1
    # Check bounds: sequence must start within the row
    if seq_start_idx >= len(row): 
        return None, None
        
    sequence_color = row[seq_start_idx]
    
    # Check if the sequence start pixel is valid:
    # - Must not be background (0)
    # - Must have a different color than the marker
    if sequence_color == 0 or sequence_color == marker_color:
        return None, None
        
    # 3. Find the end of the contiguous sequence of sequence_color
    # Initialize end index to the start of the sequence (the first sequence pixel)
    sequence_end_idx = seq_start_idx 
    for i in range(seq_start_idx + 1, len(row)):
        if row[i] == sequence_color:
            # Extend the sequence if the color matches
            sequence_end_idx = i
        else:
            # End of sequence found (or end of row reached)
            break 
            
    # Pattern is confirmed, return the start and end indices of the segment
    return marker_idx, sequence_end_idx


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by swapping the colors of the first and last pixels
    of an identified pattern segment.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid. 
                                 Expected to be 1xN based on examples.

    Returns:
        np.ndarray: A 2D NumPy array representing the transformed grid.
    """
    # Ensure input is a NumPy array, create a copy to modify
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid) # Convert if it's a list of lists
        
    output_grid = np.copy(input_grid)

    # Check if it's a single-row grid as expected from examples
    if output_grid.shape[0] == 1:
        # Access the single row
        row = output_grid[0] 
        # Also get the original row for reading colors before swap
        original_row = input_grid[0] 
        
        # Find the indices defining the pattern segment
        marker_idx, sequence_end_idx = find_pattern_segment_indices(original_row)
        
        # If the pattern segment was successfully found
        if marker_idx is not None and sequence_end_idx is not None:
            # Retrieve the original colors to be swapped
            # Read from original_row to avoid issues if row was modified prematurely
            marker_color = original_row[marker_idx]
            # The sequence color is determined by the pixel right after the marker
            sequence_color = original_row[marker_idx + 1] 
            
            # Perform the color swap on the output grid's row
            row[marker_idx] = sequence_color
            row[sequence_end_idx] = marker_color
            
    # Return the modified grid (or the original copy if no transformation occurred)
    return output_grid
```