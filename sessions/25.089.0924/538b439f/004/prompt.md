
Previous Code:
```python
import numpy as np
from collections import Counter

"""
This program transforms an input grid based on reflection rules across a central axis.
The specific reflection behavior depends on the orientation and color of the axis,
the background color, and the color of the object being reflected.

The transformation identifies a single-color central axis (either horizontal or vertical)
and the primary background color. Based on the characteristics of the axis and background,
it applies specific reflection rules:

Rule Set 1 (Detected in train_1: Vertical Blue Axis (1), Red Background (2)):
1. Identify Azure (8) pixels located to the left of the axis.
2. Reflect these Azure pixels across the axis to the right side, overwriting existing pixels with Azure (8).
3. For each row containing an original left-side Azure pixel:
   - Find the rightmost column (`max_c_orig`) of the original Azure shape in that row.
   - Find the leftmost column (`min_c_refl`) of the reflected Azure shape in that row.
   - Fill the cells between `max_c_orig` and the axis (exclusive) with Blue (1).
   - Fill the cells between the axis and `min_c_refl` (exclusive) with Blue (1).
4. All other pixels (including the axis and background) remain unchanged unless overwritten by the reflection or filling steps.

Rule Set 2 (Detected in train_2: Horizontal Red Axis (2), Azure Background (8)):
1. Identify Green (3) pixels located below the axis.
2. Reflect these Green pixels across the axis to the upper side, overwriting existing pixels with Green (3).
3. Identify Blue (1) pixels located above the axis.
4. For each Blue (1) pixel above the axis:
   - Calculate its reflected coordinates below the axis.
   - Check if the *source* Blue (1) pixel is "isolated" (has no orthogonal neighbors of the same Blue color).
   - Check if the pixel at the *reflected coordinates* in the *original input grid* is the background color (Azure 8).
   - If *both* conditions (source is isolated Blue, destination was background) are true, change the pixel at the reflected coordinates in the *output grid* to Red (2).
   - Otherwise, the reflection of the Blue pixel does not change the output grid (the destination pixel retains whatever value it had after step 2 or its original value).
5. All other pixels (including the axis and background) remain unchanged unless overwritten by the reflection steps.
"""

def find_axis(grid):
    """
    Finds the central axis (row or column) that consists of a single color
    and spans the entire grid dimension. Prioritizes non-background colors
    and centrality.
    """
    height, width = grid.shape
    counts = Counter(grid.flatten())
    
    # Determine potential background color (most frequent overall)
    potential_background = counts.most_common(1)[0][0] if counts else 0

    best_axis = None

    # Check for horizontal axis (row)
    for r in range(height):
        row = grid[r, :]
        unique_colors = np.unique(row)
        if len(unique_colors) == 1:
            axis_color = unique_colors[0]
            # Prefer non-background, full-width lines
            if counts.get(axis_color, 0) == width and axis_color != potential_background:
                centrality = abs(r - (height - 1) / 2)
                if best_axis is None or centrality < best_axis[3]:
                   best_axis = ('H', r, axis_color, centrality)
            # Consider background color axis if no other found yet or equally central
            elif counts.get(axis_color, 0) == width and axis_color == potential_background:
                 centrality = abs(r - (height - 1) / 2)
                 if best_axis is None or (best_axis[2] == potential_background and centrality < best_axis[3]):
                     best_axis = ('H', r, axis_color, centrality)


    # Check for vertical axis (column)
    for c in range(width):
        col = grid[:, c]
        unique_colors = np.unique(col)
        if len(unique_colors) == 1:
            axis_color = unique_colors[0]
            # Prefer non-background, full-height lines
            if counts.get(axis_color, 0) == height and axis_color != potential_background:
                centrality = abs(c - (width - 1) / 2)
                # Vertical axis takes precedence over horizontal if centrality is equal and non-background
                if best_axis is None or centrality < best_axis[3] or \
                   (centrality == best_axis[3] and best_axis[2] == potential_background):
                    best_axis = ('V', c, axis_color, centrality)
            # Consider background color axis if needed
            elif counts.get(axis_color, 0) == height and axis_color == potential_background:
                 centrality = abs(c - (width - 1) / 2)
                 if best_axis is None or (best_axis[2] == potential_background and centrality < best_axis[3]):
                     best_axis = ('V', c, axis_color, centrality)

    if best_axis:
        return best_axis[0], best_axis[1], best_axis[2] # orientation, index, color

    # Fallback: If no clear non-background or central axis, try first full line found
    for r in range(height):
        row = grid[r, :]
        unique_colors = np.unique(row)
        if len(unique_colors) == 1 and counts.get(unique_colors[0], 0) == width:
            return 'H', r, unique_colors[0]
    for c in range(width):
        col = grid[:, c]
        unique_colors = np.unique(col)
        if len(unique_colors) == 1 and counts.get(unique_colors[0], 0) == height:
            return 'V', c, unique_colors[0]

    raise ValueError("Could not find a suitable axis")


def find_background_color(grid, axis_info):
    """Finds the most frequent color excluding the axis color."""
    _, _, axis_color = axis_info
    counts = Counter(grid.flatten())

    # Remove axis color count
    if axis_color in counts:
        del counts[axis_color]

    if not counts:
        # If only axis color exists, return a default (e.g., 0)
        return 0

    # Most frequent remaining color is background
    background_color, _ = counts.most_common(1)[0]
    return background_color

def reflect_point(r, c, axis_info, grid_shape):
    """Calculates reflected coordinates across the axis."""
    axis_orientation, axis_index, _ = axis_info
    height, width = grid_shape

    r_refl, c_refl = r, c

    if axis_orientation == 'V':
        # Reflect horizontally across a vertical axis
        c_refl = axis_index + (axis_index - c)
    elif axis_orientation == 'H':
        # Reflect vertically across a horizontal axis
        r_refl = axis_index + (axis_index - r)

    # Ensure reflected points are within bounds
    # This shouldn't strictly be necessary if source points are correctly chosen,
    # but good for safety.
    if not (0 <= r_refl < height and 0 <= c_refl < width):
        return None # Indicate reflection is out of bounds

    return r_refl, c_refl

def is_isolated(grid, r, c, color):
    """Checks if a pixel at (r, c) has no orthogonal neighbors of the same color."""
    height, width = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width and grid[nr, nc] == color:
            return False
    return True

def transform(input_grid):
    """
    Transforms the input grid based on reflection rules derived from examples.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # 1. Identify Axis and Background
    try:
        axis_info = find_axis(input_grid_np)
    except ValueError as e:
        # If no axis found, return the original grid
        # print(f"Error finding axis: {e}. Returning original grid.")
        return input_grid # Return original list format

    axis_orientation, axis_index, axis_color = axis_info
    background_color = find_background_color(input_grid_np, axis_info)

    # 2. Apply transformation rules based on axis type and colors

    # Rule Set 1: Vertical Blue(1) Axis, Red(2) Background
    if axis_orientation == 'V' and axis_color == 1 and background_color == 2:
        azure_pixels_left = {} # Store as dict {row: [cols]}
        
        # Find Azure (8) pixels left of the axis
        for r in range(height):
            for c in range(axis_index):
                if input_grid_np[r, c] == 8:
                    if r not in azure_pixels_left:
                        azure_pixels_left[r] = []
                    azure_pixels_left[r].append(c)

        # Reflect Azure pixels and fill
        for r in azure_pixels_left:
            cols_orig = sorted(azure_pixels_left[r])
            if not cols_orig: continue

            min_c_orig = cols_orig[0]
            max_c_orig = cols_orig[-1]

            # Calculate reflection bounds for this row
            refl_coords = [reflect_point(r, c, axis_info, (height, width)) for c in cols_orig]
            refl_coords = [coord for coord in refl_coords if coord is not None] # Filter out out-of-bounds reflections
            
            if not refl_coords: continue

            reflected_cols = sorted([c_refl for _, c_refl in refl_coords])
            min_c_refl = reflected_cols[0]
            max_c_refl = reflected_cols[-1] # Not strictly needed but good for clarity

            # Perform reflection by setting pixel colors
            for r_refl, c_refl in refl_coords:
                 output_grid[r_refl, c_refl] = 8

            # Fill left side of axis (between object and axis)
            fill_start_c_left = max_c_orig + 1
            fill_end_c_left = axis_index
            if fill_start_c_left < fill_end_c_left:
                output_grid[r, fill_start_c_left : fill_end_c_left] = 1

            # Fill right side of axis (between axis and reflected object)
            fill_start_c_right = axis_index + 1
            fill_end_c_right = min_c_refl
            if fill_start_c_right < fill_end_c_right:
                 output_grid[r, fill_start_c_right : fill_end_c_right] = 1

    # Rule Set 2: Horizontal Red(2) Axis, Azure(8) Background
    elif axis_orientation == 'H' and axis_color == 2 and background_color == 8:
        # Reflect Green (3) from bottom to top first
        for r in range(axis_index + 1, height):
            for c in range(width):
                if input_grid_np[r, c] == 3:
                    refl_coord = reflect_point(r, c, axis_info, (height, width))
                    if refl_coord:
                        r_refl, c_refl = refl_coord
                        output_grid[r_refl, c_refl] = 3

        # Conditionally reflect Blue (1) from top to bottom
        for r in range(axis_index):
             for c in range(width):
                 if input_grid_np[r, c] == 1:
                     refl_coord = reflect_point(r, c, axis_info, (height, width))
                     if refl_coord:
                         r_refl, c_refl = refl_coord
                         # Check conditions: source is isolated AND original destination is background
                         source_is_isolated = is_isolated(input_grid_np, r, c, 1)
                         dest_is_background = (input_grid_np[r_refl, c_refl] == background_color)

                         if source_is_isolated and dest_is_background:
                             output_grid[r_refl, c_refl] = 2 # Change to Red

    # If axis/color combination doesn't match known cases, the output_grid remains a copy of the input

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 8 8 8 2 2 2 2 2 1 2 2 4 2 2 2 2 2 2 2
2 8 8 8 2 2 2 2 2 1 2 4 2 2 2 4 2 2 2 2
2 8 8 8 2 2 2 4 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
4 2 2 2 4 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 4 2 2 2 2
2 2 2 2 2 4 2 2 2 1 2 2 2 2 4 4 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 8 8 8 8 2 2 1 2 2 2 2 2 2 2 2 2 2
4 2 2 8 8 8 8 2 2 1 2 2 2 2 2 2 2 2 2 2
2 4 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 4 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
```
Expected Output:
```
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 8 8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 2 2
2 8 8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 2 2
2 8 8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
4 2 2 2 4 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 4 2 2 2 2
2 2 2 2 2 4 2 2 2 1 2 2 2 2 4 4 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 8 8 8 8 1 1 1 1 1 8 8 8 8 2 2 2 2
4 2 2 8 8 8 8 1 1 1 1 1 8 8 8 8 2 2 2 2
2 4 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 4 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
```
Transformed Output:
```
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 8 8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 2 2
2 8 8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 2 2
2 8 8 8 1 1 1 1 1 1 1 1 1 1 1 8 8 8 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
4 2 2 2 4 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 4 2 2 2 2
2 2 2 2 2 4 2 2 2 1 2 2 2 2 4 4 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 8 8 8 8 1 1 1 1 1 8 8 8 8 2 2 2 2
4 2 2 8 8 8 8 1 1 1 1 1 8 8 8 8 2 2 2 2
2 4 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 4 2 2 1 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 8
8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8
8 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 8
8 8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8 1 8
8 8 8 8 1 8 8 1 8 8 1 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8
8 1 8 8 8 8 8 1 8 8 8 1 8 8 8 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 1
8 8 8 8 1 8 8 1 8 8 1 8 8 8 8 8 8 8
1 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 1 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8
8 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 8 1 8 8 1 8 3 3 3 8 1 8 8 8 8
8 3 3 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8
1 8 8 8 8 8 8 8 1 8 8 8 1 8 8 8 8 1
8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 1 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 3 3 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 3 3 8 8 8 8 8 8 3 3 3 8 8 8 8 1 8
8 2 2 8 8 8 8 8 8 2 2 2 8 1 8 8 8 8
8 2 2 8 8 8 8 8 8 2 2 2 8 8 8 8 1 8
8 2 2 8 1 8 8 1 8 2 2 2 8 8 8 8 8 8
8 2 2 8 8 8 8 8 8 2 2 2 1 8 8 8 8 8
8 2 2 8 8 8 8 1 8 2 2 2 8 8 8 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 2 2 8 1 1 8 8 8 2 2 2 8 8 8 8 8 1
8 2 2 8 1 8 8 1 8 2 2 2 8 8 8 8 8 8
1 2 2 8 8 8 8 1 8 2 2 2 8 8 8 8 1 8
8 2 2 8 8 8 8 8 8 2 2 2 1 8 8 8 8 8
8 2 2 8 8 8 8 8 8 2 2 2 8 8 8 8 8 8
8 3 3 8 1 8 8 1 8 3 3 3 8 1 8 8 8 8
8 3 3 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8
1 8 8 8 8 8 8 8 1 8 8 8 1 8 8 8 8 1
8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 1 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 3 3 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 3 3 8 8 8 8 8 8 3 3 3 8 8 8 8 1 8
8 8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8 1 8
8 8 8 8 1 8 8 1 8 8 1 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8
8 1 8 8 8 8 8 1 8 8 8 1 8 8 8 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 2 8 8 1 1 8 2 8 8 8 2 8 8 8 8 8 1
8 8 8 8 1 8 8 1 8 8 1 8 2 8 8 8 8 8
1 8 8 8 2 8 8 1 8 8 2 8 8 8 8 8 1 8
8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 2 8
8 1 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8
8 3 3 8 1 8 8 1 8 3 3 3 8 1 8 8 2 8
8 3 3 8 8 8 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 3 3 3 8 8 8 8 8 8
8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 1 8 8 8 8 8 8 8 8 8 1 8 8 8 8
1 8 8 8 8 8 8 8 1 8 8 8 1 8 8 8 8 1
8 8 8 8 8 8 8 8 8 8 8 8 1 8 8 1 8 8
```
Match: False
Pixels Off: 53
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.04232804232805
