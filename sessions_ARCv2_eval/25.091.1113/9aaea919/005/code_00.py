import numpy as np
from collections import Counter

# Define color constants for rules based on observations from examples
PLUS_TO_GRAY_COLORS = {9, 6, 3}  # Maroon, Magenta, Green plus shapes become Gray
LINE_TO_REMOVE_COLORS = {2, 3}   # Red, Green horizontal lines are removed
GRAY_COLOR = 5

def _find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    counts = Counter(grid.flatten())
    # Handle empty grid case if necessary
    if not counts:
        return 0 # Default to white if grid is empty
    # Find the color with the highest count
    background_color = counts.most_common(1)[0][0]
    return background_color

def _is_plus_center(grid, r, c, rows, cols, color):
    """Checks if (r, c) is the center of a 3x3 plus shape of the given color."""
    # Check bounds for a 3x3 area centered at (r, c)
    if not (0 < r < rows - 1 and 0 < c < cols - 1):
        return False
    # Check if the center and its 4 orthogonal neighbors have the specified color
    return (grid[r-1, c] == color and
            grid[r+1, c] == color and
            grid[r, c-1] == color and
            grid[r, c+1] == color)

def _is_h_line_start(grid, r, c, rows, cols, color):
    """Checks if (r, c) is the start of a 1x5 horizontal line of the given color."""
    # Check bounds for a 1x5 area starting at (r, c)
    if not (c + 4 < cols):
        return False
    # Check if the 5 pixels starting from (r, c) have the specified color
    for i in range(5):
        if grid[r, c+i] != color:
            return False
    # Optional: Ensure it's the *start* by checking the pixel to the left (if exists)
    # if c > 0 and grid[r, c-1] == color:
    #     return False # Part of a longer line or detected earlier
    return True


"""
Transforms an input grid based on specific rules applied to 5-pixel objects.
1. Identifies the background color (most frequent color).
2. Creates an output grid filled with the background color.
3. Iterates through the input grid, identifying 5-pixel plus shapes and 
   5-pixel horizontal lines.
4. Applies rules:
   - Removes 5-pixel horizontal lines if they are Red (2) or Green (3) by 
     leaving them as the background color in the output.
   - Changes the color of 5-pixel plus shapes to Gray (5) if they are 
     Maroon (9), Magenta (6), or Green (3).
   - Keeps all other identified 5-pixel plus or horizontal line shapes 
     unchanged (copies their original color to the output).
5. Uses a visited mask to avoid processing pixels multiple times.
"""
def transform(input_grid):
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Identify the background color
    background_color = _find_background_color(input_grid_np)

    # 2. Create an output grid initialized with the background color
    output_grid = np.full_like(input_grid_np, background_color)

    # 3. Create a visited mask to track processed pixels
    visited = np.zeros_like(input_grid_np, dtype=bool)

    # 4. Iterate through each pixel to find shapes
    for r in range(rows):
        for c in range(cols):
            # Skip if already processed or background
            if visited[r, c] or input_grid_np[r, c] == background_color:
                continue

            color = input_grid_np[r, c]

            # Check if it's the center of a plus shape
            if _is_plus_center(input_grid_np, r, c, rows, cols, color):
                coords = [(r, c), (r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                
                # Determine output color based on rules
                output_color = GRAY_COLOR if color in PLUS_TO_GRAY_COLORS else color
                
                # Apply to output grid and mark visited
                for pr, pc in coords:
                    output_grid[pr, pc] = output_color
                    visited[pr, pc] = True
                continue # Move to next pixel in grid iteration

            # Check if it's the start of a horizontal line shape
            # Add check to ensure we only process lines starting at c or where c-1 is different
            is_actual_start = (c == 0 or input_grid_np[r, c-1] != color)
            if is_actual_start and _is_h_line_start(input_grid_np, r, c, rows, cols, color):
                coords = [(r, c+i) for i in range(5)]

                # Determine if line should be kept and its color
                output_color = background_color # Default to remove/background
                if color not in LINE_TO_REMOVE_COLORS:
                    output_color = color # Keep original color
                
                # Apply to output grid (if not removed) and mark visited
                for pr, pc in coords:
                    if output_color != background_color:
                         output_grid[pr, pc] = output_color
                    visited[pr, pc] = True # Mark visited even if removed
                continue # Move to next pixel in grid iteration

            # If the pixel is not background, not visited, and not part of 
            # a recognized shape starting/centered here, it might be noise 
            # or part of an unrecognized shape. 
            # Based on examples, such pixels don't seem to appear or are 
            # implicitly handled by being part of shapes processed earlier.
            # If we needed to preserve *all* non-background pixels not part 
            # of the specific shapes, we'd add:
            # else:
            #     output_grid[r, c] = color
            #     visited[r,c] = True
            # But the current logic matches the example transformations better.


    # Convert back to list of lists for the required output format
    return output_grid.tolist()