import numpy as np

"""
Identifies a contiguous segment of a single color (C, not white-0 or maroon-9) and a single target pixel (maroon-9) in a 1D input grid.
Fills the gap of background pixels (white-0) between the segment and the target pixel with the segment's color C.
"""

def find_segment(row):
    """
    Finds the first contiguous segment of a single color C (not 0 or 9) in the row.

    Args:
        row (np.array): The 1D input array.

    Returns:
        tuple: (segment_color, start_index, end_index) or (None, -1, -1) if not found.
    """
    segment_color = -1
    start_index = -1
    end_index = -1
    in_segment = False
    
    for i, pixel in enumerate(row):
        # Check if pixel is a potential segment color
        if pixel != 0 and pixel != 9:
            if not in_segment:
                # Start of a new segment
                segment_color = pixel
                start_index = i
                end_index = i # Initialize end index
                in_segment = True
            elif in_segment and pixel == segment_color:
                # Continuation of the current segment
                end_index = i # Update end index
            elif in_segment and pixel != segment_color:
                 # Found a different color, the first segment ended before this pixel
                 # Since we only care about the first segment found, we can stop.
                 break 
        elif in_segment:
            # Hit a 0 or 9, the segment ended before this pixel.
            # Since we only care about the first segment found, we can stop.
            break
            
    if start_index != -1:
        return segment_color, start_index, end_index
    else:
        # No segment found (should not happen based on task description)
        return None, -1, -1

def transform(input_grid):
    """
    Fills the gap between a colored segment and a target maroon pixel with the segment's color.

    Args:
        input_grid (list of lists): A 2D list representing the grid, expected to be 1xN.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input grid (assumed 1xN) to a 1D numpy array
    input_row = np.array(input_grid[0])
    
    # Create a copy to modify for the output
    output_row = input_row.copy()
    
    # --- Locate Key Elements ---
    
    # Find the target pixel (maroon, color 9)
    # Assumes exactly one target pixel exists based on examples
    target_indices = np.where(input_row == 9)[0]
    if len(target_indices) == 0:
        # Handle case where target is missing (though not expected)
        return [output_row.tolist()] 
    target_index = target_indices[0]

    # Find the colored segment (not 0 or 9)
    segment_color, start_index, end_index = find_segment(input_row)

    if segment_color is None:
        # Handle case where segment is missing (though not expected)
        return [output_row.tolist()]

    # --- Determine Fill Range ---
    
    # Check if the target is to the right of the segment
    if target_index > end_index:
        # The gap is between the end of the segment and the target pixel
        fill_start = end_index + 1
        fill_end = target_index # Exclusive index for slicing
        
        # Fill the gap in the output row with the segment color
        # Only fill if there's actually a gap (fill_start < fill_end)
        if fill_start < fill_end:
            output_row[fill_start:fill_end] = segment_color
            
    # Check if the target is to the left of the segment
    elif target_index < start_index:
        # The gap is between the target pixel and the start of the segment
        fill_start = target_index + 1
        fill_end = start_index # Exclusive index for slicing
        
        # Fill the gap in the output row with the segment color
        # Only fill if there's actually a gap (fill_start < fill_end)
        if fill_start < fill_end:
             output_row[fill_start:fill_end] = segment_color

    # --- Return Result ---
    
    # Convert the modified 1D numpy array back to the 1xN list of lists format
    return [output_row.tolist()]