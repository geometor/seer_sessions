import copy

"""
Transforms a 1D input grid based on identifying a specific color pattern and isolated instances of that color.
First, it identifies the color 'C' from the first occurrence of a sequence of three identical adjacent non-zero pixels (C C C) in the input grid.
Then, it scans the input grid for any pixel of color 'C' located at index 'i' whose immediate neighbors (at i-1 and i+1) are *not* color 'C'.
For each such 'isolated' pixel found in the input grid, it modifies a copy of the grid (the output grid) by setting the pixels at indices i-1, i, and i+1 to color 'C'.
All other pixels, including the original 'C C C' blocks, remain unchanged in the output grid unless they are part of the neighborhood of an isolated 'C' that gets transformed.
If no 'C C C' pattern is found initially, or the grid is too short to contain such a pattern or an isolated pixel with neighbors, the original grid is returned unchanged.
"""

def find_pattern_color(grid):
    """
    Finds the color of the first sequence of three identical adjacent non-zero pixels.

    Args:
        grid (list): The 1D input grid.

    Returns:
        int or None: The color (int) of the pattern if found, otherwise None.
    """
    grid_len = len(grid)
    # Need at least 3 elements to find the pattern C C C
    if grid_len < 3:
        return None

    for i in range(grid_len - 2):
        # Check for non-zero color
        if grid[i] != 0:
            # Check for three identical adjacent pixels
            if grid[i] == grid[i+1] == grid[i+2]:
                return grid[i] # Return the color of the pattern
    return None # No pattern found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A 1D list representing the input grid row.

    Returns:
        list: A 1D list representing the transformed output grid row.
    """
    # 1. Create a copy of the input grid to modify for the output.
    output_grid = copy.deepcopy(input_grid)
    grid_len = len(input_grid)

    # Handle grids too short to contain the 3-pixel pattern or an isolated pixel with neighbors.
    if grid_len < 3:
        return output_grid # Return the copy unchanged

    # 2. Scan the input grid to find the pattern color 'C'.
    pattern_color = find_pattern_color(input_grid)

    # 3. If no pattern color 'C' is found, return the original grid copy.
    if pattern_color is None:
        return output_grid

    # 4. Iterate through the input grid to find isolated pixels.
    # Loop bounds ensure we can safely access i-1 and i+1.
    for i in range(1, grid_len - 1):
        # 5. Check if the current pixel in the *input* grid has the pattern color.
        if input_grid[i] == pattern_color:
            # 6. Check if its neighbors in the *input* grid are *not* the pattern color.
            if input_grid[i-1] != pattern_color and input_grid[i+1] != pattern_color:
                # 7. If it's an isolated pixel, modify the *output* grid.
                # Change the neighborhood [i-1, i, i+1] to 'C C C'.
                output_grid[i-1] = pattern_color
                output_grid[i]   = pattern_color # Ensure the center is set (might be redundant but safe)
                output_grid[i+1] = pattern_color

    # 8. Return the modified output grid.
    return output_grid