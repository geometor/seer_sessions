
Previous Code:
```python
import numpy as np

"""
Fill white pixels (0) based on the nearest non-white pixel(s) using Manhattan distance.

Rule:
1. For each white pixel in the input grid:
2. Find all non-white pixels in the input grid.
3. Calculate the Manhattan distance from the white pixel to all non-white pixels.
4. Identify the minimum distance found.
5. Collect all non-white pixels that are at this minimum distance.
6. If only one non-white pixel is at the minimum distance, the white pixel takes the color of that non-white pixel.
7. If multiple non-white pixels are tied for the minimum distance:
    a. Check if the color green (3) is among the colors of the tied pixels. If yes, the white pixel takes the color green (3).
    b. If green (3) is not among the tied colors, the white pixel takes the color with the lowest numerical index among the tied colors.
8. Non-white pixels in the input grid retain their original color and position in the output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the nearest non-white pixel filling rule with tie-breaking to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find coordinates and colors of non-white pixels
    non_white_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] != 0:
                non_white_pixels.append(((r, c), input_grid[r, c]))

    # If there are no non-white pixels, return the original grid
    if not non_white_pixels:
        return output_grid

    # Find coordinates of white pixels
    white_pixel_coords = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 0:
                white_pixel_coords.append((r, c))

    # Process each white pixel
    for r_white, c_white in white_pixel_coords:
        min_distance = float('inf')
        nearest_pixels_info = [] # Stores (distance, color)

        # Calculate distance to all non-white pixels
        for (r_non_white, c_non_white), color in non_white_pixels:
            distance = abs(r_white - r_non_white) + abs(c_white - c_non_white)

            # Update minimum distance and nearest pixels list
            if distance < min_distance:
                min_distance = distance
                nearest_pixels_info = [(distance, color)]
            elif distance == min_distance:
                nearest_pixels_info.append((distance, color))

        # Determine the color based on nearest pixels and tie-breaking rules
        final_color = 0 # Default just in case (shouldn't happen if non_white_pixels is not empty)
        if len(nearest_pixels_info) == 1:
            # No tie, use the color of the single nearest pixel
            final_color = nearest_pixels_info[0][1]
        elif len(nearest_pixels_info) > 1:
            # Tie-breaking needed
            tied_colors = {info[1] for info in nearest_pixels_info}
            if 3 in tied_colors:
                # Green (3) wins ties
                final_color = 3
            else:
                # Otherwise, the color with the lowest index wins
                final_color = min(tied_colors)
        
        # Update the output grid
        output_grid[r_white, c_white] = final_color

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 0 3 0 0 3 3 3 0 3
0 2 2 2 0 0 2 0 2 0
0 2 2 0 0 0 0 2 0 0
0 2 0 8 0 8 8 0 2 0
3 2 2 0 8 8 0 2 2 0
3 0 0 8 0 8 0 2 0 0
0 0 2 8 0 8 8 2 2 0
0 2 2 0 2 2 2 2 2 0
0 0 2 2 2 0 2 0 2 3
3 3 3 0 3 3 3 3 0 3
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3
3 2 2 2 2 2 2 2 2 3
3 2 2 2 2 2 2 2 2 3
3 2 2 8 8 8 8 2 2 3
3 2 2 8 8 8 8 2 2 3
3 2 2 8 8 8 8 2 2 3
3 2 2 8 8 8 8 2 2 3
3 2 2 2 2 2 2 2 2 3
3 2 2 2 2 2 2 2 2 3
3 3 3 3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3
3 2 2 2 2 3 2 3 2 3
2 2 2 2 2 8 2 2 2 3
3 2 2 8 8 8 8 2 2 2
3 2 2 2 8 8 2 2 2 2
3 3 2 8 8 8 2 2 2 2
3 2 2 8 2 8 8 2 2 2
2 2 2 2 2 2 2 2 2 3
3 3 2 2 2 3 2 3 2 3
3 3 3 3 3 3 3 3 3 3
```
Match: False
Pixels Off: 17
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 34.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 8 8 0 8 8 8 8 8 0
0 8 2 0 0 0 2 2 0 0
0 0 0 2 0 0 2 0 8 0
0 8 0 2 2 0 0 0 0 0
0 8 2 0 0 0 2 0 8 0
0 8 0 2 0 0 0 0 0 0
0 8 0 0 0 0 0 0 8 0
0 0 8 8 8 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0
0 8 2 2 2 2 2 2 8 0
0 8 2 2 2 2 2 2 8 0
0 8 2 2 2 2 2 2 8 0
0 8 2 2 2 2 2 2 8 0
0 8 2 2 2 2 2 2 8 0
0 8 2 2 2 2 2 2 8 0
0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 2 2 8 2 2 2 2 2
8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 8 8
8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 43
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 86.00000000000001
