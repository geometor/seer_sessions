
Previous Code:
```python
import numpy as np
from typing import List, Tuple

"""
Filters a grid based on pixel adjacency.
Identifies two primary non-background colors: a 'target' color and a 'context' color.
The identification heuristic assumes the 'target' color is the less frequent of the two non-background colors.
Keeps 'target' color pixels in the output grid only if they are NOT adjacent (horizontally, vertically, or diagonally)
to any 'context' color pixel in the input grid.
All 'context' color pixels and 'target' pixels adjacent to 'context' pixels are removed (replaced with the background color, assumed to be 0).
The grid dimensions remain unchanged.
If only one non-background color exists, it's treated as the 'target' color and all its pixels are kept (as there's no 'context' color to cause removal).
If zero non-background colors exist, or if target/context cannot be reliably distinguished (e.g., equal counts, >2 non-background colors), the original grid might be returned or behavior is undefined based on examples.
"""

def identify_colors(grid: np.ndarray) -> Tuple[int, int, int]:
    """
    Identifies background, target, and context colors based on examples.
    Assumes background=0. Finds non-background colors.
    Hypothesis: If two non-background colors exist, Target color is less frequent than context color.
    Returns: (background_color, target_color, context_color)
             target_color or context_color can be -1 if not applicable/found.
             Special negative codes (-2, -3) indicate ambiguity or errors.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    background_color = 0
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    num_non_background = len(non_background_colors)

    target_color = -1
    context_color = -1

    if num_non_background == 0:
        # Only background color present
        pass # target/context remain -1
    elif num_non_background == 1:
        # Only one non-background color, assume it's target, no context
        target_color = list(non_background_colors.keys())[0]
        context_color = -1 # No context color
    elif num_non_background == 2:
        # Exactly two non-background colors, apply frequency heuristic
        colors = list(non_background_colors.keys())
        counts_list = list(non_background_colors.values())

        # Assign based on frequency (target is less frequent)
        if counts_list[0] < counts_list[1]:
            target_color = colors[0]
            context_color = colors[1]
        elif counts_list[1] < counts_list[0]:
            target_color = colors[1]
            context_color = colors[0]
        else:
             # Tie in counts - ambiguous based on heuristic.
             print("Warning: Tie in non-background color counts, cannot distinguish target/context.")
             target_color = -2 # Indicate ambiguity
             context_color = -2

    else: # More than two non-background colors
        print("Warning: More than two non-background colors found.")
        # Cannot determine target/context based on the observed pattern.
        target_color = -3 # Indicate >2 colors
        context_color = -3

    return background_color, target_color, context_color

def check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    """
    Checks the 8 neighbors (Moore neighborhood) of cell (r, c) in the grid
    to see if any neighbor has the specified color_to_find.
    Returns True if found, False otherwise.
    """
    rows, cols = grid.shape
    # Iterate through the 3x3 neighborhood centered at (r, c)
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue

            # Calculate neighbor coordinates
            nr, nc = r + dr, c + dc

            # Check if the neighbor coordinates are within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor has the color we're looking for
                if grid[nr, nc] == color_to_find:
                    return True # Found the color in a neighbor

    # If the loop completes without finding the color
    return False

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: Keeps target pixels only if they are not
    adjacent (8-way connectivity) to any context pixel. Context pixels are removed.
    Target/context colors are identified based on frequency (target is less frequent).
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Step 1: Identify background, target, and context colors
    background_color, target_color, context_color = identify_colors(input_grid)

    # Handle cases where color identification might fail or lead to undefined behavior
    if target_color < 0: # Includes -1 (no target), -2 (ambiguous), -3 (>2 colors)
        # If no target identified (-1), or ambiguous (-2), or too many colors (-3),
        # the safe default might be returning an empty grid of the same size,
        # or potentially the original grid. Let's return an empty grid.
        # If target is -1 (only background found), this results in an empty grid correctly.
        print(f"Color identification issue (code: {target_color}). Returning empty grid.")
        output_grid = np.full((rows, cols), background_color, dtype=int)
        return output_grid.tolist()

    # Step 2: Create a new grid initialized with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Step 3: Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Step 4: Check if the current pixel is the target color
            if input_grid[r, c] == target_color:

                # Step 5a: Assume the target pixel should be kept unless proven otherwise
                keep_pixel = True

                # Step 5b: Check if a context color exists and if any neighbor has it
                if context_color != -1: # Check only if context color is defined
                    is_near_context = check_neighbors_for_color(input_grid, r, c, context_color)
                    if is_near_context:
                        keep_pixel = False # Do not keep if adjacent to context

                # Step 5c: If the pixel should be kept, place it in the output grid
                if keep_pixel:
                    output_grid[r, c] = target_color
            # Pixels that are not the target color (i.e., background or context)
            # are implicitly left as the background color in the output grid.

    # Step 6: Convert the resulting numpy array back to a list of lists
    return output_grid.tolist()

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 3 3 3 3 3 3 3 0 0
6 0 3 3 0 0 0 0 3 0 0 6
0 0 3 0 0 6 0 0 3 0 0 0
0 0 3 3 0 6 0 6 3 0 6 0
0 0 0 3 0 0 0 0 3 0 0 0
6 0 0 3 0 0 6 0 0 3 0 0
0 0 3 3 0 0 0 0 0 3 0 0
0 0 0 3 3 3 0 0 0 3 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.5454545454545325

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 4 4 0 0
0 0 4 4 0 0 1 0 0 0 4 0 4 0 0
0 0 4 0 4 0 0 0 0 0 0 0 4 0 0
0 4 0 0 4 0 0 0 0 4 0 0 0 4 0
4 0 1 0 4 4 0 0 0 4 0 0 0 4 0
4 4 0 0 0 4 4 4 4 0 0 0 4 4 0
0 4 4 0 0 0 0 0 0 0 0 0 4 0 0
0 0 4 4 0 1 0 0 0 0 0 4 4 0 0
0 0 0 4 4 0 0 1 0 0 0 4 0 0 0
0 0 0 0 4 0 0 0 0 0 4 4 0 0 0
0 0 0 0 4 0 0 0 0 4 0 0 0 1 0
0 1 0 0 0 0 4 4 4 4 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 0.8888888888888857
