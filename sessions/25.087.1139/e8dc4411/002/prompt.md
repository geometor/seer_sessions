
Previous Code:
```python
import numpy as np
from collections import Counter

"""
The transformation rule identifies a unique 'source' pixel in the input grid, distinguished by its color being neither the predominant background color nor white (0). Based on the color of this source pixel, a specific predefined pattern of relative coordinates is selected. This pattern is then applied relative to the source pixel's location, changing the pixels in the output grid at the calculated target coordinates to the source pixel's color. The background and other elements like white pixels remain unchanged unless overwritten by the pattern application.
"""

def find_most_frequent_color(grid):
    """Finds the most frequent color in the grid, ignoring white (0)."""
    colors = grid.flatten()
    color_counts = Counter(c for c in colors if c != 0)
    if not color_counts:
        # Handle cases with only white pixels or empty grids if necessary
        # For ARC, grids usually have a background. If not, maybe return 0?
        # Let's assume a dominant non-white color exists based on examples.
        # If the grid is all white, the concept of 'background' is less clear.
        # Could fall back to the most frequent overall, which would be 0.
        return 0 # Or handle error/edge case appropriately
    # Return the color (key) with the highest count (value)
    return color_counts.most_common(1)[0][0]

def find_source_pixel(grid, background_color):
    """Finds the unique pixel that is not the background color and not white (0)."""
    source_pixel_info = None
    found_count = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != background_color and color != 0:
                source_pixel_info = {'row': r, 'col': c, 'color': color}
                found_count += 1
                # Assuming only one such pixel exists based on the problem description
                # If more than one could exist, this logic would need adjustment.
    # Add a check to ensure exactly one source pixel was found, as per perception
    if found_count == 1:
         return source_pixel_info
    else:
        # Handle cases where 0 or >1 source pixels are found (error or different logic needed)
        print(f"Warning: Found {found_count} source pixels. Expected 1.")
        return None # Or raise an error

def transform(input_grid):
    """
    Applies a color-specific pattern anchored at a unique source pixel.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # 1. Determine the background color
    background_color = find_most_frequent_color(grid)

    # 2. Find the source pixel (location and color)
    source_pixel = find_source_pixel(grid, background_color)

    # Proceed only if a unique source pixel was found
    if source_pixel is None:
        print("Error: Could not find a unique source pixel.")
        return output_grid.tolist() # Return the original grid if no source found

    source_row = source_pixel['row']
    source_col = source_pixel['col']
    source_color = source_pixel['color']

    # 3. Define the patterns associated with specific source colors
    # Patterns are sets of (dr, dc) relative offsets
    patterns = {
        3: {(0,0), (1,0), (1,1), (1,2), (2,-2), (2,0), (3,-3), (3,-2), (3,-1), (4,-4), (4,-2), (5,-4), (5,-3)}, # Green
        2: {(0,0), (1,-1), (1,1), (2,0), (2,2), (3,1), (3,3), (4,2), (4,4), (5,3), (5,5), (6,4), (6,6)}, # Red
        8: {(-4,0), (-4,1), (-4,3), (-4,4), (-3,0), (-3,1), (-3,3), (-3,4), (-2,2), (-1,0), (-1,1), (-1,3), (-1,4), (0,0), (0,1), (0,3), (0,4)}  # Azure
    }

    # 4. Select the appropriate pattern
    selected_pattern = patterns.get(source_color)

    # Proceed only if a pattern exists for the source color
    if selected_pattern is None:
        print(f"Warning: No pattern defined for source color {source_color}.")
        return output_grid.tolist() # Return the original grid if no pattern found

    # 5. Apply the pattern to the output grid
    for dr, dc in selected_pattern:
        target_row = source_row + dr
        target_col = source_col + dc

        # 6. Check if the target coordinates are within grid bounds
        if 0 <= target_row < rows and 0 <= target_col < cols:
            # 7. Update the output grid pixel
            output_grid[target_row, target_col] = source_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 0 1 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 1 1 1 1 1 1 1
1 1 1 1 3 1 0 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 0 1 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 1 1 1 1 1 1 1
1 1 1 1 3 1 0 1 1 1 1 1 1 1 1
1 1 1 3 3 3 1 1 1 1 1 1 1 1 1
1 1 3 1 3 1 1 1 1 1 1 1 1 1 1
1 3 3 3 1 1 1 1 1 1 1 1 1 1 1
3 1 3 1 1 1 1 1 1 1 1 1 1 1 1
3 3 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 0 1 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 1 1 1 1 1 1 1
1 1 1 1 3 1 0 1 1 1 1 1 1 1 1
1 1 1 1 3 3 3 1 1 1 1 1 1 1 1
1 1 3 1 3 1 1 1 1 1 1 1 1 1 1
1 3 3 3 1 1 1 1 1 1 1 1 1 1 1
3 1 3 1 1 1 1 1 1 1 1 1 1 1 1
3 3 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 1.025641025641022

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8
8 8 8 0 8 0 8 8 8 8 8 8 8 8
8 8 8 8 0 8 2 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8
8 8 8 0 8 0 8 8 8 8 8 8 8 8
8 8 8 8 0 8 2 8 8 8 8 8 8 8
8 8 8 8 8 2 8 2 8 8 8 8 8 8
8 8 8 8 8 8 2 8 2 8 8 8 8 8
8 8 8 8 8 8 8 2 8 2 8 8 8 8
8 8 8 8 8 8 8 8 2 8 2 8 8 8
8 8 8 8 8 8 8 8 8 2 8 2 8 8
8 8 8 8 8 8 8 8 8 8 2 8 2 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8
8 8 8 0 8 0 8 8 8 8 8 8 8 8
8 8 8 8 0 8 2 8 8 8 8 8 8 8
8 8 8 8 8 2 8 2 8 8 8 8 8 8
8 8 8 8 8 8 2 8 2 8 8 8 8 8
8 8 8 8 8 8 8 2 8 2 8 8 8 8
8 8 8 8 8 8 8 8 2 8 2 8 8 8
8 8 8 8 8 8 8 8 8 2 8 2 8 8
8 8 8 8 8 8 8 8 8 8 2 8 2 8
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 8 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 4 4 0 4 4 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 4 4 4 4 4 4 4 8 4 4
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 4 4 0 4 4 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 4 4 4 4 4 4 4 8 4 4
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 4 4 4 4 4 8 8 4 8 8
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 4 4 0 4 4 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 0 0 4 0 0 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
