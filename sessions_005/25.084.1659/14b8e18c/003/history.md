
Previous Code:
```python
import copy

def transform(input_grid):
    """
    Transforms the input grid by changing specific background pixels (orange, 7) to red (2).
    A background pixel at (r, c) is changed to red if it is part of any 2x2 square
    (fully within the grid bounds) that contains exactly one non-background pixel
    (i.e., one foreground pixel and three background pixels). The four potential 2x2 squares
    checked are those for which the pixel (r, c) is one of the four cells.
    All other pixels retain their original color.
    """

    # --- Helper Functions ---
    def is_valid(r, c, h, w):
        """Checks if coordinates (r, c) are within grid bounds (h, w)."""
        return 0 <= r < h and 0 <= c < w

    def check_square_condition(grid, tr, tc, h, w, bg_color):
        """
        Checks if a 2x2 square starting at top-left (tr, tc) is fully within bounds
        and contains exactly one foreground pixel.
        """
        foreground_count = 0
        pixel_count = 0
        for r_offset in range(2):
            for c_offset in range(2):
                r, c = tr + r_offset, tc + c_offset
                # Check if this cell of the 2x2 square is within grid bounds
                if is_valid(r, c, h, w):
                    pixel_count += 1
                    # Count foreground pixels within the square
                    if grid[r][c] != bg_color:
                        foreground_count += 1
                else:
                    # If any part of the 2x2 square is out of bounds, it cannot meet the condition
                    # which requires 4 pixels (1 foreground, 3 background).
                    return False

        # The condition is met if the square is fully within bounds (4 pixels)
        # and has exactly 1 foreground pixel.
        return pixel_count == 4 and foreground_count == 1

    # --- Main Transformation Logic ---

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of input_grid
    output_grid = copy.deepcopy(input_grid)

    # Define relevant colors
    background_color = 7 # orange
    target_color = 2     # red

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # We only potentially change background pixels
            if input_grid[r][c] == background_color:
                # Define the top-left corners (tr, tc) of the four 2x2 squares
                # that would contain the current pixel (r, c).
                # Square 1: (r, c) is bottom-right -> TL corner is (r-1, c-1)
                # Square 2: (r, c) is bottom-left  -> TL corner is (r-1, c)
                # Square 3: (r, c) is top-right    -> TL corner is (r, c-1)
                # Square 4: (r, c) is top-left     -> TL corner is (r, c)
                square_origins = [
                    (r - 1, c - 1),
                    (r - 1, c),
                    (r, c - 1),
                    (r, c)
                ]

                # Check if any of these squares meet the transformation condition
                should_change_color = False
                for tr, tc in square_origins:
                    # Check the condition for the square starting at (tr, tc)
                    if check_square_condition(input_grid, tr, tc, height, width, background_color):
                        should_change_color = True
                        break # Condition met by at least one square, no need to check further

                # If the condition was met by any relevant square, change the pixel color
                if should_change_color:
                    output_grid[r][c] = target_color

    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 7 7 7 7 7 7 7 7 7
7 6 6 6 6 7 7 7 6 7
7 6 7 7 6 7 7 6 7 7
7 6 7 7 6 7 7 7 7 7
7 6 6 6 6 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 6 7 7 6 6 6 6 7
7 6 7 7 7 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 2 7 7 2 7 7 7 7 7
2 6 6 6 6 2 7 7 6 7
7 6 7 7 6 7 7 6 7 7
7 6 7 7 6 7 7 7 7 7
2 6 6 6 6 2 7 7 7 7
7 2 7 7 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 6 7 7 6 6 6 6 7
7 6 7 7 7 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7
```
Transformed Output:
```
2 2 7 7 2 2 7 2 2 2
2 6 6 6 6 2 2 2 6 2
7 6 7 7 6 7 2 6 2 2
7 6 7 7 6 7 2 2 2 7
2 6 6 6 6 2 7 7 7 7
2 2 7 7 2 2 7 7 7 7
7 2 2 2 2 2 7 7 2 2
2 2 6 2 2 6 6 6 6 2
2 6 2 2 2 6 6 6 6 2
2 2 2 7 2 2 7 7 2 2
```
Match: False
Pixels Off: 40
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 80.0

## Example 2:
Input:
```
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 6 6 6 7 7 6 7 7
7 7 6 7 6 7 7 6 7 7
7 7 6 6 6 7 7 6 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 6 6 6 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 7 7 7 7 7 7 7
7 7 2 7 2 7 7 7 7 7
7 2 6 6 6 2 7 6 7 7
7 7 6 7 6 7 7 6 7 7
7 2 6 6 6 2 7 6 7 7
7 7 2 7 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 6 6 6 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
```
Transformed Output:
```
7 7 7 7 7 7 7 7 7 7
7 2 2 7 2 2 2 2 2 7
7 2 6 6 6 2 2 6 2 7
7 7 6 7 6 7 7 6 7 7
7 2 6 6 6 2 2 6 2 7
7 2 2 7 2 2 2 2 2 7
7 2 2 7 2 2 7 7 7 7
7 2 6 6 6 2 7 7 7 7
7 2 2 7 2 2 7 7 7 7
7 7 7 7 7 7 7 7 7 7
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 48.0

## Example 3:
Input:
```
7 7 7 7 7 7 7 7 7 7
7 8 8 8 8 8 8 8 8 7
7 8 7 7 7 7 7 7 8 7
7 8 7 7 7 7 7 7 8 7
7 8 7 7 8 8 7 7 8 7
7 8 7 7 8 8 7 7 8 7
7 8 7 7 7 7 7 7 8 7
7 8 7 7 7 7 7 7 8 7
7 8 8 8 8 8 8 8 8 7
7 7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 2 7 7 7 7 7 7 2 7
2 8 8 8 8 8 8 8 8 2
7 8 7 7 7 7 7 7 8 7
7 8 7 7 2 2 7 7 8 7
7 8 7 2 8 8 2 7 8 7
7 8 7 2 8 8 2 7 8 7
7 8 7 7 2 2 7 7 8 7
7 8 7 7 7 7 7 7 8 7
2 8 8 8 8 8 8 8 8 2
7 2 7 7 7 7 7 7 2 7
```
Transformed Output:
```
2 2 7 7 7 7 7 7 2 2
2 8 8 8 8 8 8 8 8 2
7 8 7 7 7 7 7 7 8 7
7 8 7 2 2 2 2 7 8 7
7 8 7 2 8 8 2 7 8 7
7 8 7 2 8 8 2 7 8 7
7 8 7 2 2 2 2 7 8 7
7 8 7 7 7 7 7 7 8 7
2 8 8 8 8 8 8 8 8 2
2 2 7 7 7 7 7 7 2 2
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.0
