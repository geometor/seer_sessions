import numpy as np
import copy

"""
1. Identify all gray pixels (color 5) in the input grid.
2. For each gray pixel, examine its 8 neighbours (orthogonal and diagonal).
3. Count the number of distinct non-white (0) and non-gray (5) colors among these neighbours.
4. Based on the count:
    a. If zero distinct colors: The gray pixel becomes white (0).
    b. If one distinct color C: The gray pixel becomes color C.
    c. If two or more distinct colors: The gray pixel becomes white (0), AND its column is marked for removal.
5. Create a modified grid by applying the color changes from step 4.
6. Construct the final output grid by removing the marked columns from the modified grid.
"""

def get_neighbors(grid: np.ndarray, r: int, c: int) -> list[tuple[int, int, int]]:
    """
    Gets the 8 neighbours (value, row, col) of a pixel at (r, c), handling grid boundaries.
    """
    neighbours = []
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the center pixel itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbours.append((grid[nr, nc], nr, nc))
    return neighbours

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the rules derived from gray pixel neighbourhoods.
    """
    input_array = np.array(input_grid, dtype=int)
    working_grid = np.copy(input_array)
    rows, cols = input_array.shape

    columns_to_remove = set()
    modifications = [] # Store modifications as (r, c, new_color)

    # Iterate through each pixel to find gray pixels and determine modifications
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == 5: # Found a gray pixel
                neighbours = get_neighbors(input_array, r, c)

                # Filter for non-white, non-gray neighbours
                colored_neighbours = [n for n in neighbours if n[0] != 0 and n[0] != 5]

                # Get distinct colors of these neighbours
                distinct_colors = set(n[0] for n in colored_neighbours)
                num_distinct_colors = len(distinct_colors)

                if num_distinct_colors == 0:
                    # Case a: Isolated gray pixel or only white/gray neighbours
                    modifications.append((r, c, 0)) # Becomes white
                elif num_distinct_colors == 1:
                    # Case b: One distinct neighbour color
                    the_color = list(distinct_colors)[0]
                    modifications.append((r, c, the_color)) # Becomes that color
                else: # num_distinct_colors >= 2
                    # Case c: Two or more distinct neighbour colors
                    modifications.append((r, c, 0)) # Becomes white
                    columns_to_remove.add(c) # Mark column for removal

    # Apply all modifications to the working grid
    for r, c, new_color in modifications:
        working_grid[r, c] = new_color

    # Construct the output grid by removing marked columns
    output_cols = []
    for c in range(cols):
        if c not in columns_to_remove:
            output_cols.append(working_grid[:, c])

    # Handle the case where all columns might be removed
    if not output_cols:
        # If output_cols is empty, create an empty grid with the original number of rows
        # Or potentially a grid of size rows x 0 depending on expected output format.
        # Let's assume rows x 0 for now.
         output_grid_array = np.empty((rows, 0), dtype=int)
    else:
        # Stack the kept columns horizontally
        output_grid_array = np.stack(output_cols, axis=1)


    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_array.tolist()

    return output_grid