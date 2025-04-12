```python
import numpy as np
import math
from typing import List, Tuple

"""
The transformation rule rearranges the non-background pixels (colors 1-9) from the input grid into a square output grid, anchored by the gray (5) pixel.

1.  Identify all non-background pixels (colors 1-9) in the input grid. Let 'N' be the total count of these pixels.
2.  Calculate the side length 'S' for the square output grid, where S = sqrt(N). (Based on the examples, 'N' will be a perfect square). The output grid will be S x S.
3.  Locate the unique gray pixel (color 5) in the input grid; let its coordinates be (anchor_row, anchor_col).
4.  Create an ordered list 'P' of pixel values, starting with the anchor color: P = [5].
5.  Gather the values of the other N-1 non-background pixels from the input grid.
6.  Append these N-1 pixel values to the list 'P' in a specific sequence. **This sequence is determined by an unknown rule related to the pixels' spatial positions relative to the anchor pixel (anchor_row, anchor_col).** Simple row-major scanning or direct relative position mapping does not produce the correct sequence. A placeholder ordering (row-major scan of the full grid) will be used here, acknowledging it's likely incorrect.
7.  Reshape the final list 'P' (containing N elements) into an S x S grid by filling the grid row by row, left to right.
8.  Return the resulting S x S grid.
"""


def _find_anchor(grid: np.ndarray) -> Tuple[int, int] | None:
    """Finds the coordinates of the unique gray pixel (color 5)."""
    anchor_coords = np.argwhere(grid == 5)
    if anchor_coords.shape[0] == 1:
        # Return the (row, col) tuple
        return tuple(anchor_coords[0])
    elif anchor_coords.shape[0] == 0:
        # Anchor not found
        return None
    else:
        # Multiple anchors found - problematic, return the first one based on example behavior
        # print("Warning: Multiple anchor pixels (color 5) found. Using the first one.")
        return tuple(anchor_coords[0])

def _collect_pixels_ordered(grid: np.ndarray, anchor_pos: Tuple[int, int]) -> List[int]:
    """
    Collects non-background pixels, starting with the anchor's value (5), 
    followed by others according to a specific ordering rule.
    
    *** Placeholder Implementation ***
    The ordering rule for non-anchor pixels is UNKNOWN based on the examples.
    This implementation uses a simple row-major scan of the entire grid
    as a placeholder, which is known to be INCORRECT for achieving the target outputs.
    """
    
    # Find coordinates and values of all non-zero pixels
    non_zero_coords = np.argwhere(grid != 0)
    
    # Store as (value, row, col) tuples
    pixel_data = []
    for r, c in non_zero_coords:
        pixel_data.append((grid[r, c], r, c))
        
    # Separate the anchor pixel from the others
    anchor_value = 5 # We expect the anchor to be 5
    other_pixels_data = []
    found_anchor_in_list = False
    for val, r, c in pixel_data:
        if (r, c) == anchor_pos:
            anchor_value = val # Confirm it's 5
            found_anchor_in_list = True
        else:
            other_pixels_data.append((val, r, c))
            
    if not found_anchor_in_list:
         # This case should ideally not happen if anchor_pos was valid
         # print("Error: Anchor position not found among non-zero pixels.")
         # Fallback: Find the value 5 anyway? Or return error.
         # For robustness, let's ensure 5 is first if it exists, regardless of position check failing.
         all_values = [p[0] for p in pixel_data]
         if 5 in all_values:
             anchor_value = 5
             other_values = [v for v in all_values if v != 5] # Simple value removal, might lose duplicates
             # A more robust way needed if duplicates of 5 exist AND anchor pos failed.
             # Let's stick to the primary path assuming anchor_pos is correct.
             return [] # Indicate error if anchor logic fails
         else:
            # print("Error: Anchor value 5 not found at all.")
            return []


    # *** Apply the Placeholder Ordering Rule ***
    # Sort the *other* pixels based on row, then column (simple grid scan)
    other_pixels_data.sort(key=lambda x: (x[1], x[2])) 
    
    # Construct the final sequence: anchor value first, then sorted other values
    ordered_values = [anchor_value] + [p[0] for p in other_pixels_data]
    
    return ordered_values

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid based on the described rearrangement rule.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # Step 1: Count non-background pixels (N)
    non_zero_mask = input_array != 0
    num_non_zero = np.count_nonzero(non_zero_mask)

    # Handle empty input
    if num_non_zero == 0:
        return [] 

    # Step 2: Calculate output size (S)
    side_length_f = math.sqrt(num_non_zero)
    if side_length_f != int(side_length_f):
        # Rule assumes N is a perfect square, based on examples.
        # If not, the rule is violated or incomplete. Return empty.
        # print(f"Error: Number of non-zero pixels ({num_non_zero}) is not a perfect square.")
        return [] 
    side_length = int(side_length_f)

    # Step 3: Find the anchor pixel (color 5)
    anchor_pos = _find_anchor(input_array)
    if anchor_pos is None:
        # Rule requires an anchor pixel. If missing, cannot proceed.
        # print("Error: Anchor pixel (5) required but not found.")
        return [] 

    # Step 4 & 6: Collect pixels in the specific (but unknown) order
    # Using the placeholder function which returns anchor first, then others row-major.
    pixel_sequence = _collect_pixels_ordered(input_array, anchor_pos)

    # Validation check
    if not pixel_sequence or len(pixel_sequence) != num_non_zero:
        # print(f"Error: Pixel collection failed or mismatch. Expected {num_non_zero}, got {len(pixel_sequence)}.")
        return []

    # Step 7: Reshape the sequence into the S x S output grid
    try:
        output_array = np.array(pixel_sequence).reshape((side_length, side_length))
    except ValueError as e:
        # This should not happen if N is a perfect square and sequence length matches N.
        # print(f"Error during reshape: {e}.")
        return []
        
    # Step 8: Convert final numpy array back to list of lists and return
    output_grid = output_array.tolist()

    return output_grid
```