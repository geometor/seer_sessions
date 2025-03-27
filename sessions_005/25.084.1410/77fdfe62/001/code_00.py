import numpy as np

"""
Identify the rectangular subgrid ("inner grid") enclosed by a 1-pixel thick blue (1) frame, which is itself offset by 1 pixel from the input grid's edges.
Record the colors of the four corner pixels of the original input grid (Top-Left: C_TL, Top-Right: C_TR, Bottom-Left: C_BL, Bottom-Right: C_BR).
Create an output grid with the same dimensions as the inner grid.
Iterate through each pixel P at (r, c) in the inner grid:
- If P is white (0), the corresponding output grid pixel at (r, c) is white (0).
- If P is azure (8), determine its quadrant within the inner grid:
    - Top-Left Quadrant: Output pixel is C_TL.
    - Top-Right Quadrant: Output pixel is C_TR.
    - Bottom-Left Quadrant: Output pixel is C_BL.
    - Bottom-Right Quadrant: Output pixel is C_BR.
The quadrants are determined by dividing the inner grid at its vertical and horizontal midpoints. 
Specifically, for an inner grid of height H and width W:
- Top rows have indices r < (H+1)//2
- Bottom rows have indices r >= (H+1)//2
- Left columns have indices c < (W+1)//2
- Right columns have indices c >= (W+1)//2
Return the resulting output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on corner colors and inner grid contents.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_h, input_w = input_np.shape

    # Step 1: Identify the Inner Grid
    # The blue frame is at row 1, row input_h-2, col 1, col input_w-2
    # The inner grid is offset by one more pixel inwards
    inner_grid = input_np[2:input_h-2, 2:input_w-2]
    inner_h, inner_w = inner_grid.shape

    # Step 2: Identify Corner Colors
    c_tl = input_np[0, 0]
    c_tr = input_np[0, input_w - 1]
    c_bl = input_np[input_h - 1, 0]
    c_br = input_np[input_h - 1, input_w - 1]

    # Step 3: Initialize Output Grid
    output_grid = np.zeros((inner_h, inner_w), dtype=int)

    # Define quadrant boundaries
    # Rows < top_boundary are top, rows >= top_boundary are bottom
    # Cols < left_boundary are left, cols >= left_boundary are right
    top_boundary = (inner_h + 1) // 2
    left_boundary = (inner_w + 1) // 2

    # Step 4: Process Inner Grid Pixels
    for r in range(inner_h):
        for c in range(inner_w):
            pixel_value = inner_grid[r, c]

            if pixel_value == 0:
                # White pixels remain white (already initialized to 0)
                pass # output_grid[r, c] = 0
            elif pixel_value == 8:
                # Azure pixels are replaced based on quadrant
                is_top = r < top_boundary
                is_left = c < left_boundary

                if is_top and is_left:        # Top-Left quadrant
                    output_grid[r, c] = c_tl
                elif is_top and not is_left:  # Top-Right quadrant
                    output_grid[r, c] = c_tr
                elif not is_top and is_left:  # Bottom-Left quadrant
                    output_grid[r, c] = c_bl
                else:                         # Bottom-Right quadrant
                    output_grid[r, c] = c_br
            # Other pixel values in the inner grid (if any) are ignored, output remains 0

    # Step 5: Return Output
    # Convert numpy array back to list of lists
    return output_grid.tolist()