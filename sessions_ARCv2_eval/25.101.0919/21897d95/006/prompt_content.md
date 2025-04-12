
Previous Code:
```python
import numpy as np
from scipy.ndimage import label
from collections import Counter

"""
Transforms the input grid based on the following rules:

1.  **Identify Background/Foreground:** 
    - Background pixels belong to connected components that both touch the bottom edge of the input grid and consist of colors found on that bottom edge.
    - Foreground pixels are all pixels that are not background pixels.

2.  **Identify Foreground Regions and Determine Output Color:**
    - Foreground regions are maximal connected components of foreground pixels initially having the same color (the 'dominant color').
    - For each foreground region, identify any 'noise' pixels within it (pixels of a different color).
    - If a region has exactly one unique noise color, the entire region (including noise pixels) maps to that single noise color in the output.
    - Otherwise (zero or multiple noise colors), the entire region maps to its original dominant color in the output.

3.  **Rotation and Initial Coloring:**
    - Rotate the input grid 90 degrees clockwise.
    - Create an intermediate grid.
    - For each pixel in the intermediate grid, find its corresponding pixel in the original input grid.
    - If the original pixel was background, mark the intermediate pixel with a placeholder value (-1).
    - If the original pixel was foreground, find the output color determined in Step 2 for its region and place that color in the intermediate grid.

4.  **Background Propagation:**
    - Fill the placeholder values in the intermediate grid.
    - For each row, iterate from left to right. Replace any placeholder pixel with the value of the nearest non-placeholder pixel found to its left in the same row.
    - If a row starts with placeholders, they take the value of the first non-placeholder pixel encountered in that row. If a row consists entirely of placeholders, fill it with a default color (e.g., 0).
"""

def _find_background_mask(grid: np.ndarray) -> np.ndarray:
    """
    Identifies pixels belonging to connected components that touch the bottom edge
    and consist of colors present on the bottom edge. Uses 8-way connectivity.
    """
    h, w = grid.shape
    if h == 0:
        return np.zeros((h, w), dtype=bool) # Handle empty grid

    # Get the set of unique colors present on the bottom row
    bottom_row_colors = set(grid[h - 1, :])
    if not bottom_row_colors:
        return np.zeros((h, w), dtype=bool) # Handle empty bottom row

    # Create a mask where pixels have one of the bottom row colors
    potential_bg_mask = np.isin(grid, list(bottom_row_colors))

    # Label connected components within this potential background mask
    # Use a structure that defines 8-way connectivity
    structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool)
    labeled_potential_bg, num_labels = label(potential_bg_mask, structure=structure)

    # Identify the labels of components that actually touch the bottom row
    labels_touching_bottom = set(labeled_potential_bg[h - 1, :])
    if 0 in labels_touching_bottom: # 0 is the label for non-mask areas
        labels_touching_bottom.remove(0)

    # If no components touch the bottom row, there's no background by this definition
    if not labels_touching_bottom:
        return np.zeros((h, w), dtype=bool)

    # The final background mask includes only pixels belonging to those components touching the bottom
    background_mask = np.isin(labeled_potential_bg, list(labels_touching_bottom))
    return background_mask

def _propagate_background(grid: np.ndarray, placeholder: int = -1, default_fill: int = 0) -> np.ndarray:
    """
    Fills placeholder values by propagating the color from the nearest
    non-placeholder pixel to the left within the same row.
    Fills rows that are all placeholders with default_fill.
    """
    output_grid = grid.copy()
    h, w = output_grid.shape

    for r in range(h):
        last_valid_color = -1 # Indicates no valid color seen yet in this row
        first_valid_found = False

        # Find the first non-placeholder color to handle rows starting with placeholders
        for c in range(w):
            if output_grid[r, c] != placeholder:
                last_valid_color = output_grid[r, c]
                first_valid_found = True
                break

        # If the entire row is placeholder, fill with default
        if not first_valid_found:
            output_grid[r, :] = default_fill
            continue # Move to next row

        # Propagate from left
        current_fill_color = last_valid_color # Start filling with the first valid color found
        for c in range(w):
            if output_grid[r, c] == placeholder:
                output_grid[r, c] = current_fill_color
            else:
                # Update the color to propagate when a non-placeholder is encountered
                current_fill_color = output_grid[r, c]

    return output_grid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rotate, map-by-noise, and propagate rule.
    """
    input_array = np.array(input_grid, dtype=int)
    h, w = input_array.shape
    placeholder = -1
    fallback_color = 0 # Default color if mapping fails or for all-placeholder rows

    # Handle empty input grid
    if h == 0 or w == 0:
        return [[] for _ in range(w)] if w > 0 else []

    # --- Step 1: Identify Background/Foreground Masks ---
    bg_mask = _find_background_mask(input_array)
    fg_mask = ~bg_mask

    # --- Step 2 & 3: Identify FG Regions, Analyze Noise, Determine Output Color ---
    # Create a grid to store the calculated output color for each input foreground pixel
    # Initialize with a value indicating "not calculated" or "background"
    region_output_color_map_grid = np.full((h, w), placeholder, dtype=int)
    structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool) # 8-way connectivity

    # Label connected components *purely based on the foreground mask structure* first
    # This helps group noise pixels with their surrounding region initially.
    labeled_fg_structure, num_fg_regions = label(fg_mask, structure=structure)

    for region_id in range(1, num_fg_regions + 1):
        # Get mask for the current structural region
        component_mask = (labeled_fg_structure == region_id)
        component_pixels = input_array[component_mask]

        if component_pixels.size == 0:
            continue

        # Find the dominant color within this structural component
        colors, counts = np.unique(component_pixels, return_counts=True)
        dominant_color = colors[np.argmax(counts)]

        # Find noise colors within this structural component
        noise_colors = set(colors) - {dominant_color}

        # Determine the output color based on the noise rule
        output_color = fallback_color # Default if something goes wrong
        if len(noise_colors) == 1:
            output_color = list(noise_colors)[0]
        else:
            # Zero or multiple noise colors -> use dominant color
            output_color = dominant_color

        # Assign this output color to all pixels belonging to this structural region
        region_output_color_map_grid[component_mask] = output_color


    # --- Step 4: Rotate and Create Intermediate Grid ---
    rotated_h, rotated_w = w, h
    intermediate_grid = np.full((rotated_h, rotated_w), placeholder, dtype=int)

    # Loop through each pixel of the *output* grid
    for r_out in range(rotated_h):
        for c_out in range(rotated_w):
            # Calculate corresponding coordinates in the *original* input grid
            # Clockwise rotation: input (r_in, c_in) -> output (c_in, H_in - 1 - r_in)
            # Inverse: output (r_out, c_out) -> input (H_in - 1 - c_out, r_out)
            r_in = h - 1 - c_out
            c_in = r_out

            # Ensure calculated input coordinates are valid
            if 0 <= r_in < h and 0 <= c_in < w:
                # Check if the original pixel was background
                if bg_mask[r_in, c_in]:
                    intermediate_grid[r_out, c_out] = placeholder
                else:
                    # Assign the pre-calculated output color for the foreground region
                    mapped_color = region_output_color_map_grid[r_in, c_in]
                    # Ensure it's not still the placeholder value if logic was perfect
                    intermediate_grid[r_out, c_out] = mapped_color if mapped_color != placeholder else fallback_color
            else:
                 # Fallback for out-of-bounds calculation (should not happen)
                 intermediate_grid[r_out, c_out] = fallback_color

    # --- Step 5: Propagate Background Color ---
    final_output_array = _propagate_background(intermediate_grid, placeholder, fallback_color)

    # Convert the final numpy array back to a list of lists
    return final_output_array.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
6 6 6 6 6 7 7 7 4 4 4 4
6 6 6 6 6 7 7 7 4 4 4 4
6 6 6 1 6 7 7 7 4 4 4 4
6 6 6 3 1 7 7 7 4 9 9 9
6 6 6 1 6 7 7 7 4 4 4 9
6 6 6 6 6 7 7 7 4 4 4 9
6 6 6 6 6 7 1 7 4 4 4 4
6 6 6 6 6 7 1 1 4 4 4 4
6 6 6 6 6 7 1 7 4 4 4 4
6 6 6 6 6 7 7 7 4 4 4 4
7 7 1 7 7 7 7 7 7 7 7 7
7 1 0 1 7 7 7 7 7 1 1 1
7 7 7 7 7 7 7 7 7 7 1 7
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
7 7 7 7 7 7 7 7 7 7 3 3 3 7 7 7
7 7 7 7 7 7 7 7 7 7 3 3 3 7 7 7
7 7 7 7 7 7 7 7 7 7 3 3 3 7 7 7
7 7 7 7 7 7 7 7 7 7 3 3 3 7 7 7
3 3 3 3 3 3 3 3 3 3 3 3 3 7 7 7
3 3 3 3 3 3 3 3 3 3 3 3 3 7 7 7
3 3 3 3 3 3 3 3 3 3 3 3 3 7 7 7
0 0 0 0 0 0 0 0 0 0 3 3 3 7 7 7
0 0 0 0 0 0 0 0 0 0 3 3 3 7 7 7
0 0 0 0 0 0 0 0 0 0 3 3 3 7 7 7
0 0 0 0 0 0 0 0 0 0 3 3 3 7 7 7
0 0 0 0 0 0 0 0 0 0 3 3 3 7 7 7
```
Transformed Output:
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Match: False
Pixels Off: 116
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 120.83333333333334

## Example 2:
Input:
```
7 7 7 7 7 7 1 7 3 3
7 7 7 7 7 7 1 1 3 3
7 7 7 7 7 7 1 7 3 3
8 8 8 3 1 7 7 7 3 1
8 8 8 1 1 7 7 7 1 6
8 1 8 3 1 7 7 7 3 1
8 1 1 3 3 1 9 1 3 3
8 1 8 3 3 7 1 7 3 3
8 8 8 3 3 5 5 5 3 3
8 8 8 3 3 5 5 5 3 3
```
Expected Output:
```
6 6 6 6 6 6 6 6 7 7
6 6 6 6 6 6 6 6 7 7
6 6 6 6 6 6 6 6 7 7
3 3 3 8 8 6 6 6 7 7
3 3 3 8 8 6 6 6 7 7
3 3 3 8 8 6 6 6 7 7
3 3 3 8 8 6 6 6 7 7
3 3 3 8 8 6 6 6 7 7
3 3 3 8 8 9 9 9 7 7
3 3 3 8 8 9 9 9 7 7
```
Transformed Output:
```
7 7 7 7 7 7 7 7 7 7
1 1 1 1 1 1 1 7 7 7
1 1 1 1 1 1 1 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7
```
Match: False
Pixels Off: 80
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 320.0

## Example 3:
Input:
```
6 6 6 3 1 3 3 3 3
6 6 6 1 1 3 3 3 3
6 6 6 3 1 3 3 3 3
6 6 6 4 4 4 4 1 4
6 6 6 4 4 4 1 1 1
6 6 6 4 4 4 4 4 4
6 6 6 6 1 6 4 4 4
6 6 6 6 1 1 4 4 4
6 6 6 6 1 6 4 4 4
5 5 5 4 4 4 4 4 4
9 9 9 8 8 8 8 8 8
9 5 5 8 8 8 1 7 1
9 5 5 8 8 8 8 1 8
5 5 5 4 4 4 4 4 4
```
Expected Output:
```
5 5 5 5 5 3 3 3 3 3 3 3 3 3
5 5 5 5 5 3 3 3 3 3 3 3 3 3
5 5 5 5 5 3 3 3 3 3 3 3 3 3
7 8 8 8 6 3 3 3 6 6 6 4 4 4
7 8 8 8 6 3 3 3 6 6 6 4 4 4
7 8 8 8 6 3 3 3 6 6 6 4 4 4
7 8 8 8 6 6 6 6 6 6 6 4 4 4
7 8 8 8 6 6 6 6 6 6 6 4 4 4
7 8 8 8 6 6 6 6 6 6 6 4 4 4
```
Transformed Output:
```
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Match: False
Pixels Off: 93
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 147.61904761904762

## Example 4:
Input:
```
2 2 2 2 2 1 2 3 3 3
2 2 2 2 2 1 1 3 3 3
2 2 2 2 2 1 2 3 3 3
6 6 6 6 1 6 6 3 1 3
6 6 6 1 1 1 6 1 1 3
1 1 1 6 6 6 6 3 1 3
6 1 6 6 6 6 6 3 3 3
4 4 4 4 4 4 4 3 3 3
4 4 4 4 4 4 4 3 3 3
4 4 4 4 4 4 4 3 3 3
```
Expected Output:
```
6 6 6 6 6 6 6 2 2 2
6 6 6 6 6 6 6 2 2 2
6 6 6 6 6 6 6 2 2 2
3 3 3 3 3 3 3 2 2 2
3 3 3 3 3 3 3 2 2 2
3 3 3 3 3 3 3 2 2 2
3 3 3 3 3 3 3 2 2 2
6 6 6 6 6 6 6 2 2 2
6 6 6 6 6 6 6 2 2 2
6 6 6 6 6 6 6 2 2 2
```
Transformed Output:
```
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 65
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 260.0
