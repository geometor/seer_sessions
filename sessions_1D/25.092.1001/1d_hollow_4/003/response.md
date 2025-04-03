```python
import numpy as np

"""
Transforms a 1D numpy grid by finding the first contiguous horizontal segment of a 
single non-white color (value > 0). It keeps the first (leftmost) and last 
(rightmost) pixels of this segment and changes all pixels *between* these two 
endpoints to white (0). Pixels outside the identified segment remain unchanged. 
If the segment has a length of 1 or 2, or if no non-white segment is found, 
the grid is returned unchanged. The function assumes the input grid has exactly one row.
"""

def find_segment_indices_np(row_array):
    """
    Finds the start and end indices of the first contiguous non-white segment in a numpy row array.

    Args:
        row_array: A 1D numpy array representing a row of the grid.

    Returns:
        A tuple (start_index, end_index) or (None, None) if no segment is found 
        or if the segment is broken/invalid. Indices are integer column numbers.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(row_array != 0)[0] 

    # If no non-zero elements exist, return None
    if len(non_zero_indices) == 0:
        return None, None

    # The start index is the first non-zero index found
    start_index = non_zero_indices[0]
    # Get the color of the segment start
    segment_color = row_array[start_index]
    
    # Initialize the end index to the start index
    end_index = start_index
    
    # Iterate from the element *after* the start index to find the end
    for i in range(start_index + 1, len(row_array)):
        # If the current pixel matches the segment color, update the end index
        if row_array[i] == segment_color:
            end_index = i
        # If the color changes or becomes zero, the segment ends here (before index i)
        else:
            break 
            
    return start_index, end_index


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the segment hollowing transformation to the input grid.

    Args:
        input_grid: A numpy ndarray representing the input grid. Assumed to have 1 row.

    Returns:
        A numpy ndarray representing the transformed output grid.
    """
    # Create a deep copy to avoid modifying the original input
    output_grid = np.copy(input_grid)
    
    # Check if the input grid has exactly one row. If not, return the copy.
    # This handles potential edge cases or invalid inputs based on task constraints.
    if input_grid.shape[0] != 1:
        return output_grid
        
    # Extract the single row (as a 1D array)
    input_row = input_grid[0]
    
    # Find the start and end indices of the non-white segment in the row
    start_index, end_index = find_segment_indices_np(input_row)

    # Check if a valid segment was found
    if start_index is not None and end_index is not None:
        # Check if the segment has inner pixels to modify (length > 2)
        if end_index > start_index + 1:
            # Set the pixels *between* start and end indices to white (0)
            # Note: slicing is [start:end], end is exclusive, so use end_index directly.
            output_grid[0, start_index + 1 : end_index] = 0

    # Return the modified output grid
    return output_grid
```