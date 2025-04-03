import collections 
import numpy as np # Although lists are used, numpy might be useful for potential generalizations or if inputs are numpy arrays

"""
This transformation rearranges elements of a 1D input grid based on the positions 
of a background color (0), a unique marker color (7), and a single contiguous 
object block of another color.

The rule is to:
1. Identify the background color (0), marker color (7), and the object color 
   (the single color that is not 0 or 7).
2. Locate the contiguous block of the object color.
3. Find the index of the marker color (7).
4. Count the number of leading background pixels (L) at the start of the input.
5. Count the number of background pixels (N) immediately preceding the marker.
6. Count the number of background pixels (T) immediately following the marker.
7. Construct the output grid by concatenating:
    a. (L + N) background pixels.
    b. The object block.
    c. The marker pixel (7).
    d. T background pixels.
"""

# --- Helper Functions ---

def find_marker_index(grid, marker_color):
    """Finds the index of the first occurrence of the marker_color."""
    # Convert to list if it's a numpy array to use list.index()
    grid_list = list(grid) 
    try:
        return grid_list.index(marker_color)
    except ValueError:
        return -1 # Marker not found

def find_object_block(grid, background_color, marker_color):
    """Finds the contiguous block of the object color."""
    object_color = -1
    start_index = -1
    object_block_list = []

    # First pass to find the object color
    for pixel in grid:
        if pixel != background_color and pixel != marker_color:
            object_color = pixel
            break
    
    if object_color == -1:
        return [] # No object found

    # Second pass to find the block
    in_block = False
    for pixel in grid:
        if pixel == object_color:
            object_block_list.append(pixel)
            in_block = True
        elif in_block: 
            # Found the end of the block
            break 
            
    return object_block_list


def count_leading_background(grid, background_color):
    """Counts consecutive background pixels from the start of the grid."""
    count = 0
    for pixel in grid:
        if pixel == background_color:
            count += 1
        else:
            break
    return count

def count_preceding_marker_background(grid, marker_index, background_color):
    """Counts consecutive background pixels immediately before the marker index."""
    count = 0
    idx = marker_index - 1
    # Iterate backwards from the position just before the marker
    while idx >= 0 and grid[idx] == background_color:
        count += 1
        idx -= 1
    return count

def count_trailing_background(grid, marker_index, background_color):
    """Counts consecutive background pixels immediately after the marker index."""
    count = 0
    idx = marker_index + 1
    # Iterate forwards from the position just after the marker
    while idx < len(grid) and grid[idx] == background_color:
        count += 1
        idx += 1
    return count

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the rearrangement transformation to the input grid.

    Args:
        input_grid (list or numpy array): A 1D sequence of integers 
                                         representing the input grid.

    Returns:
        list: A list of integers representing the transformed 1D output grid.
    """
    
    # Ensure input is a list for consistent processing
    if isinstance(input_grid, np.ndarray):
        # Handle potential multi-dimensional arrays if needed, although examples are 1D
        if input_grid.ndim > 1:
             # Flatten if accidentally passed as 2D with one row/column
             input_list = input_grid.flatten().tolist()
        else:
             input_list = input_grid.tolist()
    else:
        input_list = list(input_grid) # Ensure it's a mutable list

    # Define constant colors
    background_color = 0
    marker_color = 7

    # Step 1 & 3: Identify marker and its index
    marker_index = find_marker_index(input_list, marker_color)
    if marker_index == -1:
         # Handle error: marker not found
         print("Error: Marker color (7) not found in input.")
         return [] 

    # Step 2: Find the object block
    object_block = find_object_block(input_list, background_color, marker_color)
    if not object_block:
         # Handle error: object not found
         print("Error: Object block not found in input.")
         return [] 

    # Step 4: Count leading background pixels (L)
    leading_bg_count = count_leading_background(input_list, background_color)

    # Step 5: Count background pixels immediately preceding the marker (N)
    preceding_marker_bg_count = count_preceding_marker_background(input_list, marker_index, background_color)

    # Step 6: Count background pixels immediately following the marker (T)
    # Note: The original logic seemed to just take *all* trailing background pixels,
    # let's re-evaluate based on example 3.
    # Example 3 Input:  0 8 8 8 8 8 8 8 8 8 8 8 8 0 0 7 0 0 0 0 0 0 
    # Example 3 Output: 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 7 0 0 0 0 0 0
    # L=1, N=2, T=6. Object = twelve 8s. Marker=7.
    # Output starts with L+N = 1+2=3 background pixels (0 0 0). Correct.
    # Then object block (twelve 8s). Correct.
    # Then marker (7). Correct.
    # Then T=6 background pixels (0 0 0 0 0 0). Correct.
    # The logic for counting *contiguous* trailing background seems correct.
    trailing_bg_count = count_trailing_background(input_list, marker_index, background_color)

    # Step 7: Construct the output grid
    output_grid = []

    # 7a. Add (L + N) background pixels
    total_leading_bg = leading_bg_count + preceding_marker_bg_count
    output_grid.extend([background_color] * total_leading_bg)

    # 7b. Add the object block
    output_grid.extend(object_block)

    # 7c. Add the marker pixel
    output_grid.append(marker_color)

    # 7d. Add T background pixels
    output_grid.extend([background_color] * trailing_bg_count)
    
    # Final check: Ensure output length matches input length if that's a constraint
    # In these examples, the length is preserved. If output is shorter due to calculation,
    # pad with background? Let's assume length preservation is desired if possible,
    # but the current logic naturally preserves the components.
    # Let's verify counts.
    # Example 1: L=0, N=2, T=2. Object=sixteen 1s. Marker=7.
    # Input:  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 | 1 0 | 0 7 | 0 0
    # Output: 0 0 | sixteen 1s | 7 | 0 0
    # L+N = 0+2 = 2 -> Correct. T = 2 -> Correct.
    
    # Example 2: L=0, N=2, T=3. Object=sixteen 3s. Marker=7.
    # Input:  3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 | 0 0 | 7 | 0 0 0
    # Output: 0 0 | sixteen 3s | 7 | 0 0 0
    # L+N = 0+2 = 2 -> Correct. T=3 -> Correct.

    # Example 3: L=1, N=2, T=6. Object=twelve 8s. Marker=7.
    # Input:  0 | 8 8 8 8 8 8 8 8 8 8 8 8 | 0 0 | 7 | 0 0 0 0 0 0
    # Output: 0 0 0 | twelve 8s | 7 | 0 0 0 0 0 0
    # L+N = 1+2 = 3 -> Correct. T=6 -> Correct.
    
    # The logic seems robust for the given examples.

    return output_grid