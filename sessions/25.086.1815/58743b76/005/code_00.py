"""
The transformation rule identifies a 2x2 key block of colors, typically located near a corner, distinct from the background (usually white 0) and a potential border (usually azure 8). It also identifies a single 'target' color, which is the most frequent color present elsewhere in the grid (excluding background, border, and the pixels *at the key's location*). The rule then determines the bounding box encompassing *all* pixels of the target color (including any within the key block). Based on the center of this bounding box, the grid is conceptually divided into four quadrants. Each pixel having the target color *that is not part of the key block* is then replaced by one of the four key colors, depending on which quadrant the pixel falls into: top-left quadrant maps to the top-left key color, top-right quadrant to top-right key color, bottom-left quadrant to bottom-left key color, and bottom-right quadrant to bottom-right key color. Other pixels (background, border, key pixels, and any non-target color pixels) remain unchanged.
"""

import numpy as np
from collections import Counter

def find_key(grid, border_color, background_color):
    """
    Finds the first 2x2 key block scanning top-to-bottom, left-to-right.
    A key block has no border or background colored pixels.

    Args:
        grid (np.array): The input grid.
        border_color (int): The color designated as the border.
        background_color (int): The color designated as the background.

    Returns:
        tuple: (key_r, key_c, k00, k01, k10, k11) top-left coords and colors,
               or None if no key is found.
    """
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Extract 2x2 block colors
            k00 = grid[r, c]
            k01 = grid[r, c+1]
            k10 = grid[r+1, c]
            k11 = grid[r+1, c+1]
            colors = [k00, k01, k10, k11]

            # Check if any color in the block is background or border
            is_valid_key = True
            for color in colors:
                if color == border_color or color == background_color:
                    is_valid_key = False
                    break
            
            # If all colors are valid, this is the key
            if is_valid_key:
                return r, c, k00, k01, k10, k11
    # No key found
    return None

def find_target_color(grid, border_color, background_color, key_positions):
    """
    Finds the most frequent color excluding border, background, and key pixels.

    Args:
        grid (np.array): The input grid.
        border_color (int): The border color.
        background_color (int): The background color.
        key_positions (set): A set of (r, c) tuples representing key locations.

    Returns:
        int or None: The target color, or None if no candidates found.
    """
    height, width = grid.shape
    candidate_pixels = []
    
    # Iterate through all pixels to find candidates for target color
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Pixel is a candidate if not border, background, and not in key position
            if color != border_color and \
               color != background_color and \
               (r, c) not in key_positions:
                candidate_pixels.append(color)

    # If no candidates found, return None
    if not candidate_pixels:
        return None

    # Count frequency and return the most common color
    count = Counter(candidate_pixels)
    target_color = count.most_common(1)[0][0]
    return target_color

def find_bounding_box(grid, target_color):
    """
    Finds the minimum bounding box containing ALL pixels of target_color.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color to find the bounding box for.

    Returns:
        tuple or None: (min_r, max_r, min_c, max_c) or None if target_color not found.
    """
    # Find indices of all pixels matching the target color
    rows, cols = np.where(grid == target_color)

    # If no such pixels exist, return None
    if rows.size == 0:
        return None

    # Determine min/max row and column indices
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    
    return min_r, max_r, min_c, max_c

def transform(input_grid):
    """
    Applies the quadrant-based color transformation based on a 2x2 key.
    """
    # Convert input list of lists to numpy array
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify for the output
    output_grid = grid.copy()
    height, width = grid.shape

    # Define assumed border and background colors
    border_color = 8  # azure
    background_color = 0 # white

    # Step 1: Find the 2x2 key
    key_info = find_key(grid, border_color, background_color)
    if key_info is None:
        # No key found, return the original grid
        return output_grid.tolist() 
        
    key_r, key_c, k00, k01, k10, k11 = key_info
    # Store the set of coordinates occupied by the key
    key_positions = {
        (key_r, key_c), (key_r, key_c + 1),
        (key_r + 1, key_c), (key_r + 1, key_c + 1)
    }

    # Step 2: Find the target color (most frequent excluding bg, border, key pixels)
    target_color = find_target_color(grid, border_color, background_color, key_positions)
    if target_color is None:
        # No target color found, return the original grid
        return output_grid.tolist()

    # Step 3: Find the bounding box of *all* target color pixels
    bbox = find_bounding_box(grid, target_color)
    if bbox is None:
         # Should not happen if target_color was found, but safety check
        return output_grid.tolist()
    min_r, max_r, min_c, max_c = bbox

    # Step 4: Calculate the center of the bounding box (can be float)
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0

    # Step 5: Iterate through the grid and apply transformation
    for r in range(height):
        for c in range(width):
            # Check if the pixel has the target color AND is NOT part of the key
            if grid[r, c] == target_color and (r, c) not in key_positions:
                
                # Determine the quadrant relative to the center
                # Pixels exactly on center lines go to bottom/right halves
                if r < center_r and c < center_c:
                    # Top-left quadrant -> top-left key color
                    output_grid[r, c] = k00  
                elif r < center_r and c >= center_c:
                    # Top-right quadrant -> top-right key color
                    output_grid[r, c] = k01  
                elif r >= center_r and c < center_c:
                    # Bottom-left quadrant -> bottom-left key color
                    output_grid[r, c] = k10  
                elif r >= center_r and c >= center_c:
                    # Bottom-right quadrant -> bottom-right key color
                    output_grid[r, c] = k11  
            # Else (pixel is bg, border, key, or non-target): keep original color (already in output_grid copy)

    # Convert the final numpy array back to a list of lists for return
    return output_grid.tolist()