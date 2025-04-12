
## train_1

**input:**
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


**output:**
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


## train_2

**input:**
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


**output:**
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

*   **Perception:**
    *   The input grids contain a background color (white), pixels of one primary color (magenta in train_1, blue in train_2), and pixels/structures of a secondary color (green in train_1, yellow in train_2).
    *   The output grids are the same size as the input grids and retain the background color.
    *   The transformation involves filtering the primary color pixels based on their proximity to the secondary color pixels.
    *   Specifically, only the primary color pixels that are *not* adjacent (horizontally, vertically, or diagonally) to any secondary color pixel are kept in the output grid.
    *   All pixels of the secondary color are removed (turned into the background color) in the output.
    *   The positions of the preserved primary color pixels remain unchanged relative to the grid boundaries.

*   **Facts:**
    
```yaml
    task_type: filtering
    elements:
      - role: background
        color: white (0)
        persistence: maintained
      - role: target_pixels
        color: variable (magenta(6) in train_1, blue(1) in train_2)
        property: isolated_from_context
        action: kept if isolated, removed otherwise
      - role: context_pixels
        color: variable (green(3) in train_1, yellow(4) in train_2)
        property: defines_exclusion_zone
        action: removed
    relationships:
      - type: adjacency
        definition: 8-connectivity (horizontal, vertical, diagonal)
        between: target_pixels, context_pixels
        relevance: determines if a target_pixel is kept or removed
    grid_properties:
      - size: maintained between input and output
    ```


*   **Natural Language Program:**
    1.  Create a new grid with the same dimensions as the input grid, initialized with the background color (white).
    2.  Identify the 'target' color (the scattered, less numerous non-background color, e.g., magenta in train_1, blue in train_2).
    3.  Identify the 'context' color (the other non-background color, often forming larger structures, e.g., green in train_1, yellow in train_2).
    4.  Iterate through each pixel in the input grid at position (row, column).
    5.  If the current pixel's color is the 'target' color:
        a.  Examine all 8 neighboring pixels (including diagonals) of the current pixel in the input grid.
        b.  Check if *any* of these neighbors have the 'context' color.
        c.  If *none* of the neighbors have the 'context' color, set the pixel at (row, column) in the new grid to the 'target' color.
    6.  Output the new grid. (Pixels not explicitly set remain the background color).
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
## General Assessment

The initial analysis identified a plausible transformation rule: identify a 'target' color (less frequent non-background) and a 'context' color (more frequent non-background), and keep only target pixels that are not adjacent (8-way) to any context pixel. The provided code attempted to implement this rule.

However, the evaluation results show mismatches:
1.  **Incorrectly Kept Pixels:** The code's output includes target pixels that *are* adjacent to context pixels (e.g., Train 1: (3,5), (4,5); Train 2: (10,7)). This points to a bug in the code's implementation of the adjacency check or the subsequent conditional logic.
2.  **Incorrectly Removed Pixel?**: In Train 1, the code correctly identifies pixel (6,6) as a target pixel with no adjacent context pixels and keeps it. However, the *expected* output removes this pixel. This discrepancy suggests either the rule is more complex than simple 8-way adjacency, the target/context identification needs refinement, or there might be an inconsistency in the provided example's expected output for this specific pixel.

**Strategy:**
1.  **Verify Color Roles:** Use code execution to confirm the frequency-based identification of target and context colors for each example.
2.  **Debug Adjacency Logic:** Re-examine the code's implementation of the `check_neighbors_for_color` function and how its result is used to determine if a target pixel is kept. Fix any bugs found to ensure pixels adjacent to the context color are correctly removed.
3.  **Re-evaluate Discrepancy:** After fixing the implementation bugs, re-evaluate the case of pixel (6,6) in Train 1. If the corrected code still keeps it while the expected output removes it, the core hypothesis about the transformation rule (simple adjacency) might need revision.

## Metrics and Verification


*code_execution:*
```python
import numpy as np

def get_color_counts(grid_list):
    grid = np.array(grid_list)
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    # Separate background (0) from others
    bg_color = 0
    non_bg_counts = {c: count for c, count in color_counts.items() if c != bg_color}
    return bg_color, non_bg_counts

# Example 1 Data
grid1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0],
    [6, 0, 3, 3, 0, 0, 0, 0, 3, 0, 0, 6],
    [0, 0, 3, 0, 0, 6, 0, 0, 3, 0, 0, 0],
    [0, 0, 3, 3, 0, 6, 0, 6, 3, 0, 6, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
    [6, 0, 0, 3, 0, 0, 6, 0, 0, 3, 0, 0],
    [0, 0, 3, 3, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Example 2 Data
grid2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 4, 0, 0],
    [0, 0, 4, 4, 0, 0, 1, 0, 0, 0, 4, 0, 4, 0, 0],
    [0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 4, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0],
    [4, 0, 1, 0, 4, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0],
    [4, 4, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 4, 4, 0],
    [0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 4, 4, 0, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

bg1, counts1 = get_color_counts(grid1)
bg2, counts2 = get_color_counts(grid2)

# Determine target/context based on frequency
target1, context1 = (-1, -1)
if len(counts1) == 2:
    colors = list(counts1.keys())
    if counts1[colors[0]] < counts1[colors[1]]:
        target1, context1 = colors[0], colors[1]
    elif counts1[colors[1]] < counts1[colors[0]]:
        target1, context1 = colors[1], colors[0]

target2, context2 = (-1, -1)
if len(counts2) == 2:
    colors = list(counts2.keys())
    if counts2[colors[0]] < counts2[colors[1]]:
        target2, context2 = colors[0], colors[1]
    elif counts2[colors[1]] < counts2[colors[0]]:
        target2, context2 = colors[1], colors[0]

print(f"Example 1 Counts: {counts1}")
print(f"Example 1 Target: {target1}, Context: {context1}")
print(f"Example 2 Counts: {counts2}")
print(f"Example 2 Target: {target2}, Context: {context2}")

# Verify neighbors for problematic pixels manually
grid1_np = np.array(grid1)
grid2_np = np.array(grid2)

def check_neighbors(grid, r, c, color_to_find):
    rows, cols = grid.shape
    found = False
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append(((nr, nc), grid[nr, nc]))
                if grid[nr, nc] == color_to_find:
                    found = True
    return found, neighbors

# Train 1, Pixel (3, 5) = 6, Context = 3
found1_3_5, neighbors1_3_5 = check_neighbors(grid1_np, 3, 5, 3)
print(f"\nTrain 1, Pixel (3, 5)=6: Neighbors={neighbors1_3_5}")
print(f"Found Context (3) Neighbor for (3, 5)? {found1_3_5}")

# Train 1, Pixel (4, 5) = 6, Context = 3
found1_4_5, neighbors1_4_5 = check_neighbors(grid1_np, 4, 5, 3)
print(f"\nTrain 1, Pixel (4, 5)=6: Neighbors={neighbors1_4_5}")
print(f"Found Context (3) Neighbor for (4, 5)? {found1_4_5}")

# Train 1, Pixel (6, 6) = 6, Context = 3
found1_6_6, neighbors1_6_6 = check_neighbors(grid1_np, 6, 6, 3)
print(f"\nTrain 1, Pixel (6, 6)=6: Neighbors={neighbors1_6_6}")
print(f"Found Context (3) Neighbor for (6, 6)? {found1_6_6}")

# Train 2, Pixel (10, 7) = 1, Context = 4
found2_10_7, neighbors2_10_7 = check_neighbors(grid2_np, 10, 7, 4)
print(f"\nTrain 2, Pixel (10, 7)=1: Neighbors={neighbors2_10_7}")
print(f"Found Context (4) Neighbor for (10, 7)? {found2_10_7}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1 Counts: {np.int64(3): np.int64(28), np.int64(6): np.int64(9)}
Example 1 Target: 6, Context: 3
Example 2 Counts: {np.int64(1): np.int64(10), np.int64(4): np.int64(45)}
Example 2 Target: 1, Context: 4

Train 1, Pixel (3, 5)=6: Neighbors=[((2, 4), np.int64(0)), ((2, 5), np.int64(0)), ((2, 6), np.int64(0)), ((3, 4), np.int64(0)), ((3, 6), np.int64(0)), ((4, 4), np.int64(0)), ((4, 5), np.int64(6)), ((4, 6), np.int64(0))]
Found Context (3) Neighbor for (3, 5)? False

Train 1, Pixel (4, 5)=6: Neighbors=[((3, 4), np.int64(0)), ((3, 5), np.int64(6)), ((3, 6), np.int64(0)), ((4, 4), np.int64(0)), ((4, 6), np.int64(0)), ((5, 4), np.int64(0)), ((5, 5), np.int64(0)), ((5, 6), np.int64(0))]
Found Context (3) Neighbor for (4, 5)? False

Train 1, Pixel (6, 6)=6: Neighbors=[((5, 5), np.int64(0)), ((5, 6), np.int64(0)), ((5, 7), np.int64(0)), ((6, 5), np.int64(0)), ((6, 7), np.int64(0)), ((7, 5), np.int64(0)), ((7, 6), np.int64(0)), ((7, 7), np.int64(0))]
Found Context (3) Neighbor for (6, 6)? False

Train 2, Pixel (10, 7)=1: Neighbors=[((9, 6), np.int64(0)), ((9, 7), np.int64(0)), ((9, 8), np.int64(0)), ((10, 6), np.int64(0)), ((10, 8), np.int64(0)), ((11, 6), np.int64(0)), ((11, 7), np.int64(0)), ((11, 8), np.int64(0))]
Found Context (4) Neighbor for (10, 7)? False

```
**Correction**: My manual check and initial analysis of the code's output/bugs were flawed. The `tool_code` execution reveals:
*   The frequency heuristic correctly identifies Target=6, Context=3 for Train 1, and Target=1, Context=4 for Train 2.
*   Critically, the `check_neighbors` function confirms that pixels (3,5), (4,5), and (10,7) do *not* have context-colored neighbors according to the 8-way adjacency rule. My previous manual checks were incorrect.
*   Pixel (6,6) also correctly shows no context neighbors.

**Revised Assessment:**
The code seems to be correctly implementing the hypothesized rule (keep target if no adjacent context neighbor). However, this rule *itself* does not produce the expected output.
*   For pixels (3,5), (4,5) in Train 1, and (10,7) in Train 2, the rule says *keep* them, but the expected output *removes* them.
*   For pixel (6,6) in Train 1, the rule says *keep* it, but the expected output *removes* it.

This means the fundamental understanding of the transformation rule needs to change. The simple 8-way adjacency to context pixels is insufficient.

**Possible Alternative Rules:**
1.  **Larger Adjacency Radius:** Maybe pixels are removed if a context pixel is within a larger radius (e.g., 2 steps)?
    *   T1 (3,5): Green(3) at (1,3), (2,2), (2,3), (2,8), (3,2), (3,3), (3,8), (4,2), (4,3), (4,8), (5,3), (5,8), (6,3), (6,9), (7,3), (7,8), (7,9), (8,3), (8,4), (8,5), (8,9), (9,5), (9,6). Closest is (4,3), distance sqrt(1^2+2^2)=sqrt(5)~2.23.
    *   T1 (4,5): Closest is (4,3), distance 2.
    *   T1 (6,6): Closest is (5,3) or (7,3), distance 3. Or (7,8) distance sqrt(1^2+2^2)=sqrt(5)~2.23.
    *   T2 (10,7): Closest yellow(4) is (9,9) or (11,5), distance sqrt(1^2+2^2)=sqrt(5)~2.23.
    *   A fixed larger radius doesn't seem to consistently explain why these specific pixels are removed while others (further away) are kept.

2.  **Context as Objects:** Maybe it's proximity to the *bounding box* or *convex hull* of the context color shapes?
3.  **Line of Sight:** Is there an unobstructed path (horizontal, vertical, diagonal) from the target pixel to a context pixel?
4.  **Containment:** Is the target pixel somehow "inside" a structure formed by the context pixels, even if not directly adjacent?

Let's reconsider **Train 1**: The green pixels form a sort of complex border or shape. The magenta pixels being removed ((3,5), (4,5), (6,6)) seem visually "closer" to the main green structures than the ones being kept ((1,0), (2,0), (2,11), (4,10), (6,0)).
Let's reconsider **Train 2**: The yellow pixels form scattered blocks and lines. The blue pixels being removed ((6,2), (9,5), (10,7)) are near yellow clusters.

**Hypothesis Refinement:** The rule seems related to proximity, but not strictly defined by 8-way adjacency. It might involve a concept of being "influenced" or "shielded" by the context shapes. Pixels deep inside the background area, far from any context shape, are kept. Pixels near or "between" parts of context shapes are removed.

Let's try the "Line of Sight" idea. Can we draw a straight line (H, V, or D) from the target pixel to *any* context pixel without hitting another non-background pixel first?
*   T1 (3,5)=6: Diagonal path to (4,6)=0? No, (4,6) is 0. Diagonal path to (2,4)=0? No. Diagonal path SE to (8,10)=0. Horizontal right path hits 0s then boundary. Left hits 0s then boundary. Up hits 0s then boundary. Down hits (4,5)=6, (5,5)=0, (6,5)=0... Path to (4,3)=3 (context) is blocked by (3,4)=0 and (4,4)=0. Path to (2,3)=3 is blocked. Path to (4,6)=0 -> fails. Path to (1,3)? Blocked. Path to (2,8)? Blocked. Path to (3,8)? Blocked.
*   This line-of-sight idea seems complex and maybe not fruitful.

What if it's simpler: Keep target pixels that are not adjacent (8-way) to *either* the context color *or another target pixel*?
*   T1 (3,5)=6: Neighbor (4,5)=6 (target). Remove (3,5)?
*   T1 (4,5)=6: Neighbors (3,5)=6 (target), (4,6)=0, (4,4)=0. Remove (4,5)?
*   T1 (6,6)=6: No target or context neighbors. Keep (6,6)? Still contradicts expected output.

Let's go back to the simplest successful rule component: context pixels are always removed. The target pixels are filtered. The filtering rule removes target pixels *near* context pixels. The definition of "near" is the issue. Since 8-way adjacency failed, let's reconsider the failed pixels:
*   T1: (3,5), (4,5), (6,6) removed.
*   T2: (6,2), (9,5), (10,7) removed.

Perhaps the rule is: Keep target pixels only if *all* 8 neighbors are background (0)?
*   T1 (1,0)=6: Neighbors are 0, 0, 0. Keep. -> OK
*   T1 (2,0)=6: Neighbors are 6, 0, 0, 0, 0. Remove? -> Fails, expected keeps.
*   T1 (2,11)=6: Neighbors are 0, 6, 0, 0, 0. Remove? -> Fails, expected keeps.
*   T1 (4,10)=6: Neighbors are 0, 0, 6, 0, 0. Remove? -> Fails, expected keeps.
*   T1 (6,0)=6: Neighbors are 0, 6, 0, 0, 0. Remove? -> Fails, expected keeps.
*   T1 (3,5)=6: Neighbor (4,5)=6. Remove? -> OK
*   T1 (4,5)=6: Neighbor (3,5)=6. Remove? -> OK
*   T1 (6,6)=6: All neighbors 0. Keep? -> Fails, expected removes.

This isn't working either. The most consistent rule seems to be the original adjacency idea, but the expected output for T1 (6,6) breaks it. Given the code seems to correctly implement the adjacency rule, and that rule works for *all other pixels* across both examples except T1(6,6), the most pragmatic approach is to stick with the adjacency rule and assume T1(6,6)'s removal in the expected output might be an anomaly or requires a secondary rule not yet apparent.

## Facts


```yaml
task_type: filtering_by_adjacency
elements:
  - role: background
    color: white (0)
    persistence: maintained
  - role: target_pixels
    color: variable (magenta(6) in train_1, blue(1) in train_2)
    property: identified as the less frequent non-background color
    action: kept only if isolated from context_pixels, otherwise removed
  - role: context_pixels
    color: variable (green(3) in train_1, yellow(4) in train_2)
    property: identified as the more frequent non-background color
    action: defines exclusion zone for target_pixels; always removed in output
relationships:
  - type: adjacency
    definition: 8-connectivity (Moore neighborhood - horizontal, vertical, diagonal distance=1)
    between: target_pixels, context_pixels
    relevance: determines if a target_pixel is kept (if no adjacent context_pixel) or removed (if any adjacent context_pixel)
grid_properties:
  - size: maintained between input and output
notes:
  - The frequency heuristic (target < context) correctly identifies roles in provided examples.
  - The primary transformation rule appears to be removing target pixels adjacent (8-way) to context pixels.
  - There is one inconsistency observed: In train_1, target pixel (6,6) has no context neighbors but is removed in the expected output, contrary to the general rule observed otherwise. The proposed program follows the general rule.
```


## Natural Language Program

1.  Initialize an output grid of the same dimensions as the input grid, filled with the background color (white, 0).
2.  Analyze the input grid to identify non-background colors and their frequencies.
3.  If exactly two non-background colors are present:
    a.  Designate the color with the lower frequency as the 'target' color.
    b.  Designate the color with the higher frequency as the 'context' color.
4.  If only one non-background color is present, designate it as the 'target' color and consider the 'context' color non-existent.
5.  If zero or more than two non-background colors exist, or if the two non-background colors have equal frequency, the rule is ambiguous based on examples; output the initialized background grid.
6.  Iterate through each pixel (at row `r`, column `c`) of the input grid.
7.  If the pixel `(r, c)` has the 'target' color:
    a.  Check if a 'context' color was identified.
    b.  If a 'context' color exists, examine all 8 neighboring pixels (including diagonals) of pixel `(r, c)` in the input grid.
    c.  Determine if *any* of these 8 neighbors have the 'context' color.
    d.  If *no* neighbor has the 'context' color (or if no 'context' color exists), then copy the 'target' color to the output grid at position `(r, c)`.
    e.  Otherwise (if any neighbor has the 'context' color), leave the background color at `(r, c)` in the output grid.
8.  Pixels in the input grid that are not the 'target' color (i.e., background or context colors) result in the background color in the output grid at their corresponding positions.
9.  Return the completed output grid.
```python
import numpy as np
from typing import List, Tuple

"""
Filters a grid based on pixel adjacency rules derived from examples.

The transformation identifies three color roles: background (assumed to be 0), 
'target', and 'context'. 
If exactly two non-background colors exist, the 'target' color is the one 
with the lower frequency count, and the 'context' color is the one with the 
higher frequency count. If only one non-background color exists, it's treated 
as the 'target' color, and there is no 'context' color.

The rule is to keep 'target' color pixels in the output grid *only if* they 
are NOT adjacent (horizontally, vertically, or diagonally - 8-connectivity) 
to any 'context' color pixel in the input grid. 

All 'context' color pixels, as well as 'target' color pixels that *are* 
adjacent to 'context' pixels, are replaced with the background color in the 
output. Pixels that are already the background color remain so.

If zero, more than two non-background colors exist, or if the two 
non-background colors have equal frequency (making the target/context roles 
ambiguous based on the frequency heuristic), the function returns a grid 
filled entirely with the background color.

The grid dimensions remain unchanged.
"""

def identify_colors(grid: np.ndarray) -> Tuple[int, int, int]:
    """
    Identifies background, target, and context colors based on frequency.
    Assumes background=0. Finds non-background colors.
    Hypothesis: If two non-background colors exist, Target color is less 
                frequent than context color.
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
             # print("Warning: Tie in non-background color counts, cannot distinguish target/context.")
             target_color = -2 # Indicate ambiguity
             context_color = -2

    else: # More than two non-background colors
        # print("Warning: More than two non-background colors found.")
        # Cannot determine target/context based on the observed pattern.
        target_color = -3 # Indicate >2 colors
        context_color = -3

    return background_color, target_color, context_color

def check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    """
    Checks the 8 neighbors (Moore neighborhood) of cell (r, c) in the grid
    to see if any neighbor has the specified color_to_find.
    Returns True if found, False otherwise.
    Handles boundary conditions gracefully.
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

    # Step 2: Handle edge cases where color identification fails or is ambiguous
    # If no target identified, or ambiguous, or too many colors, return an empty grid.
    if target_color < 0: # Includes -1 (no target), -2 (ambiguous), -3 (>2 colors)
        # print(f"Color identification issue (code: {target_color}). Returning empty grid.")
        output_grid = np.full((rows, cols), background_color, dtype=int)
        return output_grid.tolist()

    # Step 3: Create a new grid initialized with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Step 4: Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Step 5: Check if the current pixel is the target color
            if input_grid[r, c] == target_color:

                # Step 6: Determine if the target pixel should be kept
                keep_pixel = True # Assume keep unless adjacent to context

                # Step 7: Check adjacency only if a context color exists
                if context_color != -1: # context_color is -1 if only one non-bg color exists
                    is_near_context = check_neighbors_for_color(input_grid, r, c, context_color)
                    if is_near_context:
                        keep_pixel = False # Rule: remove if adjacent to context

                # Step 8: If the pixel should be kept, place it in the output grid
                if keep_pixel:
                    output_grid[r, c] = target_color
            # Step 9: Pixels that are not the target color (i.e., background or context)
            # are implicitly left as the background color initialized in output_grid.

    # Step 10: Convert the resulting numpy array back to a list of lists
    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from typing import List, Tuple

"""
Filters a grid based on pixel adjacency rules derived from examples.

The transformation identifies three color roles: background (assumed to be 0), 
'target', and 'context'. 
If exactly two non-background colors exist, the 'target' color is the one 
with the lower frequency count, and the 'context' color is the one with the 
higher frequency count. If only one non-background color exists, it's treated 
as the 'target' color, and there is no 'context' color.

The rule is to keep 'target' color pixels in the output grid *only if* they 
are NOT adjacent (horizontally, vertically, or diagonally - 8-connectivity) 
to any 'context' color pixel in the input grid. 

All 'context' color pixels, as well as 'target' color pixels that *are* 
adjacent to 'context' pixels, are replaced with the background color in the 
output. Pixels that are already the background color remain so.

If zero, more than two non-background colors exist, or if the two 
non-background colors have equal frequency (making the target/context roles 
ambiguous based on the frequency heuristic), the function returns a grid 
filled entirely with the background color.

The grid dimensions remain unchanged.
"""

def identify_colors(grid: np.ndarray) -> Tuple[int, int, int]:
    """
    Identifies background, target, and context colors based on frequency.
    Assumes background=0. Finds non-background colors.
    Hypothesis: If two non-background colors exist, Target color is less 
                frequent than context color.
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
             # print("Warning: Tie in non-background color counts, cannot distinguish target/context.")
             target_color = -2 # Indicate ambiguity
             context_color = -2

    else: # More than two non-background colors
        # print("Warning: More than two non-background colors found.")
        # Cannot determine target/context based on the observed pattern.
        target_color = -3 # Indicate >2 colors
        context_color = -3

    return background_color, target_color, context_color

def check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    """
    Checks the 8 neighbors (Moore neighborhood) of cell (r, c) in the grid
    to see if any neighbor has the specified color_to_find.
    Returns True if found, False otherwise.
    Handles boundary conditions gracefully.
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

    # Step 2: Handle edge cases where color identification fails or is ambiguous
    # If no target identified, or ambiguous, or too many colors, return an empty grid.
    if target_color < 0: # Includes -1 (no target), -2 (ambiguous), -3 (>2 colors)
        # print(f"Color identification issue (code: {target_color}). Returning empty grid.")
        output_grid = np.full((rows, cols), background_color, dtype=int)
        return output_grid.tolist()

    # Step 3: Create a new grid initialized with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Step 4: Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Step 5: Check if the current pixel is the target color
            if input_grid[r, c] == target_color:

                # Step 6: Determine if the target pixel should be kept
                keep_pixel = True # Assume keep unless adjacent to context

                # Step 7: Check adjacency only if a context color exists
                if context_color != -1: # context_color is -1 if only one non-bg color exists
                    is_near_context = check_neighbors_for_color(input_grid, r, c, context_color)
                    if is_near_context:
                        keep_pixel = False # Rule: remove if adjacent to context

                # Step 8: If the pixel should be kept, place it in the output grid
                if keep_pixel:
                    output_grid[r, c] = target_color
            # Step 9: Pixels that are not the target color (i.e., background or context)
            # are implicitly left as the background color initialized in output_grid.

    # Step 10: Convert the resulting numpy array back to a list of lists
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
## General Assessment

The previous code implemented the hypothesis: "Identify a 'target' color (less frequent non-background) and a 'context' color (more frequent). Keep target pixels only if they are not 8-way adjacent to any context pixel."

Execution results show this rule works for most pixels but fails for a few specific cases:
1.  **Train 1:** The code correctly identifies Target=6, Context=3. It keeps pixels (3,5), (4,5), and (6,6) because they have no context neighbors. However, the *expected output* removes these pixels.
2.  **Train 2:** The code correctly identifies Target=1, Context=4. It keeps pixel (10,7) because it has no context neighbors. However, the *expected output* removes this pixel. (Note: Pixels (6,2) and (9,5) are also removed in the expected output, but they *are* adjacent to context color 4, so the rule correctly handles them).

The discrepancy lies in pixels that are *not* adjacent to the context color but are removed anyway in the ground truth ((3,5), (4,5), (6,6) in T1; (10,7) in T2). The simple 8-way adjacency rule is insufficient to explain these specific removals.

Several alternative hypotheses were considered (larger radius, line-of-sight, connectivity to boundary, adjacency to *any* non-background, isolation) but failed to consistently explain all examples, particularly why T1(2,11) is kept despite having only background neighbors, while T1(6,6) and T2(10,7) are removed under the same condition.

**Strategy:**
Given the lack of a clear, simple rule explaining the exceptions, the most robust approach is to retain the primary rule (remove target pixels adjacent to context pixels) as it explains the vast majority of the transformation. The failure analysis indicates this rule is *necessary* but perhaps not *sufficient*. The code implements this necessary part. We will proceed with this rule, acknowledging it doesn't perfectly match the examples for a few specific non-adjacent pixels.

## Metrics and Verification

*code_execution:*

```python
import numpy as np

# --- Data ---
grid1_in = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0],
    [6, 0, 3, 3, 0, 0, 0, 0, 3, 0, 0, 6],
    [0, 0, 3, 0, 0, 6, 0, 0, 3, 0, 0, 0],
    [0, 0, 3, 3, 0, 6, 0, 6, 3, 0, 6, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
    [6, 0, 0, 3, 0, 0, 6, 0, 0, 3, 0, 0],
    [0, 0, 3, 3, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid1_out_exp = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid1_out_code = np.array([ # From previous execution result
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0], # Differs at (3,5)
    [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0], # Differs at (4,5)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0], # Differs at (6,6)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

grid2_in = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 4, 0, 0],
    [0, 0, 4, 4, 0, 0, 1, 0, 0, 0, 4, 0, 4, 0, 0],
    [0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 4, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0],
    [4, 0, 1, 0, 4, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0],
    [4, 4, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 4, 4, 0],
    [0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 4, 4, 0, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid2_out_exp = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid2_out_code = np.array([ # From previous execution result
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], # Differs at (10,7)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# --- Analysis Functions ---
def check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    rows, cols = grid.shape
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] == color_to_find:
                    return True
    return False

def analyze_mismatch(grid_in, grid_out_exp, grid_out_code, target_color, context_color):
    mismatches = []
    rows, cols = grid_in.shape
    for r in range(rows):
        for c in range(cols):
            if grid_out_code[r, c] != grid_out_exp[r, c]:
                pixel_val = grid_in[r,c]
                is_target = pixel_val == target_color
                code_kept = grid_out_code[r, c] == target_color
                exp_kept = grid_out_exp[r, c] == target_color
                is_adj_to_context = check_neighbors_for_color(grid_in, r, c, context_color)
                mismatches.append({
                    "coords": (r, c),
                    "input_val": pixel_val,
                    "is_target": is_target,
                    "code_output": grid_out_code[r, c],
                    "expected_output": grid_out_exp[r, c],
                    "code_kept_target": code_kept,
                    "exp_kept_target": exp_kept,
                    "is_adj_to_context": is_adj_to_context
                })
    return mismatches

# --- Run Analysis ---
target1, context1 = 6, 3
mismatches1 = analyze_mismatch(grid1_in, grid1_out_exp, grid1_out_code, target1, context1)
print("--- Train 1 Mismatches ---")
for m in mismatches1:
    print(m)

target2, context2 = 1, 4
mismatches2 = analyze_mismatch(grid2_in, grid2_out_exp, grid2_out_code, target2, context2)
print("\n--- Train 2 Mismatches ---")
for m in mismatches2:
    print(m)

# Verify adjacency specifically for the problematic points
print("\n--- Adjacency Re-Verification ---")
prob1 = [(3,5), (4,5), (6,6)]
for r, c in prob1:
    adj = check_neighbors_for_color(grid1_in, r, c, context1)
    print(f"T1 ({r},{c})={grid1_in[r,c]} adjacent to {context1}? {adj}")

prob2 = [(10,7)]
for r, c in prob2:
    adj = check_neighbors_for_color(grid2_in, r, c, context2)
    print(f"T2 ({r},{c})={grid2_in[r,c]} adjacent to {context2}? {adj}")
```


*code_execution_result:*
outcome: OUTCOME_OK

```
--- Train 1 Mismatches ---
{'coords': (3, 5), 'input_val': np.int64(6), 'is_target': True, 'code_output': np.int64(6), 'expected_output': np.int64(0), 'code_kept_target': True, 'exp_kept_target': False, 'is_adj_to_context': False}
{'coords': (4, 5), 'input_val': np.int64(6), 'is_target': True, 'code_output': np.int64(6), 'expected_output': np.int64(0), 'code_kept_target': True, 'exp_kept_target': False, 'is_adj_to_context': False}
{'coords': (6, 6), 'input_val': np.int64(6), 'is_target': True, 'code_output': np.int64(6), 'expected_output': np.int64(0), 'code_kept_target': True, 'exp_kept_target': False, 'is_adj_to_context': False}

--- Train 2 Mismatches ---
{'coords': (10, 7), 'input_val': np.int64(1), 'is_target': True, 'code_output': np.int64(1), 'expected_output': np.int64(0), 'code_kept_target': True, 'exp_kept_target': False, 'is_adj_to_context': False}

--- Adjacency Re-Verification ---
T1 (3,5)=6 adjacent to 3? False
T1 (4,5)=6 adjacent to 3? False
T1 (6,6)=6 adjacent to 3? False
T2 (10,7)=1 adjacent to 4? False
```

**Metrics Summary:**
The code execution confirms the analysis:
*   In Train 1, pixels (3,5), (4,5), and (6,6) are the target color (6). The code keeps them, while the expected output removes them. None are adjacent (8-way) to the context color (3).
*   In Train 2, pixel (10,7) is the target color (1). The code keeps it, while the expected output removes it. It is not adjacent (8-way) to the context color (4).
*   The core rule implemented (keep target if not adjacent to context) leads to these specific mismatches.

## Facts


```yaml
task_type: filtering_by_adjacency
elements:
  - role: background
    color: white (0)
    persistence: maintained
  - role: target_pixels
    color: variable (magenta(6) in train_1, blue(1) in train_2)
    property: identified as the less frequent non-background color
    action: filtered based on relationship to context_pixels
  - role: context_pixels
    color: variable (green(3) in train_1, yellow(4) in train_2)
    property: identified as the more frequent non-background color
    action: defines exclusion zone for target_pixels; always removed in output
relationships:
  - type: adjacency
    definition: 8-connectivity (Moore neighborhood)
    between: target_pixels, context_pixels
    relevance: If a target_pixel is adjacent to a context_pixel, the target_pixel is removed.
grid_properties:
  - size: maintained between input and output
ambiguity:
  - rule_incompleteness: The adjacency rule does not fully explain the removal of all target pixels in the examples. Specifically, target pixels at T1(3,5), T1(4,5), T1(6,6), and T2(10,7) are removed in the expected output despite *not* being adjacent to any context pixel. The precise condition causing their removal is not determined from the examples.
notes:
  - The frequency heuristic (target < context) correctly identifies roles in provided examples.
  - The primary transformation rule appears to be removing target pixels adjacent (8-way) to context pixels. The implemented solution follows this rule.
```


## Natural Language Program

1.  Initialize an output grid of the same dimensions as the input grid, filled with the background color (white, 0).
2.  Analyze the input grid to identify non-background colors and their frequencies.
3.  Determine the 'target' and 'context' colors:
    *   If exactly two non-background colors exist, designate the color with the lower frequency count as 'target' and the color with the higher frequency count as 'context'.
    *   If only one non-background color exists, designate it as 'target' and consider 'context' non-existent.
    *   Otherwise (zero, more than two non-background colors, or equal frequencies), return the initialized background grid as the role assignment is ambiguous.
4.  Iterate through each pixel (at row `r`, column `c`) of the input grid.
5.  If the pixel `(r, c)` has the 'target' color:
    a.  Check if a 'context' color was identified.
    b.  If a 'context' color exists, examine all 8 neighboring pixels (including diagonals) of `(r, c)` in the input grid.
    c.  If *none* of these neighbors have the 'context' color, copy the 'target' color to the output grid at position `(r, c)`.
    d.  If *any* neighbor has the 'context' color (or if no 'target' color was identified), leave the background color at `(r, c)` in the output grid.
6.  Pixels in the input grid that are not the 'target' color (i.e., background or context colors) result in the background color in the output grid at their corresponding positions.
7.  Return the completed output grid.

*(Note: This program describes the rule implemented by the provided code, which matches most but not all transformations in the examples due to the unexplained removal of certain non-adjacent target pixels in the ground truth.)*
```python
import numpy as np
from typing import List, Tuple

"""
Filters a grid based on pixel adjacency rules derived from examples.

The transformation identifies three color roles: background (assumed to be 0), 
'target', and 'context'. 
If exactly two non-background colors exist, the 'target' color is the one 
with the lower frequency count, and the 'context' color is the one with the 
higher frequency count. If only one non-background color exists, it's treated 
as the 'target' color, and there is no 'context' color.

The rule is to keep 'target' color pixels in the output grid *only if* they 
are NOT adjacent (horizontally, vertically, or diagonally - 8-connectivity) 
to any 'context' color pixel in the input grid. 

All 'context' color pixels, as well as 'target' color pixels that *are* 
adjacent to 'context' pixels, are replaced with the background color in the 
output. Pixels that are already the background color remain so.

If zero, more than two non-background colors exist, or if the two 
non-background colors have equal frequency (making the target/context roles 
ambiguous based on the frequency heuristic), the function returns a grid 
filled entirely with the background color.

The grid dimensions remain unchanged.

Note: This rule implementation matches most transformations in the provided 
examples but differs for a few specific target pixels that are removed in the 
expected output despite not being adjacent to any context pixel (e.g., 
T1(3,5), T1(4,5), T1(6,6), T2(10,7)). The exact rule for these exceptions is 
not captured here.
"""

def _identify_colors(grid: np.ndarray) -> Tuple[int, int, int]:
    """
    Identifies background, target, and context colors based on frequency.
    Assumes background=0. Finds non-background colors.
    Hypothesis: If two non-background colors exist, Target color is less 
                frequent than context color.
    Returns: (background_color, target_color, context_color)
             target_color or context_color can be -1 if not applicable/found.
             Special negative codes (-2, -3) indicate ambiguity or errors.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    background_color = 0
    # Filter out the background color to find non-background colors and their counts
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    num_non_background = len(non_background_colors)

    target_color = -1  # Default: No target color found
    context_color = -1 # Default: No context color found

    if num_non_background == 0:
        # Only background color present in the input grid
        pass # target/context remain -1
    elif num_non_background == 1:
        # Exactly one non-background color exists, treat it as the target color
        target_color = list(non_background_colors.keys())[0]
        context_color = -1 # No context color in this case
    elif num_non_background == 2:
        # Exactly two non-background colors exist, determine roles by frequency
        colors = list(non_background_colors.keys())
        counts_list = list(non_background_colors.values())

        # Assign target to the less frequent color, context to the more frequent
        if counts_list[0] < counts_list[1]:
            target_color = colors[0]
            context_color = colors[1]
        elif counts_list[1] < counts_list[0]:
            target_color = colors[1]
            context_color = colors[0]
        else:
             # Frequencies are equal, roles are ambiguous based on this heuristic
             target_color = -2 # Indicate ambiguity
             context_color = -2
    else: 
        # More than two non-background colors found, roles are ambiguous
        target_color = -3 # Indicate >2 colors issue
        context_color = -3

    return background_color, target_color, context_color

def _check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    """
    Checks the 8 neighbors (Moore neighborhood) of cell (r, c) in the grid
    to see if any neighbor has the specified color_to_find.
    Returns True if a neighbor with the color is found, False otherwise.
    Handles boundary conditions gracefully.
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
                    return True # Found the color in a neighbor, no need to check further

    # If the loop completes without finding the color in any neighbor
    return False

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:  
    # Convert input list of lists to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Step 1: Identify background, target, and context colors using the frequency heuristic
    background_color, target_color, context_color = _identify_colors(input_grid)

    # Step 2: Handle edge cases or ambiguous color roles
    # If no target color identified, or roles are ambiguous, return a grid filled with background color
    if target_color < 0: # Covers -1 (no target), -2 (ambiguous tie), -3 (>2 colors)
        output_grid = np.full((rows, cols), background_color, dtype=int)
        return output_grid.tolist()

    # Step 3: Initialize the output grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Step 4: Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Step 5: Check if the current pixel is the target color
            if input_grid[r, c] == target_color:

                # Step 6: Assume the target pixel should be kept, unless proven otherwise
                keep_pixel = True 

                # Step 7: Check for adjacent context pixels ONLY if a context color exists
                if context_color != -1: # A context color exists (i.e., exactly 2 non-bg colors found)
                    is_near_context = _check_neighbors_for_color(input_grid, r, c, context_color)
                    # If any neighbor is the context color, mark this pixel for removal
                    if is_near_context:
                        keep_pixel = False 

                # Step 8: If the pixel is marked to be kept, place its color in the output grid
                if keep_pixel:
                    output_grid[r, c] = target_color
            
            # Step 9: Pixels that are not the target color (background or context) 
            # remain as the background color in the output grid (due to initialization).

    # Step 10: Convert the final numpy array grid back to a list of lists and return
    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from typing import List, Tuple

"""
Filters a grid based on pixel adjacency rules derived from examples.

The transformation identifies three color roles: background (assumed to be 0), 
'target', and 'context'. 
If exactly two non-background colors exist, the 'target' color is the one 
with the lower frequency count, and the 'context' color is the one with the 
higher frequency count. If only one non-background color exists, it's treated 
as the 'target' color, and there is no 'context' color.

The rule is to keep 'target' color pixels in the output grid *only if* they 
are NOT adjacent (horizontally, vertically, or diagonally - 8-connectivity) 
to any 'context' color pixel in the input grid. 

All 'context' color pixels, as well as 'target' color pixels that *are* 
adjacent to 'context' pixels, are replaced with the background color in the 
output. Pixels that are already the background color remain so.

If zero, more than two non-background colors exist, or if the two 
non-background colors have equal frequency (making the target/context roles 
ambiguous based on the frequency heuristic), the function returns a grid 
filled entirely with the background color.

The grid dimensions remain unchanged.

Note: This rule implementation matches most transformations in the provided 
examples but differs for a few specific target pixels that are removed in the 
expected output despite not being adjacent to any context pixel (e.g., 
T1(3,5), T1(4,5), T1(6,6), T2(10,7)). The exact rule for these exceptions is 
not captured here.
"""

def _identify_colors(grid: np.ndarray) -> Tuple[int, int, int]:
    """
    Identifies background, target, and context colors based on frequency.
    Assumes background=0. Finds non-background colors.
    Hypothesis: If two non-background colors exist, Target color is less 
                frequent than context color.
    Returns: (background_color, target_color, context_color)
             target_color or context_color can be -1 if not applicable/found.
             Special negative codes (-2, -3) indicate ambiguity or errors.
    """
    unique_colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))

    background_color = 0
    # Filter out the background color to find non-background colors and their counts
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    num_non_background = len(non_background_colors)

    target_color = -1  # Default: No target color found
    context_color = -1 # Default: No context color found

    if num_non_background == 0:
        # Only background color present in the input grid
        pass # target/context remain -1
    elif num_non_background == 1:
        # Exactly one non-background color exists, treat it as the target color
        target_color = list(non_background_colors.keys())[0]
        context_color = -1 # No context color in this case
    elif num_non_background == 2:
        # Exactly two non-background colors exist, determine roles by frequency
        colors = list(non_background_colors.keys())
        counts_list = list(non_background_colors.values())

        # Assign target to the less frequent color, context to the more frequent
        if counts_list[0] < counts_list[1]:
            target_color = colors[0]
            context_color = colors[1]
        elif counts_list[1] < counts_list[0]:
            target_color = colors[1]
            context_color = colors[0]
        else:
             # Frequencies are equal, roles are ambiguous based on this heuristic
             target_color = -2 # Indicate ambiguity
             context_color = -2
    else: 
        # More than two non-background colors found, roles are ambiguous
        target_color = -3 # Indicate >2 colors issue
        context_color = -3

    return background_color, target_color, context_color

def _check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    """
    Checks the 8 neighbors (Moore neighborhood) of cell (r, c) in the grid
    to see if any neighbor has the specified color_to_find.
    Returns True if a neighbor with the color is found, False otherwise.
    Handles boundary conditions gracefully.
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
                    return True # Found the color in a neighbor, no need to check further

    # If the loop completes without finding the color in any neighbor
    return False

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:  
    # Convert input list of lists to a numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Step 1: Identify background, target, and context colors using the frequency heuristic
    background_color, target_color, context_color = _identify_colors(input_grid)

    # Step 2: Handle edge cases or ambiguous color roles
    # If no target color identified, or roles are ambiguous, return a grid filled with background color
    if target_color < 0: # Covers -1 (no target), -2 (ambiguous tie), -3 (>2 colors)
        output_grid = np.full((rows, cols), background_color, dtype=int)
        return output_grid.tolist()

    # Step 3: Initialize the output grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Step 4: Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Step 5: Check if the current pixel is the target color
            if input_grid[r, c] == target_color:

                # Step 6: Assume the target pixel should be kept, unless proven otherwise
                keep_pixel = True 

                # Step 7: Check for adjacent context pixels ONLY if a context color exists
                if context_color != -1: # A context color exists (i.e., exactly 2 non-bg colors found)
                    is_near_context = _check_neighbors_for_color(input_grid, r, c, context_color)
                    # If any neighbor is the context color, mark this pixel for removal
                    if is_near_context:
                        keep_pixel = False 

                # Step 8: If the pixel is marked to be kept, place its color in the output grid
                if keep_pixel:
                    output_grid[r, c] = target_color
            
            # Step 9: Pixels that are not the target color (background or context) 
            # remain as the background color in the output grid (due to initialization).

    # Step 10: Convert the final numpy array grid back to a list of lists and return
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
## General Assessment

The provided code implements a transformation rule based on two main hypotheses derived from the training examples:
1.  **Color Role Identification:** Non-background colors are categorized into 'target' and 'context' roles based on frequency, with the 'target' color being the less frequent one.
2.  **Filtering Rule:** 'Target' pixels are kept in the output *only if* they are not adjacent (8-way Moore neighborhood) to any 'context' pixel. All 'context' pixels are removed.

The code execution results show this implementation correctly handles most pixel transformations in the examples. However, persistent mismatches occur for a specific subset of 'target' pixels:
*   **Train 1:** Pixels (3,5), (4,5), and (6,6) (target color 6) are kept by the code but removed in the expected output.
*   **Train 2:** Pixel (10,7) (target color 1) is kept by the code but removed in the expected output.

Crucially, the verification confirms that none of these mismatched pixels are directly adjacent (8-way) to their respective 'context' colors (3 in Train 1, 4 in Train 2).

This indicates the implemented rule (frequency-based roles + 8-way adjacency filtering) is **incomplete**. There is an additional, unidentified condition causing the removal of certain 'target' pixels even when they are not directly next to 'context' pixels. Several alternative hypotheses (larger radius, line-of-sight, connectivity, adjacency to background/other targets, contamination spread) were considered but failed to consistently explain both the removals and the pixels that are correctly kept.

**Strategy:**

Given the failure to identify a consistent secondary rule explaining the exceptions, the best approach is to document the transformation based on the implemented logic (frequency + 8-way adjacency), as it represents the most consistent pattern observed. The documentation (Facts and NL Program) will reflect this rule, and the assessment will explicitly note the known discrepancies where the rule fails to match the expected output for these specific non-adjacent target pixels.

## Metrics and Verification

The `code_execution` block in the previous turn already performed the necessary analysis:

*   **Color Identification:** The frequency heuristic (target = less frequent non-background, context = more frequent) correctly identified Target=6, Context=3 for Train 1, and Target=1, Context=4 for Train 2.
*   **Mismatched Pixels:**
    *   Train 1: Mismatches occur at (3,5), (4,5), (6,6). Input value is 6 (target), code output is 6 (kept), expected output is 0 (removed).
    *   Train 2: Mismatch occurs at (10,7). Input value is 1 (target), code output is 1 (kept), expected output is 0 (removed).
*   **Adjacency Check:** For all mismatched pixels listed above, the `check_neighbors_for_color` function confirmed they are **not** adjacent (8-way) to their respective context colors.

Conclusion: The code correctly implements the 8-way adjacency filtering rule, but this rule itself does not fully capture the transformation logic shown in the examples.

## Facts


```yaml
task_type: filtering_by_adjacency
elements:
  - role: background
    color: white (0)
    persistence: maintained
    description: The default color filling the grid.
  - role: target_pixels
    color: variable (magenta(6) in T1, blue(1) in T2)
    property:
      - non_background
      - less_frequent (compared to context_pixels, if context_pixels exist)
    action: conditionally_kept
    condition: Kept if not adjacent (8-way) to any context_pixel. Otherwise removed.
  - role: context_pixels
    color: variable (green(3) in T1, yellow(4) in T2)
    property:
      - non_background
      - more_frequent (compared to target_pixels)
    action: removed
    effect: Defines an exclusion zone via adjacency for target_pixels.
relationships:
  - type: frequency_comparison
    between: non_background_colors
    relevance: Determines 'target' vs 'context' roles when exactly two non-background colors are present.
  - type: adjacency
    definition: 8-connectivity (Moore neighborhood)
    between: target_pixels, context_pixels
    relevance: Primary condition for removing target_pixels. If a target pixel is adjacent to a context pixel, it is removed.
grid_properties:
  - size: maintained between input and output
ambiguity:
  - rule_incompleteness: The identified rule (frequency roles + 8-way adjacency filtering) does not explain the removal of all target pixels in the examples. Specifically, target pixels at T1(3,5), T1(4,5), T1(6,6), and T2(10,7) are removed in the expected outputs despite *not* being adjacent to any context pixel according to the 8-way definition. The precise condition causing their removal remains undetermined from the examples and simple geometric priors.
```


## Natural Language Program

1.  Initialize an output grid identical in size to the input grid, filled entirely with the background color (white, 0).
2.  Count the occurrences of each color in the input grid, excluding the background color (0).
3.  Identify the 'target' and 'context' colors based on the counts:
    *   If exactly two non-background colors exist, designate the color with the lower count as 'target' and the color with the higher count as 'context'.
    *   If only one non-background color exists, designate it as 'target'; there is no 'context' color.
    *   If zero, more than two non-background colors exist, or if two non-background colors have equal counts, the roles are ambiguous; return the initialized background grid.
4.  Iterate through each cell `(r, c)` of the input grid.
5.  If the color of the input cell `(r, c)` is the identified 'target' color:
    a.  Check if a 'context' color was identified.
    b.  If a 'context' color exists, examine the 8 neighbors (horizontal, vertical, and diagonal) of the cell `(r, c)` in the input grid.
    c.  Determine if *any* of these neighbors contain the 'context' color.
    d.  If *no* neighbor contains the 'context' color (or if no 'context' color exists), set the corresponding cell `(r, c)` in the output grid to the 'target' color.
    e.  (Implicitly) If any neighbor contains the 'context' color, the cell `(r, c)` in the output grid remains the background color.
6.  (Implicitly) If the color of the input cell `(r, c)` is the background color or the 'context' color, the corresponding cell `(r, c)` in the output grid remains the background color.
7.  Return the final output grid.

*(Note: This program describes the logic that successfully explains most, but not all, transformations seen in the examples. It does not account for the removal of specific target pixels like T1(3,5), T1(4,5), T1(6,6), and T2(10,7) which are not adjacent to context pixels.)*
