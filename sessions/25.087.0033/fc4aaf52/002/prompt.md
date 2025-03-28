
Previous Code:
```python
import numpy as np

"""
Identifies a single non-background object (assuming background is Azure/8).
Creates two copies of this object.
If the object contains both Blue (1) and Red (2) pixels, swaps these two colors 
in both copies.
Places the first copy shifted 4 rows down and 0 columns right from the original 
object's top-left position.
Places the second copy shifted 1 row down and 4 columns right from the original 
object's top-left position.
The output grid has the same dimensions as the input, initialized with the 
background color, and then populated with the two potentially color-swapped 
and shifted copies.
"""

def transform(input_grid):
    """
    Transforms the input grid by duplicating, shifting, and potentially 
    color-swapping a single non-background object.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 8  # Assuming Azure (8) is the background

    # Initialize the output grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # --- Step 1: Find all non-background pixels and their colors ---
    object_pixels = []
    object_colors = set()
    for r in range(rows):
        for c in range(cols):
            color = input_np[r, c]
            if color != background_color:
                object_pixels.append((r, c))
                object_colors.add(color)

    # If there's no object (only background), return the empty output grid
    if not object_pixels:
        return output_grid.tolist()

    # --- Step 2: Determine the object's bounding box top-left corner ---
    # and extract the object's pattern relative to this corner
    min_row = min(r for r, c in object_pixels)
    min_col = min(c for r, c in object_pixels)
    
    relative_pattern = []
    for r, c in object_pixels:
        color = input_np[r, c]
        # Store relative coordinates and original color
        relative_pattern.append(((r - min_row, c - min_col), color)) 

    # --- Step 3: Check if color swapping is needed ---
    # Condition: Both Blue (1) and Red (2) must be present in the object
    needs_swap = (1 in object_colors and 2 in object_colors)

    # --- Step 4: Create potentially color-swapped patterns for the two copies ---
    pattern1 = []
    pattern2 = []
    for (rel_r, rel_c), original_color in relative_pattern:
        swapped_color = original_color
        # Apply swap logic if the condition is met
        if needs_swap:
            if original_color == 1:
                swapped_color = 2
            elif original_color == 2:
                swapped_color = 1
        
        # Both copies use the same (potentially swapped) color
        pattern1.append(((rel_r, rel_c), swapped_color))
        pattern2.append(((rel_r, rel_c), swapped_color))

    # --- Step 5: Place the first copy onto the output grid ---
    # Shift: +4 rows down, +0 columns right
    shift1_row, shift1_col = 4, 0
    for (rel_r, rel_c), color in pattern1:
        target_r = min_row + rel_r + shift1_row
        target_c = min_col + rel_c + shift1_col
        # Place pixel if within grid bounds
        if 0 <= target_r < rows and 0 <= target_c < cols:
            output_grid[target_r, target_c] = color

    # --- Step 6: Place the second copy onto the output grid ---
    # Shift: +1 row down, +4 columns right
    shift2_row, shift2_col = 1, 4
    for (rel_r, rel_c), color in pattern2:
        target_r = min_row + rel_r + shift2_row
        target_c = min_col + rel_c + shift2_col
        # Place pixel if within grid bounds
        if 0 <= target_r < rows and 0 <= target_c < cols:
            output_grid[target_r, target_c] = color

    # --- Step 7: Return the final grid ---
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8 8 8
8 8 8 0 5 0 8 8 8 8 8 8 8 8 8 8
8 8 0 5 5 5 0 8 8 8 8 8 8 8 8 8
8 8 8 0 5 0 8 8 8 8 8 8 8 8 8 8
8 8 8 0 5 0 8 8 8 8 8 8 8 8 8 8
8 8 0 5 5 5 0 8 8 8 8 8 8 8 8 8
8 8 8 0 5 0 8 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 5 8 8 8 8 8 8 8 8
8 8 8 8 8 8 5 0 5 8 8 8 8 8 8 8
8 8 8 8 8 5 0 0 0 5 8 8 8 8 8 8
8 8 8 8 8 8 5 0 5 8 8 8 8 8 8 8
8 8 8 5 0 5 8 8 8 8 8 8 8 8 8 8
8 8 5 0 0 0 5 8 8 8 8 8 8 8 8 8
8 8 8 5 0 5 8 8 8 8 8 8 8 8 8 8
8 8 8 8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 0 8 8 8 8 8 8 8
8 8 8 8 8 8 8 0 5 0 8 8 8 8 8 8
8 8 8 8 8 8 0 5 5 5 0 8 8 8 8 8
8 8 8 8 0 8 8 0 5 0 8 8 8 8 8 8
8 8 8 0 5 0 8 0 5 0 8 8 8 8 8 8
8 8 0 5 5 5 0 5 5 5 0 8 8 8 8 8
8 8 8 0 5 0 8 0 5 0 8 8 8 8 8 8
8 8 8 0 5 0 8 8 0 8 8 8 8 8 8 8
8 8 0 5 5 5 0 8 8 8 8 8 8 8 8 8
8 8 8 0 5 0 8 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 48
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 37.5

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 1 2 1 8 8 8 8 8 8 8 8 8 8 8 8
8 1 2 1 8 8 8 8 8 8 8 8 8 8 8 8
8 1 2 2 1 1 8 8 8 8 8 8 8 8 8 8
8 1 2 2 1 1 8 8 8 8 8 8 8 8 8 8
8 1 2 1 8 8 8 8 8 8 8 8 8 8 8 8
8 1 2 1 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 1 2 8 8 8 8 8 8 8
8 8 8 8 8 8 2 1 2 8 8 8 8 8 8 8
8 8 8 8 8 8 2 1 1 2 2 8 8 8 8 8
8 2 1 1 2 2 8 8 8 8 8 8 8 8 8 8
8 2 1 2 8 8 8 8 8 8 8 8 8 8 8 8
8 2 1 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 1 2 8 8 8 8 8 8 8 8
8 8 8 8 8 2 1 2 8 8 8 8 8 8 8 8
8 8 2 8 8 2 1 1 2 2 8 8 8 8 8 8
8 2 1 2 8 2 1 1 2 2 8 8 8 8 8 8
8 2 1 2 8 2 1 2 8 8 8 8 8 8 8 8
8 2 1 1 2 2 1 2 8 8 8 8 8 8 8 8
8 2 1 1 2 2 2 8 8 8 8 8 8 8 8 8
8 2 1 2 8 8 8 8 8 8 8 8 8 8 8 8
8 2 1 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 49
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 38.28125
