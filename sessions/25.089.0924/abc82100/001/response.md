```python
import numpy as np
from collections import Counter

"""
The transformation rule depends on specific features present in the input grid.

1.  Check for a Vertical Red Line: If a contiguous vertical line of Red (2) exists spanning the grid's height:
    - The Red line itself turns Blue (1).
    - The area to the left of the line is filled with Red (2).
    - The area to the right (excluding the original line) is filled with white (0).

2.  Check for Azure: If no vertical Red line is found, check for the presence of Azure (8).
    - If Azure (8) exists:
        a. Count the frequency of all non-white (0) and non-azure (8) colors.
        b. Identify the color with the highest frequency (Most Frequent Color - MFC).
        c. If MFC is Blue (1):
            - Find the largest contiguous Blue (1) object.
            - Create a white output grid.
            - Draw the largest Blue object onto the output grid, but colored Red (2).
        d. If MFC is Magenta (6):
            - Create an intermediate grid: Magenta(6)->Orange(7), Orange(7)->Magenta(6), Red(2)->Yellow(4), Yellow(4)->Red(2). Azure(8) and all other colors become white(0).
            - Initialize the final output grid from this intermediate grid.
            - Iterate through the *original* input grid. If an input pixel is Magenta(6) and the pixel below it is white(0), color the corresponding pixel below in the *output* grid Orange(7).
            - Similarly, if an input pixel is Orange(7) and the pixel below it is white(0), color the corresponding pixel below in the *output* grid Magenta(6).
        e. If MFC is Yellow (4):
            - Create a white output grid.
            - Iterate through the input grid. If a pixel is Yellow(4), set the output pixel to Red(2). If a pixel is Blue(1), set the output pixel to Orange(7). Other colors remain white.

3.  Default Case: If neither a vertical Red line nor Azure is present, return the input grid unchanged (based on the lack of examples for this scenario).
"""

def find_objects(grid, color):
    """Finds all contiguous objects of a given color."""
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def find_vertical_line_column(grid, color):
    """Checks for a vertical line of a specific color and returns its column index."""
    height, width = grid.shape
    for c in range(width):
        is_line = True
        for r in range(height):
            if grid[r, c] != color:
                is_line = False
                break
        if is_line:
            return c
    return None

def get_color_counts(grid):
    """Counts the frequency of non-white (0) and non-azure (8) colors."""
    counts = Counter()
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != 0 and color != 8:
                counts[color] += 1
    return counts

def transform(input_grid):
    """
    Applies the transformation rule based on the presence of a vertical red line
    or the most frequent color alongside azure.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    output_grid = np.array(input_grid_np, dtype=int) # Start with a copy, modify as needed

    # 1. Check for Vertical Red Line
    red_line_col = find_vertical_line_column(input_grid_np, 2)
    if red_line_col is not None:
        output_grid = np.zeros_like(input_grid_np) # Start fresh for this rule
        # a. Fill left side with Red (2)
        output_grid[:, :red_line_col] = 2
        # b. Change line itself to Blue (1)
        output_grid[:, red_line_col] = 1
        # c. Right side is already white (0) due to initialization
        return output_grid.tolist()

    # 2. Check for Azure (8)
    if 8 in input_grid_np:
        color_counts = get_color_counts(input_grid_np)

        # Handle cases where there are no non-white, non-azure colors
        if not color_counts:
             # If only white and azure exist, specific rules might apply,
             # but based on examples, perhaps clear the grid?
             # Let's clear Azure for now, consistent with other Azure rules.
             output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
             return output_grid.tolist()


        mfc = max(color_counts, key=color_counts.get)

        # 2.c. MFC is Blue (1)
        if mfc == 1:
            blue_objects = find_objects(input_grid_np, 1)
            if not blue_objects: # Should not happen if blue is MFC, but safe check
                output_grid = np.zeros_like(input_grid_np)
                return output_grid.tolist()

            largest_blue_object = max(blue_objects, key=len)
            output_grid = np.zeros_like(input_grid_np) # Start with white grid
            for r, c in largest_blue_object:
                output_grid[r, c] = 2 # Change to Red
            return output_grid.tolist()

        # 2.d. MFC is Magenta (6)
        elif mfc == 6:
            intermediate_grid = np.zeros_like(input_grid_np)
            # Apply initial swaps and removals
            for r in range(height):
                for c in range(width):
                    color = input_grid_np[r, c]
                    if color == 6: # Magenta -> Orange
                        intermediate_grid[r, c] = 7
                    elif color == 7: # Orange -> Magenta
                        intermediate_grid[r, c] = 6
                    elif color == 2: # Red -> Yellow
                        intermediate_grid[r, c] = 4
                    elif color == 4: # Yellow -> Red
                        intermediate_grid[r, c] = 2
                    # Azure (8) and other colors become white (0) implicitly

            output_grid = np.array(intermediate_grid) # Copy intermediate to final output

            # Apply row duplication logic based on *original* input
            for r in range(height - 1): # Iterate up to second to last row
                for c in range(width):
                    input_color = input_grid_np[r, c]
                    below_input_color = input_grid_np[r + 1, c]

                    if input_color == 6 and below_input_color == 0: # Magenta above white
                        output_grid[r + 1, c] = 7 # Color below Orange
                    elif input_color == 7 and below_input_color == 0: # Orange above white
                        output_grid[r + 1, c] = 6 # Color below Magenta

            return output_grid.tolist()

        # 2.e. MFC is Yellow (4)
        elif mfc == 4:
            output_grid = np.zeros_like(input_grid_np) # Start with white grid
            for r in range(height):
                for c in range(width):
                    color = input_grid_np[r, c]
                    if color == 4: # Yellow -> Red
                        output_grid[r, c] = 2
                    elif color == 1: # Blue -> Orange
                        output_grid[r, c] = 7
                    # Other colors (including Azure, original Red, original Orange) remain white
            return output_grid.tolist()
        else:
            # If MFC is some other color (not covered by examples),
            # potentially remove Azure and return? For now, remove Azure.
             output_grid = np.where(input_grid_np == 8, 0, input_grid_np)
             return output_grid.tolist()


    # 3. Default Case: No vertical red line and no Azure
    # Return the input grid unchanged as per instruction
    return input_grid_np.tolist()
```