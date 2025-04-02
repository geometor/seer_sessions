```python
import numpy as np
from typing import List, Tuple

"""
Identify the single non-background color in the input grid. Find the minimum 
bounding box that encloses all pixels of this color. Create an output grid of 
the same dimensions as the input, initialized with the background color (0). 
Draw the perimeter of the calculated bounding box onto the output grid using 
the identified non-background color.
"""

def find_non_background_pixels(grid: np.ndarray) -> Tuple[int, np.ndarray, np.ndarray]:
    """
    Finds the non-background color and the coordinates of pixels with that color.
    Assumes only one non-background color is relevant based on examples.
    
    Args:
        grid: The input grid as a NumPy array.
        
    Returns:
        A tuple containing:
        - marker_color (int): The non-background color found. Returns 0 if none found.
        - rows (np.ndarray): Array of row indices of the marker pixels.
        - cols (np.ndarray): Array of column indices of the marker pixels.
    """
    non_background_indices = np.where(grid != 0)
    if non_background_indices[0].size == 0:
        # No non-background pixels found
        return 0, np.array([]), np.array([])
        
    # Assume the color of the first found non-background pixel is the marker color
    marker_color = grid[non_background_indices[0][0], non_background_indices[1][0]]
    
    # Filter indices to only include those with the determined marker_color
    # (This handles cases where other non-zero colors might accidentally be present,
    # although examples suggest only one relevant color)
    marker_indices = np.where(grid == marker_color)
    
    return marker_color, marker_indices[0], marker_indices[1]

def calculate_bounding_box(rows: np.ndarray, cols: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Calculates the min/max row/col for the bounding box.
    
    Args:
        rows: Array of row indices.
        cols: Array of column indices.
        
    Returns:
        A tuple containing (min_row, max_row, min_col, max_col).
    """
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return min_row, max_row, min_col, max_col

def draw_perimeter(grid: np.ndarray, bounds: Tuple[int, int, int, int], color: int) -> None:
    """
    Draws the perimeter of the bounding box onto the grid in place.
    
    Args:
        grid: The grid (NumPy array) to draw on.
        bounds: A tuple (min_row, max_row, min_col, max_col).
        color: The color to use for drawing.
    """
    min_row, max_row, min_col, max_col = bounds
    
    # Draw top edge
    grid[min_row, min_col:max_col+1] = color
    # Draw bottom edge
    grid[max_row, min_col:max_col+1] = color
    # Draw left edge (excluding corners already drawn)
    grid[min_row+1:max_row, min_col] = color
    # Draw right edge (excluding corners already drawn)
    grid[min_row+1:max_row, max_col] = color
    

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by finding the bounding box of non-background 
    pixels and drawing its perimeter on a new grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid with the drawn perimeter.
    """
    # Convert input to NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid with the same shape as input, filled with background color (0)
    output_grid = np.zeros_like(input_array)
    
    # Find the marker color and the locations of all pixels with that color
    marker_color, rows, cols = find_non_background_pixels(input_array)
    
    # If no marker pixels were found, return the empty grid
    if marker_color == 0 or rows.size == 0:
        return output_grid.tolist()
        
    # Calculate the bounding box coordinates
    bounds = calculate_bounding_box(rows, cols)
    
    # Draw the perimeter of the bounding box onto the output grid
    draw_perimeter(output_grid, bounds, marker_color)
    
    # Convert the output NumPy array back to a list of lists
    return output_grid.tolist()

```