```python
import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by identifying the two colors forming a checkerboard
    pattern in the top-left region, ignoring any border color, and generating an
    output grid of the same dimensions filled entirely with an inverted checkerboard
    pattern using those two colors.

    1. Determine the height (H) and width (W) of the input grid.
    2. Identify the color at the top-left corner (0,0) as color_1.
    3. Identify the adjacent color (at (0,1) or (1,0)) that is different from color_1
       as color_2. This assumes the checkerboard pattern starts immediately and
       is at least 2x2 or 1x2/2x1 in the relevant area.
    4. Create a new output grid with dimensions H x W.
    5. Iterate through each cell (row, col) of the output grid.
    6. If (row + col) is even, set the cell color to color_2 (the swapped color for the top-left).
    7. If (row + col) is odd, set the cell color to color_1 (the swapped color for the adjacent cell).
    8. Return the completed output grid.
    """
    
    # Convert input list of lists to a numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Determine the height (H) and width (W) of the input grid.
    H, W = input_array.shape
    
    # 2. Identify the color at the top-left corner (0,0) as color_1.
    color_1 = input_array[0, 0]
    
    # 3. Identify the adjacent color (at (0,1) or (1,0)) that is different from color_1 as color_2.
    # Check (0,1) first if width > 1
    if W > 1 and input_array[0, 1] != color_1:
        color_2 = input_array[0, 1]
    # Otherwise check (1,0) if height > 1
    elif H > 1 and input_array[1, 0] != color_1:
        color_2 = input_array[1, 0]
    # Handle edge case: 1x1 grid (output will be inverted, so color_2 is needed conceptually)
    # Or if the 2x2 block wasn't standard checkerboard (unlikely based on examples)
    # We need *some* second color. Let's search the first row/col further just in case.
    # Defaulting might be risky, but based on examples, the first adjacent different color is the one.
    # If grid is 1x1, this step isn't strictly necessary as logic below handles it, but let's define color_2 anyway if possible.
    # A truly 1x1 grid is ambiguous for finding color_2. The logic assumes color_2 exists.
    # If the grid is truly 1x1, color_2 won't be found here. The loop below will only use color_2 for cell (0,0).
    # Let's assume the problem guarantees at least two distinct colors used in the pattern area.
    # If grid is 1x1, what should color_2 be? The examples don't cover this.
    # The logic implies swapping color_1 with color_2. If color_2 doesn't exist, what do we swap with?
    # Let's refine: The prompt says "inverse". So output[0,0] should be the color *other* than input[0,0].
    # We need to find that other color reliably.
    else:
        # Search the first few cells to find a color different from color_1
        found_color_2 = False
        for r in range(min(H, 2)): # Check first 2 rows (or fewer if grid is shorter)
            for c in range(min(W, 2)): # Check first 2 cols (or fewer if grid is narrower)
                if input_array[r, c] != color_1:
                    color_2 = input_array[r, c]
                    found_color_2 = True
                    break
            if found_color_2:
                break
        # If still not found (e.g., solid color input?), this logic breaks.
        # Assuming valid checkerboard input guarantees finding color_2.
        if not found_color_2:
             # This case shouldn't happen based on task description/examples.
             # If it does, maybe return the input or raise an error?
             # For now, let's assume color_2 is always identifiable.
             # A fallback could be color_2 = (color_1 + 1) % 10, but that's arbitrary.
             # Given the examples, finding color_2 in the top-left 2x2 block seems safe.
             # Let's stick to the logic derived from examples. The code above should handle it.
             # If grid is 1x1, color_2 remains undefined here.
             pass # color_2 might remain undefined, needs handling below if H=1, W=1

    # 4. Create a new output grid with dimensions H x W.
    output_grid = np.zeros((H, W), dtype=int)

    # 5. Iterate through each cell (row, col) of the output grid.
    for r in range(H):
        for c in range(W):
            # 6. If (row + col) is even, set the cell color to color_2 (swapped from color_1).
            if (r + c) % 2 == 0:
                # Handle 1x1 case where color_2 might not be defined.
                # The task implies swapping, but swapping requires two colors.
                # Let's assume 1x1 is invalid or needs specific handling.
                # If input is 1x1 grid of color_1, output should be color_2?
                # Requires clarification or assumption. Let's assume H>1 or W>1 based on examples.
                # If H=1 and W=1, maybe output should be color_1? Or a default like 0?
                # Let's proceed assuming color_2 was found.
                if 'color_2' in locals():
                     output_grid[r, c] = color_2
                else: # Fallback for 1x1 grid, maybe just keep original color? Or error? Output 0?
                     output_grid[r, c] = color_1 # Or raise ValueError("Cannot determine swap color for 1x1 grid")
                     
            # 7. If (row + col) is odd, set the cell color to color_1 (swapped from color_2).
            else:
                output_grid[r, c] = color_1

    # 8. Return the completed output grid (as list of lists if required by framework)
    return output_grid.tolist()
```