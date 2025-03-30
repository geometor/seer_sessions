import numpy as np
from typing import List, Tuple

"""
Identifies the largest contiguous rectangular block for each non-white color 
present in the input grid and changes the color of these largest blocks to yellow (4).

1. Copy the input grid to create the initial output grid.
2. Find all unique colors present in the input grid, excluding white (0).
3. For each unique non-white color:
    a. Find all maximal contiguous rectangular blocks composed entirely of that color.
    b. Calculate the area (height * width) of each block.
    c. Identify the block with the maximum area for this color. If there are ties,
       any one of the largest blocks can be chosen.
4. Store the location (top-left row, col) and dimensions (height, width) of the 
   largest block found for each color.
5. Iterate through the stored largest blocks.
6. For each largest block, change the color of all pixels within its bounds in the 
   output grid to yellow (4).
7. Return the modified output grid.
"""


def find_maximal_rectangles(grid: np.ndarray, color: int) -> List[Tuple[int, int, int, int]]:
    """
    Finds all maximal contiguous rectangles of a given color in the grid.

    Args:
        grid: The input grid as a NumPy array.
        color: The target color to search for.

    Returns:
        A list of tuples, where each tuple represents a maximal rectangle
        in the format (row, col, height, width).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                # Found a potential top-left corner of a new maximal rectangle
                
                # Find the maximum possible width for the first row
                current_w = 0
                while c + current_w < width and grid[r, c + current_w] == color and not visited[r, c + current_w]:
                    current_w += 1
                
                if current_w == 0: # Should not happen if grid[r,c]==color and not visited, but as safeguard
                    visited[r, c] = True # Mark as visited to prevent re-check
                    continue

                # Find the maximum possible height for this width
                current_h = 1
                while r + current_h < height:
                    # Check if the entire next row segment matches the color and width
                    all_match = True
                    for i in range(current_w):
                        if grid[r + current_h, c + i] != color or visited[r + current_h, c + i]:
                            all_match = False
                            break
                    
                    if all_match:
                        current_h += 1
                    else:
                        break # Cannot extend height further with this width

                # Store the rectangle found
                rectangles.append((r, c, current_h, current_w))
                
                # Mark the area of this rectangle as visited
                visited[r : r + current_h, c : c + current_w] = True
                
    return rectangles

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by finding the largest rectangle of each 
    non-white color and changing its color to yellow (4).
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape
    
    # Find unique non-white colors
    unique_colors = np.unique(input_grid_np)
    non_white_colors = [c for c in unique_colors if c != 0]
    
    largest_blocks_to_recolor = []

    # Find the largest rectangle for each color
    for color in non_white_colors:
        # Find all maximal rectangles of this color
        rectangles = find_maximal_rectangles(input_grid_np, color)
        
        if not rectangles:
            continue # No rectangles of this color found

        # Calculate areas and find the max area
        max_area = 0
        largest_rect = None
        for r, c, h, w in rectangles:
            area = h * w
            if area > max_area:
                max_area = area
                largest_rect = (r, c, h, w)
        
        if largest_rect:
             largest_blocks_to_recolor.append(largest_rect)

    # Recolor the largest identified blocks to yellow (4)
    for r, c, h, w in largest_blocks_to_recolor:
        output_grid[r : r + h, c : c + w] = 4
        
    # Return the grid in list of lists format
    return output_grid.tolist()
