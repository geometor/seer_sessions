"""
Transforms the input grid based on a conditional color change rule determined by neighbor counts. 
The rule identifies two non-background colors in the grid. One color is designated the 'Loser' (L) and the other the 'Winner' (W). 
A pixel with the Loser color L changes to the Winner color W if the number of its 8 neighbors (including diagonals) that have the Winner color W meets or exceeds a specific threshold. 
The Loser color, Winner color, and the Threshold value are determined by the specific pair of non-background colors present, based on observations from training examples:
- Pair {Red(2), Green(3)}: L=2, W=3, Threshold=3.
- Pair {Magenta(6), Orange(7)}: L=7, W=6, Threshold=4.
Pixels that are background (0), already the Winner color, or Loser color pixels that do not meet the neighbor threshold remain unchanged.
"""

import copy

def get_neighbors(r, c, height, width):
    """
    Gets coordinates of up to 8 neighbors (including diagonals) for a cell (r, c)
    within the grid bounds.
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the neighbor-count-threshold color transformation rule.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])

    # 1. Identify the two non-background colors
    colors = set()
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] != 0:
                colors.add(input_grid[r][c])

    # Expect exactly two non-background colors
    if len(colors) != 2:
        # If not exactly two non-background colors, return the original grid copy
        return output_grid

    color_list = list(colors)
    c1, c2 = color_list[0], color_list[1]

    # 2. Determine Loser (L), Winner (W) colors and Threshold based on the color pair
    loser_color = -1
    winner_color = -1
    threshold = -1

    if {c1, c2} == {2, 3}:  # Red(2) vs Green(3)
        loser_color = 2
        winner_color = 3
        threshold = 3
    elif {c1, c2} == {6, 7}:  # Magenta(6) vs Orange(7)
        loser_color = 7
        winner_color = 6
        threshold = 4
    else:
        # If the color pair is not one of the known pairs, return the original grid copy
        return output_grid

    # 3. Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # 4. Check if the current cell has the Loser color
            if input_grid[r][c] == loser_color:
                winner_neighbor_count = 0
                # 4a. Get neighbors
                neighbors = get_neighbors(r, c, height, width)
                # 4b. Count neighbors with the Winner color in the *input* grid
                for nr, nc in neighbors:
                    if input_grid[nr][nc] == winner_color:
                        winner_neighbor_count += 1

                # 4c. Check if the count meets or exceeds the threshold
                if winner_neighbor_count >= threshold:
                    # 4d. Change the color in the output grid
                    output_grid[r][c] = winner_color

    # 5. Return the transformed grid
    return output_grid