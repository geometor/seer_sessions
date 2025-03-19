"""
1.  **Identify Gray Objects:** Find all contiguous groups of gray (5) pixels.  A group can be any number of pixels.
2.  **Classify Objects:**
    *   **Horizontal Line:** If a gray object consists of 3 or more pixels in a horizontal row, it's a horizontal line.
    *   **Vertical Line:** If a gray object consists of 2 pixels stacked vertically, it's a vertical line.
    *  **3x3 Square:** If a gray object consists of 9 pixels in a square.
    *  **Single Pixel:** Any object not matching above conditions.
3.  **Transform Gray Objects:**
    *   Change horizontal line segments (3+ pixels) to red (2).
    *   Change vertical line segments (2 pixels) to blue (1).
    *   Change gray 3x3 squares to green(3).
    *   For any single gray pixel object:
        * Change single gray pixels that are *adjacent* to horizontal lines, and which are not part of any other shape, to the same color as the nearest other shape.
4.  **Output:** The output grid retains all original pixel values except for the transformed gray pixels.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of pixels of a specified color."""
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_horizontal_line(obj):
    """Checks if an object is a horizontal line segment of length 3 or more."""
    if len(obj) < 3:
        return False
    rows = [r for r, _ in obj]
    return len(set(rows)) == 1

def is_vertical_line(obj):
    """Checks if an object is a vertical line segment of length 2."""
    if len(obj) != 2:
        return False
    cols = [c for _, c in obj]
    return len(set(cols)) == 1

def is_square(obj):
    """check if object is a 3x3 square"""

    if len(obj) != 9:
        return False

    rows = [pos[0] for pos in obj]
    cols = [pos[1] for pos in obj]

    if len(set(rows)) == 3 and len(set(cols)) == 3:
      return True
    
    return False

def distance(r1,c1,r2,c2):
    return abs(r1-r2) + abs(c1 - c2)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all gray objects
    gray_objects = find_objects(input_grid, 5)

    red_objects = []
    blue_objects = []
    green_objects = []

    # Determine the new color for each object
    for obj in gray_objects:
        if is_horizontal_line(obj):
            # Change to red (2)
            for r, c in obj:
                output_grid[r, c] = 2
            red_objects.append(obj)

        elif is_vertical_line(obj):
            #change to blue (1)
            for r,c in obj:
                output_grid[r, c] = 1
            blue_objects.append(obj)

        elif is_square(obj):
            for r,c in obj:
                output_grid[r,c] = 3
            green_objects.append(obj)
        

    for obj in gray_objects:

        if len(obj) == 1:
            r,c = obj[0]

            # find minimum distance from red object
            min_dist_red = 1000
            if len(red_objects) > 0:

                for red in red_objects:
                    for red_r, red_c in red:
                        dist = distance(r,c,red_r,red_c)
                        if dist < min_dist_red:
                            min_dist_red = dist


            # find minimum distance from blue object
            min_dist_blue = 1000
            if len(blue_objects) > 0:
                for blue in blue_objects:
                    for blue_r, blue_c in blue:
                        dist = distance(r,c,blue_r,blue_c)
                        if dist < min_dist_blue:
                            min_dist_blue = dist

            # find minimum distance from green object
            min_dist_green = 1000
            if len(green_objects) > 0:
                for green in green_objects:
                    for green_r, green_c in green:
                        dist = distance(r,c,green_r, green_c)
                        if dist < min_dist_green:
                            min_dist_green = dist

            #prioritize assignment
            if min_dist_red < min_dist_blue and min_dist_red < min_dist_green:
                 output_grid[r,c] = 2
            elif min_dist_blue < min_dist_red and min_dist_blue < min_dist_green:
                output_grid[r,c] = 1
            elif min_dist_green < min_dist_red and min_dist_green < min_dist_blue:
                output_grid[r,c] = 3
            elif min_dist_red == min_dist_blue and min_dist_red < min_dist_green:  #red == blue
                output_grid[r,c] = 2
            elif min_dist_red == min_dist_green and min_dist_red < min_dist_blue:  #red == green
                output_grid[r,c] = 2;
            elif min_dist_blue == min_dist_green and min_dist_blue < min_dist_red: #blue == green
                output_grid[r,c] = 1
            else: # red == blue == green
                output_grid[r,c] = 2


    return output_grid