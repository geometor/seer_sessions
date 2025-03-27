```python
import numpy as np

# Color constants
AZURE = 8
WHITE = 0
ORANGE = 7 # Note: ORANGE was in the previous code but seems irrelevant now. Keeping for potential future debugging/comparison if needed.


def _find_horizontal_azure_pairs(input_array):
    """Finds all horizontally adjacent pairs of Azure pixels."""
    pairs = []
    H, W = input_array.shape
    for r in range(H):
        for c in range(W - 1): # Iterate up to W-2 to check c+1
            if input_array[r, c] == AZURE and input_array[r, c+1] == AZURE:
                pairs.append(((r, c), (r, c+1)))
    return pairs

def _find_vertical_azure_pairs(input_array):
    """Finds all vertically adjacent pairs of Azure pixels."""
    pairs = []
    H, W = input_array.shape
    for r in range(H - 1): # Iterate up to H-2 to check r+1
        for c in range(W):
            if input_array[r, c] == AZURE and input_array[r+1, c] == AZURE:
                pairs.append(((r, c), (r+1, c)))
    return pairs

def transform(input_grid):
    """
    Transforms the input grid based on adjacent pairs of Azure (8) pixels.

    1. Finds all horizontally adjacent Azure pairs ((r, c), (r, c+1)).
       - For each pair, places two White (0) markers at (r, W-2) and (r, W-1), if W >= 2.
    2. Finds all vertically adjacent Azure pairs ((r, c), (r+1, c)).
       - Stores the coordinates (r, c) of the top pixel of each vertical pair.
       - For each pair:
         - Places two White (0) markers at (H-2, c) and (H-1, c), if H >= 2.
         - Copies Azure pixels from row 'r' to row 'r+1', *unless* the Azure pixel in row 'r'
           is itself the top part of *any* vertical pair.
    3. The original Azure pairs remain Azure.
    4. Pixels not involved in marker placement or copying remain unchanged.
    """
    # Convert input list of lists to a numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output grid as a copy of the input
    output_array = np.copy(input_array)
    
    # Get grid dimensions
    H, W = input_array.shape

    # --- Process Horizontal Pairs ---
    horizontal_pairs = _find_horizontal_azure_pairs(input_array)
    for pair in horizontal_pairs:
        r, _ = pair[0] # Get the row index from the first pixel of the pair
        # Place White markers at the right edge of the row
        if W >= 2:
            output_array[r, W-2] = WHITE
            output_array[r, W-1] = WHITE
        # Note: If W=1, a horizontal pair cannot exist, so no special case needed.


    # --- Process Vertical Pairs ---
    vertical_pairs = _find_vertical_azure_pairs(input_array)

    # Create a set of coordinates for the top pixels of all vertical pairs
    # This is used to prevent copying these specific pixels downwards
    top_vertical_pair_pixels = set(pair[0] for pair in vertical_pairs)

    for pair in vertical_pairs:
        r, c = pair[0] # Top pixel coordinates (r, c)
        r_below, _ = pair[1] # Bottom pixel coordinates (r+1, c) - used implicitly in copy logic

        # Place White markers at the bottom edge of the column
        if H >= 2:
            output_array[H-2, c] = WHITE
            output_array[H-1, c] = WHITE
        # Note: If H=1, a vertical pair cannot exist.

        # Copy qualifying Azure pixels from row 'r' down to row 'r_below' (r+1)
        # Iterate through all columns in the *input* row 'r'
        for col_idx in range(W):
            # Check if the pixel in the input row 'r' is Azure
            if input_array[r, col_idx] == AZURE:
                # Check if this Azure pixel is NOT the top of any vertical pair
                if (r, col_idx) not in top_vertical_pair_pixels:
                    # Copy the Azure pixel down to the next row in the output
                     # Ensure r_below (which is r+1) is within grid bounds
                    if r_below < H:
                         output_array[r_below, col_idx] = AZURE

    # Convert the final numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```