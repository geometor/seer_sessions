"""
1.  **Identify Key Colors:** Determine the colors in the input grid that are *not* the most frequent (dominant) color. These are the "key" colors.
2.  **Locate Key Color Instances:**  For each key color, find the (row, column) coordinates of all pixels of that color.
3.  **Determine Output Pattern and Size**: Analyze the spatial relationship between groups of pixels of key colours and use this to determine output size
    *   If there are four key colors and each occurs in four pixels forming corners of rectangles, the output is likely a set of concentric rectangles. The output size is 5x5.
    *   If two key colors exist and four pixels of each form corners of rectangles, output is likely two concentric rectangles. Output size 5x5.
    *  If there are two key colors, and one forms a "plus" shape, while another forms a rectangle/square encompassing it. Output size will be 3x3
4. **Construct Output Grid**:
    *   **Concentric Rectangles:** Create a 5x5 output grid. Place the key colors as corners of concentric rectangles, working inwards. The outermost rectangle uses the color that formed the rectangle with a corner closest to [0,0]. The next inner one uses color with next further, and so on.
    *   **Rectangle with Plus:**  Create a 3x3 output grid. The color forming the corners of outermost rectangle will now form a solid filled rectangle. The "plus" shape color is placed in a plus shape (+) in the output, with color 1 placed at the center.
    * **Background:** If the input dominant colour and the output dominant colour match, then maintain the dominant colour as the output background (fill all cells of output with dominant input colour, and 'draw on top'.) Otherwise, create a new background with 0
5.  **Return:** Return the constructed output grid.
"""

import numpy as np
from collections import Counter

def get_dominant_color(grid):
    """Finds the most frequent color in the grid."""
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    dominant_color = color_counts.most_common(1)[0][0]
    return dominant_color

def find_key_colors(grid):
    """Identifies colors that are not the dominant color."""
    dominant_color = get_dominant_color(grid)
    return [color for color in np.unique(grid) if color != dominant_color]

def get_pixel_positions(grid, color):
    """Returns a list of (row, col) tuples for all pixels of the given color."""
    return np.argwhere(grid == color).tolist()

def is_rectangle_corners(positions):
    """Checks if the given positions form the corners of a rectangle."""
    if len(positions) != 4:
        return False
    
    rows = sorted(list(set([r for r, c in positions])))
    cols = sorted(list(set([c for r, c in positions])))

    if len(rows) != 2 or len(cols) != 2:
        return False;

    expected_corners = [[rows[0], cols[0]], [rows[0], cols[1]], [rows[1], cols[0]], [rows[1], cols[1]]]

    return all([corner in positions for corner in expected_corners])


def find_rectangle_corners_closest_to_origin(positions):
     """Of the corners, find one which is closest to origin"""
     min_dist = float('inf')
     closest_corner = None

     for r,c in positions:
        dist = (r**2 + c**2)
        if dist< min_dist:
            min_dist = dist
            closest_corner = (r,c)

     return closest_corner


def transform(input_grid):
    input_grid = np.array(input_grid)
    key_colors = find_key_colors(input_grid)
    dominant_color = get_dominant_color(input_grid)
    key_color_positions = {color: get_pixel_positions(input_grid, color) for color in key_colors}

    # Determine output pattern and size
    if len(key_colors) == 4 and all(is_rectangle_corners(key_color_positions[color]) for color in key_colors):
        # Concentric rectangles pattern
        output_grid = np.full((5, 5), dominant_color)
        
        # Sort colors based on distance of their closest corner to origin
        sorted_colors = sorted(key_colors, key=lambda color: find_rectangle_corners_closest_to_origin(key_color_positions[color])[0] + find_rectangle_corners_closest_to_origin(key_color_positions[color])[1] )


        output_grid[0, 0] = sorted_colors[0]
        output_grid[0, 4] = sorted_colors[0]
        output_grid[4, 0] = sorted_colors[0]
        output_grid[4, 4] = sorted_colors[0]

        output_grid[0, 1] = sorted_colors[1]
        output_grid[0, 3] = sorted_colors[1]
        output_grid[4, 1] = sorted_colors[1]
        output_grid[4, 3] = sorted_colors[1]

        output_grid[1, 0] = sorted_colors[3]
        output_grid[1, 4] = sorted_colors[3]
        output_grid[3, 0] = sorted_colors[3]
        output_grid[3, 4] = sorted_colors[3]

        output_grid[0, 2] = sorted_colors[2]
        output_grid[2, 0] = sorted_colors[2]
        output_grid[2, 4] = sorted_colors[2]
        output_grid[4, 2] = sorted_colors[2]
        
    elif len(key_colors) == 2 and all(is_rectangle_corners(key_color_positions[color]) for color in key_colors):
        output_grid = np.full((5,5), dominant_color)

        sorted_colors = sorted(key_colors, key=lambda color: find_rectangle_corners_closest_to_origin(key_color_positions[color])[0] + find_rectangle_corners_closest_to_origin(key_color_positions[color])[1] )

        output_grid[0, 0] = sorted_colors[0]
        output_grid[0, 4] = sorted_colors[0]
        output_grid[4, 0] = sorted_colors[0]
        output_grid[4, 4] = sorted_colors[0]

        output_grid[0, 2] = sorted_colors[1]
        output_grid[2, 0] = sorted_colors[1]
        output_grid[2, 4] = sorted_colors[1]
        output_grid[4, 2] = sorted_colors[1]

    elif len(key_colors) == 2:
        # Rectangle with plus pattern
        output_grid = np.zeros((3, 3), dtype=int)
        color1 = key_colors[0]
        color2 = key_colors[1]

        #Determine which one is rectangle
        if is_rectangle_corners(key_color_positions[color1]):
            rect_color = color1
            plus_color = color2
        else:
            rect_color = color2
            plus_color = color1

        #fill rectangle
        for r in range(3):
          for c in range(3):
            output_grid[r,c] = rect_color
        
        #make plus
        output_grid[1,1] = 1
        output_grid[0,1] = plus_color
        output_grid[1,0] = plus_color
        output_grid[1,2] = plus_color
        output_grid[2,1] = plus_color


    else:
        output_grid = np.full((5, 5), dominant_color)  # Default case

    return output_grid.tolist()