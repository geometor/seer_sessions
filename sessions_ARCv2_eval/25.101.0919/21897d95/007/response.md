```python
import numpy as np
from scipy.ndimage import label
from collections import Counter

"""
Transforms the input grid according to the following rules:

1.  **Identify Background/Foreground:** 
    - Background pixels belong to connected components (8-way) that both touch the bottom edge of the input grid and consist of colors found on that bottom edge.
    - Foreground pixels are all pixels that are not background pixels.

2.  **Calculate Output Background Color:**
    - Find the set of unique colors present in the background mask.
    - If the set is empty, the output background color is 0.
    - Otherwise, the output background color is max(0, min(background colors) - 1). 
      (Note: Analysis showed this rule doesn't match all training examples perfectly).

3.  **Identify Structural Foreground Regions and Determine Output Color:**
    - Structural foreground regions are connected components (8-way) based on the foreground mask (ignoring color for connectivity).
    - For each structural region:
        - Find its dominant color (most frequent color within the region).
        - Find the set of noise colors (other unique colors within the region).
        - If there's exactly one unique noise color, the entire region maps to that noise color.
        - Otherwise (zero or multiple noise colors), the entire region maps to its dominant color.

4.  **Rotation and Final Coloring:**
    - Rotate the input grid 90 degrees clockwise.
    - Create the output grid.
    - For each pixel in the output grid, find its corresponding pixel in the original input grid.
    - If the original pixel was background, assign the calculated output background color.
    - If the original pixel was foreground, assign the output color determined for its structural region based on the noise rule (Step 3).
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

    # Label connected components within this potential background mask (8-way)
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

def _calculate_output_bg_color(grid: np.ndarray, bg_mask: np.ndarray) -> int:
    """
    Calculates the output background color based on the min input background color - 1 rule.
    """
    if not np.any(bg_mask):
        return 0 # Default if no background pixels

    background_colors = grid[bg_mask]
    if background_colors.size == 0:
        return 0 # Should be covered by np.any, but safe check

    min_bg_color = np.min(background_colors)
    output_bg_color = max(0, min_bg_color - 1)
    return output_bg_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rotate, map-by-noise, and fill-background rule.
    """
    input_array = np.array(input_grid, dtype=int)
    h, w = input_array.shape
    fallback_color = 0 # Default color if mapping fails

    # Handle empty input grid
    if h == 0 or w == 0:
        return [[] for _ in range(w)] if w > 0 else []

    # --- Step 1: Identify Background/Foreground Masks ---
    bg_mask = _find_background_mask(input_array)
    fg_mask = ~bg_mask

    # --- Step 2: Calculate Output Background Color ---
    output_bg_color = _calculate_output_bg_color(input_array, bg_mask)

    # --- Step 3: Identify Structural FG Regions, Analyze Noise, Determine Output Color ---
    # Create a grid to store the calculated output color for each input foreground pixel
    region_output_color_map_grid = np.full((h, w), fallback_color, dtype=int) # Initialize with fallback
    structure = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=bool) # 8-way connectivity

    # Label connected components based on the foreground mask structure
    labeled_fg_structure, num_fg_regions = label(fg_mask, structure=structure)

    for region_id in range(1, num_fg_regions + 1):
        # Get mask for the current structural region
        component_mask = (labeled_fg_structure == region_id)
        component_pixels = input_array[component_mask]

        if component_pixels.size == 0:
            continue

        # Find the dominant color within this structural component
        colors, counts = np.unique(component_pixels, return_counts=True)
        # Handle tie-breaking for dominant color if needed (e.g., lowest color index)
        dominant_color = colors[np.argmax(counts)]
        if len(colors) > 1 and np.sum(counts == counts.max()) > 1:
             # Tie detected, choose lowest color index among tied max counts
             tied_colors = colors[counts == counts.max()]
             dominant_color = min(tied_colors)


        # Find noise colors within this structural component
        noise_colors = set(colors) - {dominant_color}

        # Determine the output color based on the noise rule
        output_fg_color = fallback_color # Default
        if len(noise_colors) == 1:
            output_fg_color = list(noise_colors)[0]
        else:
            # Zero or multiple noise colors -> use dominant color
            output_fg_color = dominant_color

        # Assign this output color to all pixels belonging to this structural region in the map
        region_output_color_map_grid[component_mask] = output_fg_color

    # --- Step 4: Rotate and Construct Output Grid ---
    rotated_h, rotated_w = w, h
    output_array = np.zeros((rotated_h, rotated_w), dtype=int) # Initialize output

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
                    output_array[r_out, c_out] = output_bg_color
                else:
                    # Assign the pre-calculated output color for the foreground region
                    output_array[r_out, c_out] = region_output_color_map_grid[r_in, c_in]
            else:
                 # Fallback for out-of-bounds calculation (should not happen)
                 output_array[r_out, c_out] = fallback_color

    # Convert the final numpy array back to a list of lists
    return output_array.tolist()
```