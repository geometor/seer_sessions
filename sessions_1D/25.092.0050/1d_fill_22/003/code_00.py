import numpy as np

"""
Identifies the two non-white pixels in the input row vector (1D grid). 
Fills the segment of white pixels located strictly between these two non-white pixels 
with the same non-white color. If exactly two non-white pixels are not found, 
or they are adjacent, the original grid is returned.
"""

def find_markers(grid_np):
    """
    Finds the indices and color of the two non-white marker pixels.

    Args:
        grid_np (np.array): A 1D numpy array representing the input grid row.

    Returns:
        tuple: A tuple containing (min_index, max_index, color) if exactly two
               non-white pixels are found. Otherwise, returns (None, None, None).
    """
    # Find indices of all non-zero (non-white) pixels
    non_white_indices = np.nonzero(grid_np)[0]

    # Check if exactly two non-white pixels were found
    if len(non_white_indices) == 2:
        # Get the indices
        index1 = non_white_indices[0]
        index2 = non_white_indices[1]
        
        # Determine the color (assuming they are the same, take from the first)
        color = grid_np[index1]
        
        # Ensure index1 is the minimum and index2 is the maximum
        min_idx = min(index1, index2)
        max_idx = max(index1, index2)
        
        return min_idx, max_idx, color
    else:
        # Handle cases with 0, 1, or more than 2 non-white pixels
        # Based on the problem description and examples, this implies no transformation
        return None, None, None

def transform(input_grid):
    """
    Transforms the input grid by filling the gap between two marker pixels.

    Args:
        input_grid (list): A list of integers representing the 1D input grid.

    Returns:
        list: A list of integers representing the transformed grid.
    """
    # Convert input list to a numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)

    # Find the marker pixels' indices and color
    min_idx, max_idx, color = find_markers(grid_np)

    # If markers weren't found according to the rule (exactly two non-white),
    # return the original grid unchanged (as a list).
    if min_idx is None:
        return input_grid[:] # Return a copy

    # Create a copy of the grid to modify
    output_grid_np = grid_np.copy()

    # Fill the gap between the markers (exclusive of markers themselves)
    # The slice [min_idx + 1 : max_idx] correctly selects indices
    # from min_idx + 1 up to (but not including) max_idx.
    # Only fill if there is actually a gap (i.e., max_idx > min_idx + 1)
    if max_idx > min_idx + 1:
        output_grid_np[min_idx + 1 : max_idx] = color

    # Convert the modified numpy array back to a list for the output
    return output_grid_np.tolist()