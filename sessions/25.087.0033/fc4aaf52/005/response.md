```python
import numpy as np

"""
The transformation identifies a single non-background object in the input grid, where the background color is Azure (8). 
It then creates two copies of this object. 
A conditional color swap is applied to both copies: if the original object contains both Blue (1) and Red (2) pixels, then Blue and Red are swapped in the copies.
Finally, the two copies (potentially with swapped colors) are placed onto an output grid of the same dimensions as the input, initialized with the background color. 
The placement involves specific shifts relative to the original object's top-left position:
- Copy A is always shifted by (4 rows down, 1 column left).
- Copy B is shifted by (0 rows down, 5 columns right) if the color swap occurred, or by (0 rows down, 3 columns right) if no color swap occurred.
If multiple objects exist or no object exists, the behavior might be undefined by the examples, but this implementation assumes a single object.
"""

def find_single_object(grid_np, background_color):
    """
    Finds the pixels, colors, and top-left corner of a single non-background object.

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.
        background_color (int): The color designated as the background.

    Returns:
        tuple: (object_pixels, object_colors, min_row, min_col) or (None, None, None, None) if no object found.
               object_pixels: List of (row, col) tuples for object pixels.
               object_colors: Set of unique colors in the object.
               min_row, min_col: Coordinates of the top-left bounding box corner.
    """
    rows, cols = grid_np.shape
    object_pixels = []
    object_colors = set()
    min_row, min_col = rows, cols  # Initialize to max possible values

    for r in range(rows):
        for c in range(cols):
            color = grid_np[r, c]
            if color != background_color:
                object_pixels.append((r, c))
                object_colors.add(color)
                min_row = min(min_row, r)
                min_col = min(min_col, c)

    if not object_pixels:
        return None, None, None, None

    return object_pixels, object_colors, min_row, min_col

def transform(input_grid):
    """
    Transforms the input grid by duplicating, shifting, and potentially 
    color-swapping a single non-background object based on specific rules.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 8  # Azure is the background color

    # Initialize the output grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # --- Step 1: Find the single non-background object ---
    object_pixels, object_colors, min_row, min_col = find_single_object(input_np, background_color)

    # If there's no object (only background), return the empty output grid
    if object_pixels is None:
        return output_grid.tolist()

    # --- Step 2: Extract the object's relative pattern ---
    relative_pattern = []
    for r, c in object_pixels:
        color = input_np[r, c]
        # Store relative coordinates and original color
        relative_pattern.append(((r - min_row, c - min_col), color)) 

    # --- Step 3: Check if color swapping is needed ---
    # Condition: Both Blue (1) and Red (2) must be present in the object
    needs_swap = (1 in object_colors and 2 in object_colors)

    # --- Step 4: Determine the shift vectors ---
    shift_A = (4, -1) # Corrected: Always (delta_row=4, delta_col=-1)
    if needs_swap:
        shift_B = (0, 5)  # (delta_row=0, delta_col=5) if swap occurred
    else:
        shift_B = (0, 3)  # (delta_row=0, delta_col=3) if no swap occurred

    # --- Step 5: Place the two copies onto the output grid ---
    for (rel_r, rel_c), original_color in relative_pattern:
        
        # Determine the output color (apply swap if needed for both copies)
        output_color = original_color
        if needs_swap:
            if original_color == 1:
                output_color = 2
            elif original_color == 2:
                output_color = 1
        
        # Calculate target position for Copy A and place pixel if within bounds
        target_r_A = min_row + rel_r + shift_A[0]
        target_c_A = min_col + rel_c + shift_A[1]
        if 0 <= target_r_A < rows and 0 <= target_c_A < cols:
            output_grid[target_r_A, target_c_A] = output_color

        # Calculate target position for Copy B and place pixel if within bounds
        target_r_B = min_row + rel_r + shift_B[0]
        target_c_B = min_col + rel_c + shift_B[1]
        if 0 <= target_r_B < rows and 0 <= target_c_B < cols:
            output_grid[target_r_B, target_c_B] = output_color # Use the same potentially swapped color

    # --- Step 6: Return the final grid ---
    return output_grid.tolist()
```