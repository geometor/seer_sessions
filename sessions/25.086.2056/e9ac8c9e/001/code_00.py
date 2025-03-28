"""
This module transforms an input grid based on the following rules:
1. Identify the largest contiguous rectangular area of gray (5) pixels.
2. Identify four single non-white (0), non-gray (5) pixels located outside the gray rectangle, one conceptually near each corner (top-left, top-right, bottom-left, bottom-right).
3. Create an output grid of the same dimensions as the input, initially filled with white (0).
4. Divide the area corresponding to the original gray rectangle in the output grid into four equal quadrants.
5. Fill each quadrant with the color of the corresponding corner pixel identified in step 2.
   - Top-left quadrant gets the color of the pixel found above and to the left of the gray rectangle.
   - Top-right quadrant gets the color of the pixel found above and to the right.
   - Bottom-left quadrant gets the color of the pixel found below and to the left.
   - Bottom-right quadrant gets the color of the pixel found below and to the right.
"""

import numpy as np
from typing import Tuple, Dict, Optional, List

def find_largest_gray_rectangle(grid: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the bounding box of the largest contiguous rectangular area of gray (5) pixels.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple (min_row, min_col, max_row, max_col) representing the bounding box
        of the largest gray rectangle found, or None if no gray pixels are found
        or the largest gray area is not rectangular.
    """
    height, width = grid.shape
    max_size = 0
    best_bounds = None
    visited = np.zeros_like(grid, dtype=bool)
    gray_color = 5

    for r in range(height):
        for c in range(width):
            # If we find a gray pixel that hasn't been visited yet, start a search
            if grid[r, c] == gray_color and not visited[r, c]:
                component_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Breadth-First Search to find all connected gray pixels
                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    component_pixels.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == gray_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Check if the found component forms a solid rectangle
                current_height = max_r - min_r + 1
                current_width = max_c - min_c + 1
                current_size = current_height * current_width
                
                is_solid_rectangle = True
                if len(component_pixels) != current_size:
                     # The number of pixels in the component doesn't match the bounding box area
                     is_solid_rectangle = False
                else:
                    # Verify all pixels within the bounds are gray and part of the component
                    for rr in range(min_r, max_r + 1):
                        for cc in range(min_c, max_c + 1):
                            if grid[rr, cc] != gray_color or (rr, cc) not in component_pixels:
                                is_solid_rectangle = False
                                break
                        if not is_solid_rectangle:
                            break
                            
                # Update best bounds if this rectangle is larger
                if is_solid_rectangle and current_size > max_size:
                    max_size = current_size
                    best_bounds = (min_r, min_c, max_r, max_c)

    return best_bounds

def find_corner_pixels(grid: np.ndarray, rect_bounds: Tuple[int, int, int, int]) -> Optional[Dict[str, int]]:
    """
    Finds the four corner indicator pixels and their colors relative to the gray rectangle.

    Args:
        grid: A numpy array representing the input grid.
        rect_bounds: The bounding box (min_r, min_c, max_r, max_c) of the gray rectangle.

    Returns:
        A dictionary mapping corner identifiers ('TL', 'TR', 'BL', 'BR') to their colors,
        or None if exactly four corner pixels are not found in the expected positions.
    """
    height, width = grid.shape
    min_row, min_col, max_row, max_col = rect_bounds
    corner_colors = {}
    background_color = 0
    gray_color = 5

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Ignore background and gray pixels
            if color == background_color or color == gray_color:
                continue
            
            # Check if pixel is outside the gray rectangle bounds
            is_outside = r < min_row or r > max_row or c < min_col or c > max_col
            if not is_outside:
                 continue # ignore pixels inside the rect bounds

            # Classify the pixel based on its relative position to the rectangle
            if r < min_row and c < min_col:
                # Potential Top-Left
                if 'TL' in corner_colors: return None # Found multiple TL pixels
                corner_colors['TL'] = color
            elif r < min_row and c > max_col:
                # Potential Top-Right
                if 'TR' in corner_colors: return None # Found multiple TR pixels
                corner_colors['TR'] = color
            elif r > max_row and c < min_col:
                # Potential Bottom-Left
                if 'BL' in corner_colors: return None # Found multiple BL pixels
                corner_colors['BL'] = color
            elif r > max_row and c > max_col:
                # Potential Bottom-Right
                if 'BR' in corner_colors: return None # Found multiple BR pixels
                corner_colors['BR'] = color
            # else: # Pixel is outside but not in a corner region relative to the rect
                 # Based on problem description, we expect exactly 4 such pixels in corners
                 # pass # Ignore these pixels if they exist

    # Check if exactly one pixel was found for each corner
    if len(corner_colors) == 4 and all(k in corner_colors for k in ['TL', 'TR', 'BL', 'BR']):
        return corner_colors
    else:
        # Did not find exactly four corner pixels in the correct relative positions
        return None


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by replacing a central gray rectangle with four quadrants
    colored according to corner indicator pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (white = 0)
    output_np = np.zeros_like(input_np)

    # 1. Find the largest gray rectangle
    rect_bounds = find_largest_gray_rectangle(input_np)
    if rect_bounds is None:
        # Error condition: No suitable gray rectangle found.
        # Based on examples, this shouldn't happen. Return empty grid or raise error.
        print("Error: Could not find the gray rectangle.")
        return output_np.tolist() # Return empty grid

    min_row, min_col, max_row, max_col = rect_bounds

    # 2. Find the four corner indicator pixels and their colors
    corner_colors = find_corner_pixels(input_np, rect_bounds)
    if corner_colors is None:
        # Error condition: Could not find exactly four corner pixels.
        print("Error: Could not find exactly four corner indicator pixels.")
        return output_np.tolist() # Return empty grid

    # 3. Calculate rectangle dimensions and midpoints for quadrants
    rect_height = max_row - min_row + 1
    rect_width = max_col - min_col + 1
    
    # Ensure rectangle dimensions are even as implied by examples for perfect split
    if rect_height % 2 != 0 or rect_width % 2 != 0:
        print(f"Warning: Gray rectangle dimensions ({rect_height}x{rect_width}) are not even.")
        # Proceeding with integer division for midpoints

    mid_row = min_row + rect_height // 2
    mid_col = min_col + rect_width // 2

    # 4. Fill the quadrants in the output grid
    try:
        # Top-Left Quadrant (Color: TL)
        output_np[min_row:mid_row, min_col:mid_col] = corner_colors['TL']
        
        # Top-Right Quadrant (Color: TR)
        # Numpy slicing is exclusive of the end index, so use max_col + 1
        output_np[min_row:mid_row, mid_col:max_col + 1] = corner_colors['TR']
        
        # Bottom-Left Quadrant (Color: BL)
        # Numpy slicing is exclusive of the end index, so use max_row + 1
        output_np[mid_row:max_row + 1, min_col:mid_col] = corner_colors['BL']
        
        # Bottom-Right Quadrant (Color: BR)
        # Numpy slicing is exclusive of the end index, so use max_row + 1 and max_col + 1
        output_np[mid_row:max_row + 1, mid_col:max_col + 1] = corner_colors['BR']
    except KeyError as e:
         print(f"Error: Missing corner color for {e}")
         return output_np.tolist() # Return empty grid if a color is missing
    except IndexError as e:
         print(f"Error: Indexing error during quadrant filling: {e}")
         return output_np.tolist() # Return empty grid

    # 5. Convert the resulting numpy array back to a list of lists and return
    return output_np.tolist()