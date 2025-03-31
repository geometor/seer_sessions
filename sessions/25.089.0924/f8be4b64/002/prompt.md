
Previous Code:
```python
import numpy as np

"""
Identifies "plus" shapes made of green pixels (3) in the input grid.
A plus shape is defined by a central pixel having four green neighbors (North, South, East, West).
The color of the central pixel (the "core color") determines a fill operation:
- Red (2) or Gray (5): Fill the background (0) pixels in the intersecting row and column with the core color.
- Magenta (6): Fill the background (0) pixels in the intersecting column with the core color.
- Yellow (4) or Azure (8): Fill the background (0) pixels in the intersecting row with the core color.
- White (0) or any other color: No fill operation.

Fill operations only change white (0) background pixels. Original non-white pixels are preserved.
If multiple fill operations target the same background pixel, a priority is applied:
1. Column fill (Magenta)
2. Row/Column fill (Red, Gray)
3. Row fill (Yellow, Azure)
The fill operation with the highest priority determines the final color of the background pixel.
"""

def find_plus_centers(grid):
    """
    Finds all pixels that are centers of a green plus shape.
    A center is a pixel (r, c) where grid[r-1, c], grid[r+1, c], 
    grid[r, c-1], and grid[r, c+1] are all green (3).
    
    Args:
        grid (np.array): Input grid.

    Returns:
        list: A list of tuples, where each tuple is ((row, col), core_color).
    """
    centers = []
    height, width = grid.shape
    # Iterate through possible center locations (avoiding edges)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check orthogonal neighbors
            if (grid[r - 1, c] == 3 and
                grid[r + 1, c] == 3 and
                grid[r, c - 1] == 3 and
                grid[r, c + 1] == 3):
                core_color = grid[r, c]
                centers.append(((r, c), core_color))
    return centers

def transform(input_grid):
    """
    Transforms the input grid based on green plus shapes and their core colors.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    height, width = grid_np.shape

    # Find all green plus centers and their core colors
    plus_centers = find_plus_centers(grid_np)

    # Separate centers by the type of fill operation they trigger
    row_col_fills = [] # Priority 2 (colors 2, 5)
    col_fills = []     # Priority 1 (color 6)
    row_fills = []     # Priority 3 (colors 4, 8)

    for (r, c), core_color in plus_centers:
        if core_color in [2, 5]:
            row_col_fills.append(((r, c), core_color))
        elif core_color == 6:
            col_fills.append(((r, c), core_color))
        elif core_color in [4, 8]:
            row_fills.append(((r, c), core_color))
        # Other core colors (like 0) do nothing

    # Iterate through each pixel to determine its final color
    for r in range(height):
        for c in range(width):
            # Only modify original background pixels
            if grid_np[r, c] == 0:
                # Check for fills based on priority
                
                # Priority 1: Column fills (Magenta)
                col_fill_color = 0
                for (pr, pc), p_color in col_fills:
                    if pc == c:
                        col_fill_color = p_color # Should always be 6
                        break # Found highest priority fill for this pixel
                
                if col_fill_color != 0:
                    output_grid[r, c] = col_fill_color
                    continue # Apply highest priority and move to next pixel

                # Priority 2: Row/Column fills (Red, Gray)
                row_col_fill_color = 0
                # Check potential fills, last one found wins if multiple apply
                for (pr, pc), p_color in row_col_fills:
                    if pr == r or pc == c:
                        row_col_fill_color = p_color 
                
                if row_col_fill_color != 0:
                    output_grid[r, c] = row_col_fill_color
                    continue # Apply this priority and move to next pixel
                    
                # Priority 3: Row fills (Yellow, Azure)
                row_fill_color = 0
                # Check potential fills, last one found wins if multiple apply
                for (pr, pc), p_color in row_fills:
                    if pr == r:
                        row_fill_color = p_color
                        
                if row_fill_color != 0:
                    output_grid[r, c] = row_fill_color
                    # No continue needed, this is the last check

    # Convert back to list of lists
    return output_grid.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 5 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 6 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 4 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 3 0 3 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 3 0 0 0 0
5 5 5 0 5 5 5 6 5 5 5 5 3 5 3 5 5 5
0 0 0 0 0 0 0 6 0 0 0 0 0 3 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 5 4 0 0 0
6 6 6 0 6 6 3 6 3 6 6 6 6 5 4 6 6 6
0 0 0 0 0 0 0 3 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 4 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 3 0 0 0
4 4 4 0 4 4 4 6 4 4 4 4 4 3 4 3 4 4
0 0 0 0 0 0 0 6 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0 4 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 3 0 3 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 3 0 0 0 0
5 5 5 5 5 5 5 6 5 5 5 5 3 5 3 5 5 5
0 0 0 0 0 0 0 6 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 3 6 3 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 3 0 0 0
4 4 4 4 4 4 4 6 4 4 4 4 4 3 4 3 4 4
0 0 0 0 0 0 0 6 0 0 0 0 0 5 3 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 5 0 0 0 0
```
Match: False
Pixels Off: 23
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 14.197530864197518

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 5 3 0 0 0 0 3 0
0 0 3 0 0 0 0 3 6 3
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 8 3 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 5 0 0 8 0 0 6 0
0 0 3 0 0 8 0 0 6 0
5 3 5 3 5 8 5 5 3 0
0 0 3 6 6 8 6 3 6 3
0 0 5 0 0 8 0 0 3 0
0 0 5 0 0 3 0 0 6 0
8 8 5 8 3 8 3 8 6 8
0 0 5 0 0 3 0 0 6 0
0 0 5 0 0 8 0 0 6 0
0 0 5 0 0 8 0 0 6 0
```
Transformed Output:
```
0 0 5 0 0 0 0 0 6 0
0 0 3 0 0 0 0 0 6 0
5 3 5 3 5 5 5 5 3 5
0 0 3 0 0 0 0 3 6 3
0 0 5 0 0 0 0 0 3 0
0 0 5 0 0 3 0 0 6 0
8 8 5 8 3 8 3 8 6 8
0 0 5 0 0 3 0 0 6 0
0 0 5 0 0 0 0 0 6 0
0 0 5 0 0 0 0 0 6 0
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 22.0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 2 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
2 2 3 2 3 2 2 2 0 2 2 2 2
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 3 0 3 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
2 2 3 2 3 2 2 2 2 2 2 2 2
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 3 0 3 0 0 0
0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.1834319526627155

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 2 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 6 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 8 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
2 2 2 2 3 2 3 2 2 2 2 2 2 0 2 2 2 2 2 2 3 0 8 0 0 0 0 0 0 0
0 0 0 0 0 3 6 6 6 6 6 6 6 0 6 6 6 6 6 3 6 3 8 6 6 6 6 6 6 6
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 3 0 3 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
8 8 8 8 8 2 8 8 8 8 8 8 8 0 8 8 8 8 8 8 6 3 8 3 8 8 8 8 8 8
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 8 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
2 2 2 2 3 2 3 2 2 2 2 2 2 2 2 2 2 2 2 2 3 2 2 2 2 2 2 2 2 2
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 3 6 3 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 3 0 3 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 3 8 3 8 8 8 8 8 8
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 3 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 56
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.444444444444429
