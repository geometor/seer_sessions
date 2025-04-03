"""
Transformation Rule:
1. Handle potential input format variations: If the input is a list containing a single list (e.g., [[0, 0, 4,...]]), extract the inner list.
2. Identify the contiguous segment of non-white pixels (colors > 0) within the input row.
3. Within this segment, identify the 'singleton' color (appears once) and the 'repeated' color (appears multiple times consecutively).
4. Swap the position of the singleton pixel with the block of repeated color pixels.
   - If the singleton is at the start of the segment, move it to the end, placing the repeated block first.
   - If the singleton is at the end of the segment, move it to the start, placing the singleton first.
5. Keep the surrounding white pixels (color 0) unchanged.
6. Return the modified row as a list.
"""

import numpy as np
from collections import Counter
import copy # Used for deep copying if needed, though numpy copy is sufficient here

def find_non_white_segment_indices(grid_1d):
    """
    Finds the start and end indices of the first contiguous non-white segment
    in a 1D list or NumPy array.

    Args:
        grid_1d: A 1D list or NumPy array representing a row of pixels.

    Returns:
        A tuple (start_index, end_index) if a segment is found,
        otherwise (None, None).
    """
    start_index = -1
    end_index = -1
    # Find the first non-zero pixel for the start index
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            start_index = i
            break
    # If no non-zero pixel found, return None
    if start_index == -1:
        return None, None

    # Find the last non-zero pixel for the end index
    for i in range(len(grid_1d) - 1, start_index - 1, -1):
         if grid_1d[i] != 0:
             # Check if the segment is contiguous
             is_contiguous = True
             for j in range(start_index, i + 1):
                 if grid_1d[j] == 0:
                     is_contiguous = False
                     break # Found a zero within the potential segment
             if is_contiguous:
                 end_index = i
                 break # Found the last non-zero of a contiguous block
             else:
                 # If not contiguous here, it means we encountered a zero.
                 # We need to reset the search for the end index from before the zero.
                 # However, the current logic implicitly handles finding the *first* contiguous block.
                 # If the requirement was *any* such block, logic would need adjustment.
                 # For this specific task structure, the first non-zero and last non-zero
                 # correctly define the single segment seen in examples.
                 pass # Continue loop backwards to find the true end of the first segment.


    # The examples show only one segment, so finding the first non-zero (start_idx)
    # and the last non-zero (end_idx) is sufficient, assuming contiguity. Let's refine.
    start_index = -1
    end_index = -1
    in_segment = False
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            if not in_segment:
                start_index = i
                in_segment = True
            end_index = i # Keep updating end_index as long as we see non-zero
        elif pixel == 0 and in_segment:
            # We found a zero after starting a segment, so the segment ended at i-1
            # Since examples only show one segment, we can break here.
             break

    if start_index != -1:
        return start_index, end_index
    else:
        return None, None # No non-white segment found


def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.

    Args:
        input_grid: A list or list-of-lists representing the input grid.
                    Expected to contain a single row for this task.

    Returns:
        A list representing the transformed row.
    """

    # 1. Handle potential input format variations and ensure 1D numpy array
    if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
        # Input is likely [[...]], extract the inner list
        grid_1d_list = input_grid[0]
    elif isinstance(input_grid, list):
         # Input is likely already [...]
         grid_1d_list = input_grid
    else:
         # Try converting directly, might raise error for unexpected formats
         try:
            grid_1d_list = list(input_grid) # Fallback attempt
         except TypeError:
              # Handle error state - return input or raise specific error?
              # For ARC, often best to return input unchanged if format is wrong.
              return copy.deepcopy(input_grid) # Return original if format unclear


    grid_1d = np.array(grid_1d_list)

    # Ensure it's actually 1D after conversion
    if grid_1d.ndim != 1:
         # If it became 2D+, something is wrong, return original
         # This shouldn't happen with the checks above, but safety first.
         return grid_1d_list # Return the list version

    # Initialize output_grid as a copy
    output_grid = grid_1d.copy()

    # 2. Find the non-white segment indices
    start_idx, end_idx = find_non_white_segment_indices(grid_1d)

    # If no non-white segment exists or it's too small, return the original grid copy
    if start_idx is None or (end_idx - start_idx + 1) < 2:
        return output_grid.tolist() # Return as list

    # 3. Extract the segment and analyze its colors
    segment = grid_1d[start_idx : end_idx + 1]
    segment_len = len(segment)

    color_counts = Counter(segment)

    singleton_color = None
    repeated_color = None
    valid_segment = True

    # Check for exactly one singleton and one repeated color
    if len(color_counts) != 2:
        valid_segment = False
    else:
        found_singleton = False
        found_repeated = False
        for color, count in color_counts.items():
            if count == 1:
                if found_singleton: # Found more than one singleton
                    valid_segment = False
                    break
                singleton_color = color
                found_singleton = True
            elif count > 1:
                 if found_repeated: # Found more than one repeated color
                     valid_segment = False
                     break
                 repeated_color = color
                 found_repeated = True
            else: # count is 0? Should not happen with Counter on segment
                 valid_segment = False
                 break
        if not (found_singleton and found_repeated):
             valid_segment = False

    # If the segment doesn't fit the pattern, return original
    if not valid_segment:
        return output_grid.tolist()

    # 4. Determine position of singleton and construct the transformed segment
    transformed_segment = np.zeros_like(segment)

    if segment[0] == singleton_color:
        # Singleton was at the start, move it to the end
        # Place repeated block first
        transformed_segment[0 : segment_len - 1] = repeated_color
        # Place singleton at the end
        transformed_segment[segment_len - 1] = singleton_color
    elif segment[-1] == singleton_color:
        # Singleton was at the end, move it to the start
        # Place singleton at the start
        transformed_segment[0] = singleton_color
        # Place repeated block after
        transformed_segment[1 : segment_len] = repeated_color
    else:
        # Singleton is in the middle - this case is not handled by the examples/rule. Return original.
        return output_grid.tolist()

    # 5. Place the transformed segment back into the output grid
    output_grid[start_idx : end_idx + 1] = transformed_segment

    # 6. Return the result as a list
    return output_grid.tolist()