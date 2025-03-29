import numpy as np

"""
Processes objects on a background grid by:
1. Conditionally filling a 9x9 square area if exactly one single-pixel non-background object exists in the input. The fill color and center location are determined by this single pixel.
2. Removing the outermost layer of pixels (noise) from all non-background objects present in the original input. A pixel is considered noise if it's not the background color and has at least one neighbor (8-connectivity) that is the background color.

The background color is orange (7).
The conditional fill happens first on a copy of the input grid.
The noise removal happens second, modifying the potentially filled grid by setting identified noise pixels (based on the *original* input) back to the background color.
"""

def find_single_pixels(grid, background_color):
    """
    Finds all pixels of non-background color that are completely surrounded
    by the background color (8-connectivity).
    Returns a list of tuples: (row, col, color).
    """
    single_pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color:
                is_single = True
                # Check 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            if grid[nr, nc] != background_color:
                                is_single = False
                                break
                        # Implicitly, out-of-bounds is like background for isolation check
                    if not is_single:
                        break
                
                if is_single:
                    single_pixels.append((r, c, color))
    return single_pixels

def find_noise_pixels(grid, background_color):
    """
    Finds all non-background pixels that have at least one background neighbor
    (8-connectivity).
    Returns a set of coordinate tuples: {(row, col), ...}.
    """
    noise_locations = set()
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color:
                is_noise = False
                # Check 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            if grid[nr, nc] == background_color:
                                is_noise = True
                                break
                        else: # Out of bounds counts as background neighbor
                           is_noise = True
                           break 
                    if is_noise:
                        break
                
                if is_noise:
                    noise_locations.add((r, c))
    return noise_locations

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    background_color = 7

    # 1. Find single-pixel objects in the *input* grid
    single_pixels = find_single_pixels(input_np, background_color)

    # 2. Perform Conditional Fill if exactly one single pixel found
    if len(single_pixels) == 1:
        center_r, center_c, fill_color = single_pixels[0]
        
        # Calculate the 9x9 area bounds, centered on (center_r, center_c)
        # Top-left corner calculation
        top = max(0, center_r - 4)
        left = max(0, center_c - 4)
        
        # Bottom-right corner calculation (exclusive for slicing)
        # Ensure the size is up to 9x9 within grid boundaries
        bottom = min(height, top + 9)
        right = min(width, left + 9)

        # Adjust top/left if clipping affected the size potential from bottom/right
        top = max(0, bottom - 9)
        left = max(0, right - 9)

        # Fill the calculated area in the output grid
        output_grid[top:bottom, left:right] = fill_color

    # 3. Identify noise pixels based on the *original input* grid
    noise_locations = find_noise_pixels(input_np, background_color)

    # 4. Remove noise pixels from the *output* grid
    for r, c in noise_locations:
        # Ensure coordinates are valid just in case (should be by find_noise_pixels logic)
        if 0 <= r < height and 0 <= c < width:
             output_grid[r, c] = background_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()