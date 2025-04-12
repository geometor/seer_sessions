```python
"""
Transforms the input grid based on the uniformity of its corner pixels and a comparison between the corner color and the overall dominant color.

1.  Examine the four corner pixels (top-left, top-right, bottom-left, bottom-right).
2.  If the four corner pixels do NOT all have the same color:
    a.  Find the 'overall_dominant_color' (most frequent color across the entire grid, ties broken by smallest color index).
    b.  Fill the entire output grid with the 'overall_dominant_color'.
3.  If the four corner pixels DO all have the same color:
    a.  Identify this common corner color as the 'background_color'.
    b.  Find the 'overall_dominant_color'.
    c.  If the 'background_color' is the same as the 'overall_dominant_color':
        i. Fill the entire output grid with the 'background_color'.
    d.  Else (the 'background_color' is different from the 'overall_dominant_color'):
        i. Identify 'interior_pixels' (not on the perimeter).
        ii. Find the 'dominant_interior_non_background_color' (most frequent color among interior pixels whose color is not 'background_color', ties broken by smallest index).
        iii. Create the output grid.
        iv. Fill all perimeter pixels of the output grid with 'background_color'.
        v. Fill interior pixels: if the corresponding input pixel was 'background_color', use 'background_color'; otherwise, use 'dominant_interior_non_background_color'. (Handles grids < 3x3 correctly as they have no interior to modify).
4.  Return the resulting output grid.
"""

import numpy as np
from collections import Counter

def find_dominant_color(pixels: np.ndarray) -> int | None:
    """
    Finds the most frequent color in a flattened array of pixels.
    Handles ties by returning the smallest color index.
    Returns None if the input array is empty.
    """
    if pixels.size == 0:
        return None # No pixels, no dominant color

    counts = Counter(pixels.flatten())
    if not counts: # Check if counter is empty
        return None

    # Find the maximum count
    max_count = 0
    # Use counts.most_common(1) for potentially slightly better performance?
    # Or iterate as before:
    for count in counts.values():
         if count > max_count:
             max_count = count

    # Get all colors with the maximum count
    dominant_colors = [color for color, count in counts.items() if count == max_count]

    # Return the smallest color index in case of a tie
    return min(dominant_colors)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation based on corner uniformity and dominant colors.
    """
    # Convert input list of lists to a NumPy array for easier indexing and operations
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Handle edge case of 1x1 grid (already uniform)
    if height == 1 and width == 1:
        return input_grid

    # Check corner pixels
    top_left = grid_np[0, 0]
    top_right = grid_np[0, width - 1]
    bottom_left = grid_np[height - 1, 0]
    bottom_right = grid_np[height - 1, width - 1]

    corners_match = (top_left == top_right == bottom_left == bottom_right)

    if not corners_match:
        # Case 1: Corners do not match
        # Find the overall dominant color
        overall_dominant_color = find_dominant_color(grid_np)
        # Fill the entire output grid with the overall dominant color
        # Handle case where grid is empty (shouldn't happen based on ARC constraints)
        fill_color = overall_dominant_color if overall_dominant_color is not None else 0 # Default fill
        output_grid_np = np.full_like(grid_np, fill_color)

    else:
        # Case 2: Corners match
        background_color = top_left

        # Find overall dominant color
        overall_dominant_color = find_dominant_color(grid_np)
        
        # Check if background color is the overall dominant color
        if background_color == overall_dominant_color:
            # Subcase 2a: Background IS dominant
            # Fill output grid entirely with background_color
            output_grid_np = np.full_like(grid_np, background_color)
        else:
            # Subcase 2b: Background is NOT dominant
            # Initialize output grid with background color (covers perimeter and background pixels in interior)
            output_grid_np = np.full_like(grid_np, background_color)

            # Check if grid has an interior region
            if height > 2 and width > 2:
                # Extract interior region from input
                interior_region = grid_np[1:-1, 1:-1]
                
                # Find pixels in the interior that are not the background color
                interior_non_background_pixels = interior_region[interior_region != background_color]
                
                # Find the dominant color among these non-background interior pixels
                dominant_interior_fill_color = find_dominant_color(interior_non_background_pixels)

                # If there were non-background pixels in the interior, fill them in the output
                if dominant_interior_fill_color is not None:
                    # Iterate through interior indices and update output grid
                    for r in range(1, height - 1):
                        for c in range(1, width - 1):
                            if grid_np[r, c] != background_color:
                                output_grid_np[r, c] = dominant_interior_fill_color
            # Else (no interior): The grid is already correctly filled with background_color


    # Convert the final NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```