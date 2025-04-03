import numpy as np
from collections import Counter

"""
Identifies a contiguous block of non-zero colored pixels within a 1D input array (represented as a single row grid). 
This block contains exactly two distinct non-zero colors: one appearing as a single pixel and the other as a contiguous sub-block. 
The transformation swaps the positions of the single pixel and the contiguous sub-block within this identified region, leaving the surrounding zero (white) pixels unchanged.
"""

def find_active_region(row):
    """Finds the start and end indices and content of the non-zero region."""
    non_zero_indices = [i for i, x in enumerate(row) if x != 0]
    if not non_zero_indices:
        return None, None, None  # No active region found
    
    start_index = min(non_zero_indices)
    end_index = max(non_zero_indices)
    
    # Check for contiguity (optional but good practice)
    if len(non_zero_indices) != (end_index - start_index + 1):
        # This indicates gaps of zeros within the supposed active region,
        # which contradicts the problem description's examples.
        # Handle as an error or unexpected case if necessary.
        # For now, we'll proceed assuming contiguity based on examples.
        pass 
        
    active_segment = row[start_index : end_index + 1]
    return start_index, end_index, active_segment

def transform(input_grid):
    """
    Transforms the input grid by swapping a single pixel and a block of pixels 
    within the contiguous non-zero region of the single row.
    
    Args:
        input_grid (list of lists): A grid representing the input state. 
                                     Expected to have a single row for this task.

    Returns:
        list of lists: The transformed grid.
    """
    # Ensure input is treated as a NumPy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Assuming the relevant data is always in the first (and only) row
    if input_array.shape[0] != 1:
        # Handle unexpected input dimensions if necessary
        # For this specific task based on examples, we expect 1 row.
        # Returning input as is or raising error might be options.
        print("Warning: Expected input grid with a single row.")
        # Attempt to process the first row anyway
        # return input_grid # Or raise ValueError("Input must be a 1xN grid")
        
    row = list(input_array[0]) # Work with the first row as a list

    # 1. Identify the Active Region
    start_index, end_index, active_segment = find_active_region(row)

    # If no active region, return the original grid
    if active_segment is None:
        return input_grid 

    # 2. Identify Objects within the Active Region
    color_counts = Counter(c for c in active_segment if c != 0)
    
    # Validate the composition (exactly two non-zero colors)
    if len(color_counts) != 2:
        print(f"Warning: Active region {active_segment} does not contain exactly two non-zero colors.")
        return input_grid # Return original if structure is unexpected

    single_pixel_color = None
    block_color = None
    for color, count in color_counts.items():
        if count == 1:
            single_pixel_color = color
        else:
            block_color = color
            block_count = count # Store the expected count for the block

    # Validate identification (one single, one block)
    if single_pixel_color is None or block_color is None:
         print(f"Warning: Active region {active_segment} does not contain one single pixel and one block.")
         return input_grid # Return original

    # 3. Determine Order & 4. Perform Swap
    # Find the index of the single pixel within the active segment
    try:
        single_pixel_index_in_segment = active_segment.index(single_pixel_color)
    except ValueError:
         # Should not happen if previous checks passed, but good practice
         print(f"Error: Could not find single pixel color {single_pixel_color} in segment {active_segment}.")
         return input_grid

    swapped_active_segment = []
    # Create the block first
    block = [block_color] * block_count
    
    # Check if the single pixel was at the beginning or end
    if single_pixel_index_in_segment == 0:
        # Single pixel was first, put block first in output
        swapped_active_segment.extend(block)
        swapped_active_segment.append(single_pixel_color)
    elif single_pixel_index_in_segment == len(active_segment) - 1:
         # Single pixel was last, put it first in output
        swapped_active_segment.append(single_pixel_color)
        swapped_active_segment.extend(block)
    else:
        # This case (single pixel in the middle) is not covered by examples
        # or the description of a single pixel and a *contiguous* block.
        print(f"Warning: Single pixel {single_pixel_color} found in the middle of the active segment {active_segment}. Unexpected.")
        return input_grid

    # 5. Construct Output Array
    output_row = list(row) # Create a mutable copy
    output_row[start_index : end_index + 1] = swapped_active_segment
    
    # Convert back to the required grid format (list of lists)
    output_grid = [output_row]

    return output_grid