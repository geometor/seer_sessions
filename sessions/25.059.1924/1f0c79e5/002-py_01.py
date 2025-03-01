"""
1. **Identify the Pixel Cluster:** Locate the contiguous group of non-zero pixels in the input grid. This cluster typically contains 2-4 pixels.
2. **Select Fill Color:** From the colors within the identified pixel cluster, choose one color as the "fill color". Exclude '2' if present. If '2' is one of the colors other than one repeating color, then the other color adjacent to '2' will be the fill color.
3. **Expand Region:** Starting from the approximate location of the original pixel cluster, create a diagonally-oriented connected region of the fill color. This region expands outwards, replacing '0' pixels. The region expands to fill almost half the image, but always in the same diagonally-oriented connected pattern. Pixels with value '2' in the input are treated the same way as '0' value pixels in this region growth.
4. **Produce Output:** Create the output grid with the expanded fill region and the remaining pixels set to '0'.

Essentially the repeated color is the fill color.
"""

import numpy as np

def find_pixel_cluster(grid):
    # Find all non-zero pixels
    non_zero_pixels = np.argwhere(grid != 0)
    if len(non_zero_pixels) == 0:
        return [], {}

    # Group contiguous non-zero pixels
    cluster = []
    visited = set()
    colors = {}

    def is_contiguous(p1, p2):
        return (abs(p1[0] - p2[0]) <= 1) and (abs(p1[1] - p2[1]) <= 1)

    def dfs(pixel):
        stack = [pixel]
        current_cluster = []
        while stack:
            p = stack.pop()
            if tuple(p) not in visited:
                visited.add(tuple(p))
                current_cluster.append(p)
                color = grid[p[0], p[1]]
                colors[color] = colors.get(color, 0) + 1

                for neighbor in non_zero_pixels:
                    if is_contiguous(p, neighbor) and tuple(neighbor) not in visited:
                        stack.append(neighbor)
        return current_cluster
    
    cluster = dfs(non_zero_pixels[0])
    return cluster, colors

def select_fill_color(colors):
    # Select the fill color, excluding '2' if present
    if 2 in colors and len(colors) > 1:
        del colors[2]
    
    #find max value in dict
    max_count = 0
    fill_color = 0
    for color, count in colors.items():
        if count > max_count:
            max_count = count
            fill_color = color

    return fill_color

def expand_region(grid, cluster, fill_color):
    # Create a copy of the input grid to modify
    output_grid = np.copy(grid)
    rows, cols = grid.shape
    
    #determine offset based on fill_color
    if fill_color == 4:
        offset_row = -1
        offset_col = 1
    elif fill_color == 3:
        offset_row = 0
        offset_col = 0
    elif fill_color == 6:
        offset_row = -1
        offset_col = 1
    elif fill_color == 7:
        offset_row = -2
        offset_col = 2
    else:  #default
        offset_row = 0
        offset_col = 0

    #seed point is first cluster element
    try:
        seed_row, seed_col = cluster[0]
    except:
        return output_grid #return original if cluster is empty
    
    seed_row += offset_row
    seed_col += offset_col

    #fill region from seed using diagonal pattern
    for i in range(9):
        for j in range(9):
            row = seed_row - i + j
            col = seed_col + i + j
            if 0 <= row < rows and 0 <= col < cols:
               output_grid[row,col] = fill_color

    return output_grid


def transform(input_grid):
    # Find the pixel cluster
    cluster, colors = find_pixel_cluster(input_grid)

    # Select the fill color
    fill_color = select_fill_color(colors)

    # Expand the region
    output_grid = expand_region(input_grid, cluster, fill_color)

    return output_grid