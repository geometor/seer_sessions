import numpy as np
import copy

"""
The transformation identifies a repeating background pattern present in the non-white (non-zero) areas of the input grid. 
It then fills in any white (zero) pixels in the input grid with the color that corresponds to that position within the repeating pattern. 
Pixels that are not white in the input remain unchanged in the output.

The process involves:
1. Determining the dimensions (height and width) of the smallest repeating unit (tile) of the background pattern by analyzing the non-white pixels.
2. Creating an output grid initially identical to the input grid.
3. Iterating through each pixel of the input grid.
4. If a pixel is white (0), calculate its position within the pattern tile using the modulo operator with the pattern dimensions.
5. Find the correct color for this pattern position by looking at a corresponding non-white pixel in the input grid that falls on the same relative position within its pattern tile.
6. Replace the white pixel in the output grid with the determined pattern color.
7. Return the modified output grid.
"""

def find_pattern_dimensions(grid):
    """
    Finds the smallest repeating pattern dimensions (height, width) in the grid,
    ignoring white (0) pixels.
    """
    height, width = grid.shape
    
    # Iterate through possible pattern heights
    for h in range(1, height + 1):
        # Iterate through possible pattern widths
        for w in range(1, width + 1):
            is_pattern = True
            # Check if this (h, w) defines a valid pattern
            for r in range(height):
                for c in range(width):
                    color = grid[r, c]
                    # Ignore white pixels for pattern definition
                    if color == 0:
                        continue

                    # Check vertical repetition
                    if r + h < height:
                        neighbor_color = grid[r + h, c]
                        if neighbor_color != 0 and color != neighbor_color:
                            is_pattern = False
                            break
                    
                    # Check horizontal repetition
                    if c + w < width:
                        neighbor_color = grid[r, c + w]
                        if neighbor_color != 0 and color != neighbor_color:
                            is_pattern = False
                            break
                if not is_pattern:
                    break
            
            # If a consistent pattern is found for this (h, w), return dimensions
            if is_pattern:
                 # Add an extra check: ensure at least one repetition was actually verified
                 # to avoid trivial 1x1 patterns if the grid is monochrome (excluding 0s)
                 # or patterns matching grid size if no repetition occurs.
                 verified_repetition = False
                 for r in range(height):
                     for c in range(width):
                         if grid[r,c] == 0: continue
                         if r + h < height and grid[r+h,c]!=0 and grid[r,c] == grid[r+h,c]:
                             verified_repetition = True
                             break
                         if c + w < width and grid[r,c+w]!=0 and grid[r,c] == grid[r,c+w]:
                             verified_repetition = True
                             break
                     if verified_repetition: break
                 
                 # Only return if a non-trivial pattern repetition was found or if it's the full grid size
                 if verified_repetition or (h == height and w == width):
                     return h, w

    # Should not happen with ARC task constraints, but return full size as fallback
    return height, width 

def transform(input_grid):
    """
    Fills white (0) pixels in the input grid based on the surrounding repeating pattern.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # 1. Determine the pattern dimensions
    pattern_h, pattern_w = find_pattern_dimensions(input_np)

    # 2. Create a reference pattern tile (optional but can optimize lookup)
    # We can skip creating the full tile and look up the source color directly when needed.

    # 3. Iterate through the grid and fill white pixels
    for r in range(height):
        for c in range(width):
            # 4. If the pixel is white
            if input_np[r, c] == 0:
                # 5. Calculate position within the pattern
                target_pr = r % pattern_h
                target_pc = c % pattern_w

                # Find the source color for this pattern position
                source_color = -1 # Use -1 to indicate not found yet
                
                # Search for a non-white pixel at a corresponding pattern location
                # Start searching from the top-left and expand outwards in pattern repetitions
                found = False
                for repeat_r in range(height // pattern_h + 1):
                    for repeat_c in range(width // pattern_w + 1):
                        source_r = target_pr + repeat_r * pattern_h
                        source_c = target_pc + repeat_c * pattern_w

                        if source_r < height and source_c < width:
                            if input_np[source_r, source_c] != 0:
                                source_color = input_np[source_r, source_c]
                                found = True
                                break
                    if found:
                        break
                
                # 6. Replace the white pixel in the output grid
                if source_color != -1:
                    output_grid[r, c] = source_color
                # If no source color was found (e.g., entire grid was white, or a pattern
                # position only ever appeared as white), leave it as 0 (or handle as error).
                # ARC guarantees should prevent this usually.


    return output_grid.tolist()