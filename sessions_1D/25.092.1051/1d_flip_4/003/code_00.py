import collections
import numpy as np # numpy might be useful, though list operations suffice here

"""
Transforms a single-row grid by finding a contiguous segment of non-white pixels. 
Within this segment, identifies a single pixel of one color and a contiguous block 
of pixels of another color, where the single pixel is at one end of the segment. 
Swaps the positions of the single pixel and the block within the segment's 
original boundaries, leaving surrounding white pixels unchanged. Returns the
transformed grid. If the input doesn't match the expected structure (single row, 
valid segment), the original input grid is returned.
"""

def find_non_white_segment(row):
    """
    Finds the start and end indices of the first contiguous non-white segment.

    Args:
        row: A list of integers representing a row.

    Returns:
        A tuple (start_index, end_index) or None if no segment found.
        end_index is exclusive (suitable for slicing).
    """
    start_index = -1
    end_index = -1
    in_segment = False
    for i, pixel in enumerate(row):
        if pixel != 0 and not in_segment:
            start_index = i
            in_segment = True
        elif pixel == 0 and in_segment:
            end_index = i
            break # Found the end of the first segment
            
    # Handle case where segment goes to the end of the row
    if in_segment and end_index == -1:
        end_index = len(row)

    if start_index != -1:
        # Ensure start_index < end_index (segment has length > 0)
        if start_index < end_index:
             return start_index, end_index
        else: # Should not happen if logic is correct, but good to handle
             return None
    else:
        return None

def analyze_segment(segment):
    """
    Analyzes a segment to find the single pixel's color/index and the block's color.

    Args:
        segment: A list of non-white integers representing the segment.

    Returns:
        A tuple (single_pixel_color, block_color, single_pixel_index_relative) 
        or None if the segment doesn't match the expected structure (one unique 
        color appearing once at either end, one repeated color making up the rest).
        single_pixel_index_relative is 0 if at the start, len(segment)-1 if at the end.
    """
    if not segment or len(segment) < 2: # Need at least two pixels for swap
        return None

    counts = collections.Counter(segment)
    
    # Expect exactly two distinct non-white colors
    if len(counts) != 2:
        return None

    single_pixel_color = None
    block_color = None
    
    # Identify the single and block colors based on counts
    for color, count in counts.items():
        if count == 1:
            single_pixel_color = color
        elif count > 1:
            block_color = color
        # If count is not 1 or >1 (e.g., 0, negative?), something is wrong.
        # This shouldn't happen with Counter on a non-empty list.

    # Check if we successfully identified both types
    if single_pixel_color is None or block_color is None:
        return None # Didn't find one of each type

    # Verify the single pixel is at one of the ends
    single_pixel_index_relative = -1
    if segment[0] == single_pixel_color:
        # Check if the rest is the block color
        if all(p == block_color for p in segment[1:]):
             single_pixel_index_relative = 0
        else: # Single color is at start, but rest isn't a uniform block
             return None
    elif segment[-1] == single_pixel_color:
         # Check if the rest is the block color
        if all(p == block_color for p in segment[:-1]):
             single_pixel_index_relative = len(segment) - 1
        else: # Single color is at end, but rest isn't a uniform block
             return None
    else:
        # Single pixel color exists but is not at either end
        return None 
        
    return single_pixel_color, block_color, single_pixel_index_relative


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid (expected 1 row).
                    Can also be a NumPy array internally from the framework.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert potential NumPy array row to list for consistency
    # and check if it's a single row grid
    try:
        if isinstance(input_grid, np.ndarray):
            if input_grid.ndim != 2 or input_grid.shape[0] != 1:
                 # Return input unchanged if not a single row 2D array
                 return input_grid.tolist() if isinstance(input_grid, np.ndarray) else input_grid
            input_row = input_grid[0].tolist()
        elif isinstance(input_grid, list):
             if len(input_grid) != 1 or not isinstance(input_grid[0], list):
                 # Return input unchanged if not list containing one list
                 return input_grid
             input_row = list(input_grid[0]) # Ensure it's a mutable list copy
        else:
             # Unexpected input type
             return input_grid # Or raise an error? Returning seems safer for ARC.

    except Exception: # Catch potential errors during conversion/checking
        return input_grid # Return original if any issue arises


    # Make a copy of the input row to modify for the output
    output_row = list(input_row) # Ensure it's a distinct copy

    # 1. Identify the contiguous sequence of non-white pixels
    segment_info = find_non_white_segment(input_row)

    if not segment_info:
        # No non-white segment found, return original grid format
        return [input_row] # Return as list of lists

    start_index, end_index = segment_info
    
    # Ensure indices are valid before slicing
    if start_index < 0 or end_index > len(input_row) or start_index >= end_index:
         return [input_row] # Invalid segment indices

    segment = input_row[start_index:end_index]
    
    # Check if segment is unexpectedly empty (should be caught by find_non_white_segment)
    if not segment:
         return [input_row]

    # 2. Analyze the segment to find the single pixel and the block
    analysis_result = analyze_segment(segment)

    if not analysis_result:
        # Segment doesn't match expected structure, return original grid format
        return [input_row]
        
    single_pixel_color, block_color, single_pixel_index_relative = analysis_result
    block_length = len(segment) - 1

    # 3. Create the new segment with swapped order
    new_segment = []
    # Check if the single pixel was originally at the start or end (relative index)
    if single_pixel_index_relative == 0:
        # Original order: Single, Block...
        # New order: Block..., Single
        new_segment.extend([block_color] * block_length)
        new_segment.append(single_pixel_color)
    elif single_pixel_index_relative == len(segment) - 1:
        # Original order: Block..., Single
        # New order: Single, Block...
        new_segment.append(single_pixel_color)
        new_segment.extend([block_color] * block_length)
    else:
        # This case should be prevented by analyze_segment, but as a safeguard:
        return [input_row] # Return original grid format

    # 4 & 5. Place the new segment into the output row copy
    # Ensure the new segment has the correct length before assignment
    if len(new_segment) == len(segment):
        output_row[start_index:end_index] = new_segment
    else:
        # Length mismatch indicates an error in logic, return original
        return [input_row]

    # 6. Surrounding white pixels are already preserved in the output_row copy.
    
    # 7. Return the transformed row in the expected grid format (list of lists)
    return [output_row]