import numpy as np
import collections

"""
Transformation Rule:
Identify the contiguous horizontal segment of non-white (non-zero) pixels in the input row. 
Within this segment, find the single pixel whose color is unique compared to the others. 
Move this unique pixel to the opposite end of the segment, shifting the other pixels 
(which all share the same repeated color) accordingly. Keep the surrounding white (zero) 
pixels and the colors within the segment unchanged. Return the modified grid.
"""

def find_segment_indices(row):
    """
    Finds the start and end indices of the first contiguous non-zero segment in a 1D array.

    Args:
        row: A 1D numpy array or list representing a row of pixels.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no segment is found.
    """
    start_index = -1
    end_index = -1
    in_segment = False
    for i, pixel in enumerate(row):
        if pixel != 0:
            if not in_segment:
                start_index = i
                in_segment = True
            end_index = i
        elif in_segment:
            # Found the end of the segment
            break 
            # Optimization: if we assume only one segment exists per row based on examples
            # we can break here. If multiple segments could exist and we only care about the
            # first one, this break is correct. If we need to process potentially multiple
            # segments, the logic would need extension. Based on examples, only one segment exists.
            
    # Handle case where segment goes to the end of the row
    if in_segment and end_index == -1:
         end_index = len(row) -1
         
    # Recalculate end_index if start was found but loop finished within segment
    if start_index != -1 and end_index < start_index:
         for i in range(start_index, len(row)):
             if row[i] != 0:
                 end_index = i
             else:
                 break # Stop at the first zero after start

    # Final check if only start was found but no non-zero followed
    if start_index != -1 and end_index < start_index :
         return -1, -1 # No valid segment found

    return start_index, end_index


def transform(input_grid):
    """
    Moves a unique colored pixel within a contiguous non-zero segment 
    to the opposite end of that segment in a 1-row grid.

    Args:
        input_grid: A numpy array, expected to be 2D with shape (1, N).

    Returns:
        A numpy array with the transformed row, same shape as input.
    """
    # Validate input shape - expect 2D array with 1 row
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Or handle other potential valid inputs if needed
        # For now, assume strict adherence to the observed pattern
        return input_grid 

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    input_row = output_grid[0] # Work directly on the row of the output grid copy

    # 1. Find the start and end indices of the non-white segment
    start, end = find_segment_indices(input_row)

    # 2. If no segment is found or segment is too small, return the original grid
    if start == -1 or (end - start + 1) < 2:
        return output_grid

    # 3. Extract the segment
    segment = input_row[start:end+1]
    segment_len = len(segment)

    # 4. Analyze segment colors
    color_counts = collections.Counter(segment)
    
    # 5. Check for the specific pattern: exactly two colors, one unique
    unique_color = -1
    repeated_color = -1
    if len(color_counts) == 2:
        for color, count in color_counts.items():
            if count == 1:
                unique_color = color
            else:
                repeated_color = color # Assumes the other color count > 1
    
    # 6. If the pattern doesn't match, return original
    if unique_color == -1 or repeated_color == -1 or color_counts[repeated_color] != segment_len - 1:
       return output_grid

    # 7. Determine current position of the unique pixel
    is_unique_at_start = (segment[0] == unique_color)
    is_unique_at_end = (segment[-1] == unique_color)

    # 8. If unique pixel is not at either end, return original (shouldn't happen based on examples)
    if not is_unique_at_start and not is_unique_at_end:
        return output_grid
        
    # 9. Construct the new segment
    new_segment = np.zeros(segment_len, dtype=input_row.dtype)
    num_repeated = segment_len - 1

    if is_unique_at_start:
        # Move unique pixel to the end
        new_segment[0:num_repeated] = repeated_color
        new_segment[num_repeated] = unique_color
    elif is_unique_at_end:
        # Move unique pixel to the start
        new_segment[0] = unique_color
        new_segment[1:segment_len] = repeated_color
        
    # 10. Replace the original segment with the new segment in the output row
    output_grid[0, start:end+1] = new_segment

    # 11. Return the modified grid
    return output_grid