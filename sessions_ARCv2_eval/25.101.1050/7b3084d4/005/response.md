```python
import numpy as np
import math
from typing import List, Tuple, Dict

"""
The transformation rule rearranges the non-background pixels (colors 1-9) from the input grid into a square output grid.

1.  Count the total number 'N' of non-background pixels in the input grid.
2.  Calculate the side length 'S' of the square output grid, where S = sqrt(N). It is assumed N is always a perfect square based on the examples.
3.  Find the unique gray pixel (color 5), which serves as an anchor.
4.  Create a 1D sequence of pixel values:
    a. The first element is always 5 (the anchor color).
    b. The remaining N-1 elements are the other non-background pixel values from the input grid.
    c. The specific order in which these N-1 pixels are collected is crucial but not definitively determined from the examples. A placeholder ordering (e.g., row-major within the bounding box) will be used, acknowledging this uncertainty.
5.  Reshape this 1D sequence of N pixels into an S x S grid. This grid is the final output.
"""


def _find_anchor(grid: np.ndarray) -> Tuple[int, int] | None:
    """Finds the coordinates of the unique gray pixel (color 5)."""
    anchor_coords = np.argwhere(grid == 5)
    if anchor_coords.shape[0] == 1:
        return tuple(anchor_coords[0])
    elif anchor_coords.shape[0] == 0:
        print("Warning: No anchor pixel (color 5) found.")
        return None
    else:
        print("Warning: Multiple anchor pixels (color 5) found. Using the first one.")
        return tuple(anchor_coords[0])

def _find_bounding_box(grid: np.ndarray) -> Tuple[int, int, int, int] | None:
    """Finds the minimal bounding box containing all non-zero elements."""
    non_zero_coords = np.argwhere(grid != 0)
    if non_zero_coords.size == 0:
        return None
    min_row = non_zero_coords[:, 0].min()
    max_row = non_zero_coords[:, 0].max()
    min_col = non_zero_coords[:, 1].min()
    max_col = non_zero_coords[:, 1].max()
    return min_row, max_row, min_col, max_col

def _collect_pixels_ordered(grid: np.ndarray, anchor_pos: Tuple[int, int]) -> List[int]:
    """
    Collects non-background pixels, starting with the anchor, 
    followed by others in a specific (currently placeholder) order.
    """
    
    # Find all non-zero coordinates and their values
    non_zero_coords = np.argwhere(grid != 0)
    non_zero_values = grid[non_zero_coords[:, 0], non_zero_coords[:, 1]]
    
    # Create a list of tuples: (value, row, col)
    pixel_data = list(zip(non_zero_values, non_zero_coords[:, 0], non_zero_coords[:, 1]))
    
    # Find the anchor pixel data
    anchor_pixel_data = None
    other_pixels_data = []
    for val, r, c in pixel_data:
        if (r, c) == anchor_pos:
            anchor_pixel_data = val # Should be 5
        else:
            other_pixels_data.append((val, r, c))
            
    if anchor_pixel_data is None:
         # Should not happen if anchor_pos was found correctly
         print("Error: Anchor pixel not found in non_zero list.")
         return [] 
         
    # --- Placeholder Ordering ---
    # Sort remaining pixels by row, then column (row-major within the full grid)
    # This is the part that needs refinement based on the true transformation rule.
    other_pixels_data.sort(key=lambda x: (x[1], x[2])) 
    
    # Extract just the values in the determined order
    ordered_values = [anchor_pixel_data] + [p[0] for p in other_pixels_data]
    
    return ordered_values

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by rearranging non-background pixels into a square grid,
    anchored by the gray pixel (5).
    """
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Count non-background pixels
    non_zero_coords = np.argwhere(input_array != 0)
    num_non_zero = non_zero_coords.shape[0]

    if num_non_zero == 0:
        return [] # Handle empty input

    # 2. Calculate output size S
    side_length_f = math.sqrt(num_non_zero)
    if side_length_f != int(side_length_f):
        print(f"Warning: Number of non-zero pixels ({num_non_zero}) is not a perfect square.")
        # Decide handling: error out, or proceed with floor/ceil? Examples suggest it's always square.
        return [] # Return empty based on assumption violation
    side_length = int(side_length_f)

    # 3. Find the anchor pixel (color 5)
    anchor_pos = _find_anchor(input_array)
    if anchor_pos is None:
        print("Error: Anchor pixel (5) required but not found.")
        return [] # Cannot proceed without anchor

    # 4. Collect non-background pixels in a specific order (anchor first)
    # NOTE: The ordering of non-anchor pixels is the critical unknown part.
    # Using a placeholder order (row-major scan of the grid) for now.
    pixel_sequence = _collect_pixels_ordered(input_array, anchor_pos)

    if len(pixel_sequence) != num_non_zero:
        print(f"Error: Collected pixel count ({len(pixel_sequence)}) mismatches expected ({num_non_zero}).")
        return []

    # 5. Reshape the sequence into the S x S output grid
    try:
        output_array = np.array(pixel_sequence).reshape((side_length, side_length))
    except ValueError as e:
        print(f"Error during reshape: {e}. Sequence length {len(pixel_sequence)}, Target shape ({side_length}, {side_length})")
        return []
        
    # Convert final numpy array back to list of lists
    output_grid = output_array.tolist()

    return output_grid
```