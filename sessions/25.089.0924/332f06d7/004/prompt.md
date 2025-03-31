
Previous Code:
```python
import numpy as np
from scipy.ndimage import binary_dilation, generate_binary_structure

"""
Transforms the input grid based on a conditional rule involving Red (2), White (0), and Blue (1) pixels. 
The rule selection depends on whether any White pixel is adjacent (including diagonals) to any Blue pixel, 
and whether the total count of Red pixels is greater than 1.

Condition Logic:
1. Check if any White(0) pixel is adjacent (8-way connectivity) to any Blue(1) pixel.
2. Count the total number of Red(2) pixels.
3. If (White is adjacent to Blue) AND (Red pixel count > 1), then apply Rule Set TRUE.
4. Otherwise, apply Rule Set FALSE.

Rule Sets:
- Rule Set TRUE: White(0) becomes Blue(1), Blue(1) becomes White(0). Red(2) and others remain unchanged.
- Rule Set FALSE: Red(2) becomes White(0), White(0) becomes Blue(1). Blue(1) and others remain unchanged.
"""

def check_adjacency(grid, color1, color2):
    """
    Checks if any pixel of color1 is adjacent (8-way) to any pixel of color2.

    Args:
        grid (np.array): The input grid.
        color1 (int): The first color value.
        color2 (int): The second color value.

    Returns:
        bool: True if any color1 pixel is adjacent to a color2 pixel, False otherwise.
    """
    # Create a mask for color1 pixels
    mask1 = (grid == color1)
    if not np.any(mask1):
        return False # No pixels of color1 exist

    # Define 8-way connectivity structure
    structure = generate_binary_structure(2, 2) 
    
    # Dilate the color1 mask by one pixel in all 8 directions
    dilated_mask1 = binary_dilation(mask1, structure=structure)
    
    # Create a mask for color2 pixels
    mask2 = (grid == color2)
    if not np.any(mask2):
        return False # No pixels of color2 exist

    # Check if the dilated area of color1 overlaps with any color2 pixel
    return np.any(dilated_mask1 & mask2)

def count_pixels(grid, color):
    """
    Counts the number of pixels of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to count.

    Returns:
        int: The total count of pixels with the specified color.
    """
    return np.sum(grid == color)

def transform(input_grid):
    """
    Applies the conditional color transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # --- Determine the condition ---
    # Check if White(0) is adjacent to Blue(1)
    white_touches_blue = check_adjacency(input_np, 0, 1)
    
    # Count the number of Red(2) pixels
    num_red_pixels = count_pixels(input_np, 2)
    
    # Evaluate the primary condition for using Rule Set TRUE
    use_true_rule = white_touches_blue and (num_red_pixels > 1)
    
    # --- Apply the transformation ---
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    
    if use_true_rule:
        # Apply Rule Set TRUE: White -> Blue, Blue -> White
        # Find pixels that are White (0) in the input
        white_pixels_mask = (input_np == 0)
        # Find pixels that are Blue (1) in the input
        blue_pixels_mask = (input_np == 1)
        
        # Change White pixels to Blue in the output grid
        output_grid[white_pixels_mask] = 1 
        # Change Blue pixels to White in the output grid
        output_grid[blue_pixels_mask] = 0 
        # Red and other colors remain unchanged (already copied)
    else:
        # Apply Rule Set FALSE: Red -> White, White -> Blue
        # Find pixels that are Red (2) in the input
        red_pixels_mask = (input_np == 2)
        # Find pixels that are White (0) in the input
        white_pixels_mask = (input_np == 0)
        
        # Change Red pixels to White in the output grid
        output_grid[red_pixels_mask] = 0
        # Change White pixels to Blue in the output grid
        output_grid[white_pixels_mask] = 1
        # Blue and other colors remain unchanged (already copied)
        
    # Convert the final NumPy array back to a list of lists for the output format
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 2 2 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 0 0 3 3 3 3 3 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 2 2 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3
3 0 0 3 0 0 0 0 0 0 3 3
3 0 0 3 0 0 0 0 0 0 3 3
3 0 0 3 0 0 3 0 0 0 3 3
3 0 0 3 0 0 3 0 0 0 0 3
3 0 0 0 0 0 3 0 0 0 0 3
3 0 0 0 0 0 3 3 0 0 3 3
3 0 0 0 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 56
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 155.55555555555554

## Example 2:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 0 0 0 0 0 1 1 3 3
3 3 3 3 3 0 0 0 0 0 1 1 3 3
3 3 3 3 3 0 0 3 3 3 3 3 3 3
3 3 3 3 3 0 0 3 3 3 3 3 3 3
3 3 3 3 3 0 0 3 3 3 3 3 3 3
3 3 3 3 3 0 0 0 0 0 3 3 3 3
3 3 3 3 3 0 0 0 0 0 3 3 3 3
3 3 3 3 3 3 3 3 3 0 3 3 3 3
3 0 0 0 0 0 0 0 0 0 3 3 3 3
3 0 0 0 0 0 0 0 0 0 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 41
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 41.83673469387753

## Example 3:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 3
2 2 2 0 0 0 0 3 3 0 0 0 0 0 0 3
2 2 2 0 0 3 3 3 3 3 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 3
3 3 3 0 0 0 0 0 0 0 3 3 3 0 0 3
3 3 3 0 0 0 0 0 0 0 3 3 3 0 0 3
3 3 3 0 0 0 0 0 0 0 3 3 3 0 0 3
3 3 0 0 0 0 3 0 0 0 3 3 3 0 0 3
3 3 0 0 0 0 3 0 0 3 3 3 0 0 0 3
3 3 0 0 0 0 3 0 0 3 3 3 0 0 0 3
3 3 0 0 0 3 3 0 0 3 3 3 0 0 0 3
3 1 1 1 0 3 3 0 0 0 0 0 0 0 0 3
3 1 1 1 0 3 3 0 0 0 0 0 0 0 0 3
3 1 1 1 0 3 3 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 111
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 86.71875

## Example 4:
Input:
```
3 3 3 3 3 3 3 3 3 3
3 0 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 2 3 3 3 3 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3
3 1 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 0 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3
3 1 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 0 3 3 3 3 3
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
