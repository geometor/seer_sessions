import numpy as np

"""
Identifies a single non-background object (assuming background is Azure/8).
Checks if the object contains both Blue (1) and Red (2) pixels.
Creates two copies of this object. 
If the object contains both Blue and Red, swaps these two colors in both copies.
Determines two shift vectors based on the color swap condition:
- Shift A: Always (4 rows down, 0 columns right).
- Shift B: (0 rows down, 5 columns right) if swap occurred, otherwise (0 rows down, 3 columns right).
Places the first copy (Copy A) shifted by Shift A from the original object's top-left position.
Places the second copy (Copy B) shifted by Shift B from the original object's top-left position.
The output grid has the same dimensions as the input, initialized with the background color, 
and then populated with the two potentially color-swapped and shifted copies.
"""

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
    object_pixels = []
    object_colors = set()
    min_row, min_col = rows, cols # Initialize to max possible values
    
    for r in range(rows):
        for c in range(cols):
            color = input_np[r, c]
            if color != background_color:
                object_pixels.append((r, c))
                object_colors.add(color)
                min_row = min(min_row, r)
                min_col = min(min_col, c)

    # If there's no object (only background), return the empty output grid
    if not object_pixels:
        return output_grid.tolist()

    # Extract the object's pattern relative to its top-left corner
    relative_pattern = []
    for r, c in object_pixels:
        color = input_np[r, c]
        # Store relative coordinates and original color
        relative_pattern.append(((r - min_row, c - min_col), color)) 

    # --- Step 2: Check if color swapping is needed ---
    # Condition: Both Blue (1) and Red (2) must be present in the object
    needs_swap = (1 in object_colors and 2 in object_colors)

    # --- Step 3: Determine the shift vectors ---
    shift_A = (4, 0)  # Always (delta_row=4, delta_col=0)
    if needs_swap:
        shift_B = (0, 5)  # (delta_row=0, delta_col=5) if swap occurred
    else:
        shift_B = (0, 3)  # (delta_row=0, delta_col=3) if no swap occurred

    # --- Step 4: Place the two copies onto the output grid ---
    for (rel_r, rel_c), original_color in relative_pattern:
        
        # Determine the output color (apply swap if needed)
        output_color = original_color
        if needs_swap:
            if original_color == 1:
                output_color = 2
            elif original_color == 2:
                output_color = 1
        
        # Calculate target position for Copy A and place pixel
        target_r_A = min_row + rel_r + shift_A[0]
        target_c_A = min_col + rel_c + shift_A[1]
        if 0 <= target_r_A < rows and 0 <= target_c_A < cols:
            output_grid[target_r_A, target_c_A] = output_color

        # Calculate target position for Copy B and place pixel
        target_r_B = min_row + rel_r + shift_B[0]
        target_c_B = min_col + rel_c + shift_B[1]
        if 0 <= target_r_B < rows and 0 <= target_c_B < cols:
            output_grid[target_r_B, target_c_B] = output_color

    # --- Step 5: Return the final grid ---
    return output_grid.tolist()