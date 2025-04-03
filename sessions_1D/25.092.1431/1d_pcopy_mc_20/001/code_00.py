import math
from collections import Counter

"""
Transforms a 1D input array (list of integers 0-9) based on contiguous sequences of non-zero colors (objects).
- Objects are sequences of identical non-zero colors. In the examples, objects have lengths of 1 or 3.
- Background is color 0 (white), forming gaps between objects.
- The transformation rules are:
    1. If an object has length 3, it remains unchanged, and its preceding gap of zeros also remains unchanged.
    2. If an object has length 1 (a single pixel), it is expanded to a length of 3 (repeating its color).
    3. The gap of zeros immediately preceding a single-pixel object is reduced. The amount of reduction is equal to the count of single-pixel objects encountered so far (including the current one). The gap length cannot be negative (minimum 0).
- The transformation proceeds sequentially from left to right.
"""

def transform(input_grid):
    """
    Applies the described transformation to a 1D input grid.

    Args:
        input_grid (list): A list of integers representing the input 1D grid.

    Returns:
        list: A list of integers representing the transformed 1D grid.
    """
    output_grid = []
    single_pixel_count = 0
    i = 0
    n = len(input_grid)

    while i < n:
        # Find the start of the current segment (either gap or object)
        start_index = i

        # Check if it's a gap (sequence of zeros)
        if input_grid[i] == 0:
            # Find the end of the gap
            while i < n and input_grid[i] == 0:
                i += 1
            current_gap_length = i - start_index

            # If this gap is followed by an object (i.e., we are not at the end)
            if i < n:
                # Look ahead to find the object length without consuming it yet
                object_start = i
                object_color = input_grid[i]
                object_end = i
                while object_end < n and input_grid[object_end] == object_color:
                    object_end += 1
                object_length = object_end - object_start

                # Decide gap length based on the upcoming object
                if object_length == 1:
                     # Gap precedes a single-pixel object, calculate reduction
                     # Note: single_pixel_count will be incremented *after* this gap calculation
                     #       when the object itself is processed. So we use count + 1 here.
                     reduction = single_pixel_count + 1
                     new_gap_length = max(0, current_gap_length - reduction)
                     output_grid.extend([0] * new_gap_length)
                elif object_length == 3:
                     # Gap precedes a three-pixel object, keep original length
                     output_grid.extend([0] * current_gap_length)
                else:
                     # Handle unexpected object lengths by keeping original gap
                     # (Based on examples, only 1 and 3 are expected)
                     output_grid.extend([0] * current_gap_length)

            else:
                 # This is a trailing gap, append as is
                 output_grid.extend([0] * current_gap_length)

        # Else, it's an object (sequence of non-zeros)
        else:
            object_color = input_grid[i]
            # Find the end of the object
            while i < n and input_grid[i] == object_color:
                i += 1
            object_length = i - start_index

            # Process the object based on its length
            if object_length == 1:
                # Increment the count for single-pixel objects found
                single_pixel_count += 1
                # Append the expanded object (3 times the color)
                output_grid.extend([object_color] * 3)
            elif object_length == 3:
                # Append the object as is
                output_grid.extend([object_color] * 3)
            else:
                # Handle unexpected lengths by appending the original object
                # (Based on examples, only 1 and 3 are expected)
                 output_grid.extend(input_grid[start_index:i])


    return output_grid
