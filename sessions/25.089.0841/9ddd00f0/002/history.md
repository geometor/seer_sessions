
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 0 8 8
0 8 0 8 0
```


**output:**
```
0 8 0 8 0
8 8 0 8 8
0 0 0 0 0
8 8 0 8 8
0 8 0 8 0
```


## train_2

**input:**
```
0 0 0 0 2 0 2 0 2 2 0
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 2 0 2 0 2 2 0
```


**output:**
```
0 2 2 0 2 0 2 0 2 2 0
2 2 2 0 2 2 2 0 2 2 2
2 2 2 0 2 2 2 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 2 2 2 0 2 2 2
0 2 2 0 2 0 2 0 2 2 0
2 2 2 0 2 2 2 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 2 2 2 0 2 2 2
2 2 2 0 2 2 2 0 2 2 2
0 2 2 0 2 0 2 0 2 2 0
```

```python
import numpy as np

def transform(input_grid):
    """
    Detects if the non-background pattern in the input grid is confined to one half 
    (top, bottom, left, or right) relative to the grid's center line(s). 
    If so, it reflects that half onto the opposite, empty half, overlaying the reflection 
    onto the original grid content.

    1. Identify the grid dimensions (height h, width w).
    2. Determine the background color (assumed to be 0).
    3. Locate all non-background pixels.
    4. Check if all non-background pixels lie exclusively in the top, bottom, left, or right half of the grid.
       - Halves are defined relative to the center row(s)/column(s).
       - For height h, top half is rows 0 to h//2 - 1, bottom half is rows h - h//2 to h - 1.
       - For width w, left half is columns 0 to w//2 - 1, right half is columns w - w//2 to w - 1.
    5. If the pattern is confined to one half:
       - Copy the pixels from that half.
       - Flip the copied section (vertically for top/bottom, horizontally for left/right).
       - Paste the flipped section onto the corresponding opposite half in the output grid.
    6. The original pattern remains in its location in the output grid.
    7. If the pattern is not confined to a single half, the output grid is identical to the input grid.
    """

    # Convert input to numpy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    h, w = input_array.shape
    
    # Define background color (assuming 0)
    bg_color = 0

    # Find coordinates of non-background pixels
    non_bg_coords = np.argwhere(input_array != bg_color)

    # If there are no non-background pixels, return the original grid
    if non_bg_coords.size == 0:
        return output_array.tolist()

    # Calculate half boundaries
    rows_in_half = h // 2
    cols_in_half = w // 2
    
    # Determine which halves contain non-background pixels
    in_top_half = np.any(non_bg_coords[:, 0] < rows_in_half)
    in_bottom_half = np.any(non_bg_coords[:, 0] >= h - rows_in_half)
    in_left_half = np.any(non_bg_coords[:, 1] < cols_in_half)
    in_right_half = np.any(non_bg_coords[:, 1] >= w - cols_in_half)

    # Perform vertical reflection if pattern is only in one vertical half
    if in_bottom_half and not in_top_half:
        # Pattern is only in the bottom half, reflect it to the top
        source_rows = input_array[h - rows_in_half : h, :]
        flipped_rows = np.flipud(source_rows)
        output_array[0 : rows_in_half, :] = flipped_rows
    elif in_top_half and not in_bottom_half:
        # Pattern is only in the top half, reflect it to the bottom
        source_rows = input_array[0 : rows_in_half, :]
        flipped_rows = np.flipud(source_rows)
        output_array[h - rows_in_half : h, :] = flipped_rows

    # Perform horizontal reflection if pattern is only in one horizontal half
    # Note: This assumes vertical reflection takes precedence if conditions for both are met,
    # or that only one type of reflection is needed per task example.
    # If horizontal reflection should happen independently, remove the `elif`.
    # Based on examples, only one reflection axis seems active. Let's assume vertical check first.
    # If no vertical reflection happened, check horizontal.
    
    # Re-check horizontal conditions if vertical reflection didn't occur (or adjust logic if both can happen)
    # For simplicity based on examples, let's assume only one reflection type applies per grid.
    # The code above handles vertical first. If vertical was done, we stop.
    # If no vertical reflection happened, check horizontal:
    
    vertical_reflection_done = (in_bottom_half and not in_top_half) or (in_top_half and not in_bottom_half)

    if not vertical_reflection_done:
        if in_right_half and not in_left_half:
            # Pattern is only in the right half, reflect it to the left
            source_cols = input_array[:, w - cols_in_half : w]
            flipped_cols = np.fliplr(source_cols)
            output_array[:, 0 : cols_in_half] = flipped_cols
        elif in_left_half and not in_right_half:
            # Pattern is only in the left half, reflect it to the right
            source_cols = input_array[:, 0 : cols_in_half]
            flipped_cols = np.fliplr(source_cols)
            output_array[:, w - cols_in_half : w] = flipped_cols

    # Convert the result back to a list of lists
    return output_array.tolist()
```
