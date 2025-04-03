import copy
# Using lists for 1D representation, numpy not strictly necessary for this task
# import numpy as np 

"""
Transformation Rule:
Identify a specific pattern within the 1D input grid: a non-white pixel ('marker') 
immediately followed by a sequence of one or more identical non-white pixels 
('sequence'), where the marker's color differs from the sequence's color. 
The transformation involves swapping the order of the marker and the sequence 
within the block they occupy. Specifically, in the output grid, the sequence 
is placed first, starting at the original marker's position, and is immediately 
followed by the marker pixel. All other pixels (background) remain unchanged.
"""

def find_marker_and_sequence(grid_1d):
    """
    Scans the 1D grid to find the marker pixel and the adjacent sequence.

    Args:
        grid_1d: A list of integers representing the 1D grid.

    Returns:
        A tuple (marker_idx, marker_color, sequence_color, seq_start_idx, seq_end_idx) 
        if the pattern is found, otherwise None.
        - marker_idx: index of the marker pixel.
        - marker_color: color value of the marker pixel.
        - sequence_color: color value of the sequence pixels.
        - seq_start_idx: starting index of the sequence (marker_idx + 1).
        - seq_end_idx: ending index of the sequence.
    """
    # Iterate through the grid, looking for the start of the pattern
    # Stop one element early as we need to look at grid_1d[i+1]
    for i in range(len(grid_1d) - 1):
        marker_candidate = grid_1d[i]
        sequence_start_candidate = grid_1d[i+1]

        # Check for the pattern conditions:
        # 1. Marker is not background (0)
        # 2. Sequence start is not background (0)
        # 3. Marker color is different from sequence start color
        if marker_candidate != 0 and sequence_start_candidate != 0 and marker_candidate != sequence_start_candidate:
            # Found a potential pattern start
            marker_idx = i
            marker_color = marker_candidate
            sequence_color = sequence_start_candidate
            seq_start_idx = i + 1
            seq_end_idx = seq_start_idx # Sequence must have at least one pixel

            # Extend the sequence end index as long as the color matches and we are within bounds
            # Start checking from the element *after* the sequence start candidate
            while seq_end_idx + 1 < len(grid_1d) and grid_1d[seq_end_idx + 1] == sequence_color:
                seq_end_idx += 1
            
            # Pattern found, return its details
            return marker_idx, marker_color, sequence_color, seq_start_idx, seq_end_idx

    # If the loop finishes without finding the pattern
    return None

def transform(input_grid):
    """
    Applies the marker-sequence swap transformation to the input grid.
    
    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Initialize output_grid as a deep copy to avoid modifying the input
    output_grid = copy.deepcopy(input_grid)

    # Find the marker and sequence details using the helper function
    pattern_details = find_marker_and_sequence(input_grid)

    # If the required pattern is not found in the input grid, return the unmodified copy.
    if pattern_details is None:
        return output_grid # Return the copy

    # Extract details from the found pattern
    marker_idx, marker_color, sequence_color, seq_start_idx, seq_end_idx = pattern_details
    
    # Calculate the length of the sequence
    # sequence_length = length of sequence block
    sequence_length = seq_end_idx - seq_start_idx + 1

    # Perform the transformation by modifying the output grid:
    # The transformation happens within the indices [marker_idx, seq_end_idx]
    
    # 1. Place the sequence pixels starting at the original marker's position.
    #    Iterate for the length of the sequence.
    for i in range(sequence_length):
        # The position in the output grid is the original marker's start index 
        # plus the offset within the sequence (i).
        output_grid[marker_idx + i] = sequence_color
        
    # 2. Place the marker color immediately after the newly placed sequence.
    #    The new position for the marker is the original marker's start index 
    #    plus the length of the sequence. This corresponds to the original 
    #    seq_end_idx position.
    new_marker_idx = marker_idx + sequence_length
    
    # Ensure the calculated new marker index is within the grid bounds before writing.
    # (Based on examples, this seems guaranteed, but good practice to check).
    if new_marker_idx < len(output_grid):
         output_grid[new_marker_idx] = marker_color
    # If new_marker_idx is out of bounds (shouldn't happen based on examples), 
    # the marker effectively disappears off the end, which might be wrong but 
    # adheres strictly to the placement logic.
         
    # The background pixels remain untouched as we only overwrite the specific
    # positions occupied by the original marker and sequence block.

    return output_grid