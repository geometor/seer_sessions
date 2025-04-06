import copy

"""
1. Take the input 3x3 grid.
2. Create a second 3x3 grid by horizontally flipping each row of the input grid (reversing the order of elements in each row).
3. Concatenate the original input grid and the horizontally flipped grid side-by-side, placing the flipped grid to the right, to form a 3x6 grid (the top half of the output).
4. Create the bottom half of the output by vertically flipping the 3x6 grid created in step 3 (reversing the order of its rows).
5. Concatenate the top half (from step 3) and the bottom half (from step 4) vertically, placing the bottom half below the top half, to form the final 6x6 output grid.
"""

def flip_horizontal(grid: list[list[int]]) -> list[list[int]]:
    """Reverses the order of elements within each row of the grid."""
    flipped = []
    for row in grid:
        flipped.append(row[::-1]) # Use slicing to reverse the row
    return flipped

def flip_vertical(grid: list[list[int]]) -> list[list[int]]:
    """Reverses the order of rows in the grid."""
    return grid[::-1] # Use slicing to reverse the list of rows

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 3x3 input grid into a 6x6 output grid by:
    1. Creating a horizontally flipped version of the input.
    2. Concatenating the original and flipped versions horizontally to form the top half.
    3. Creating the bottom half by vertically flipping the top half.
    4. Concatenating the top and bottom halves vertically.
    """

    # 1. Input grid is provided as input_grid

    # 2. Create a horizontally flipped version of the input grid
    horizontally_flipped_grid = flip_horizontal(input_grid)

    # 3. Create the top half (3x6) by concatenating original and flipped grids row by row
    top_half_output = []
    num_rows = len(input_grid)
    if num_rows == 0:
        return [] # Handle empty input grid

    for i in range(num_rows):
        # Concatenate the i-th row of the original grid with the i-th row of the flipped grid
        new_row = input_grid[i] + horizontally_flipped_grid[i]
        top_half_output.append(new_row)

    # 4. Create the bottom half (3x6) by vertically flipping the top half
    bottom_half_output = flip_vertical(top_half_output)

    # 5. Create the final output grid (6x6) by concatenating top and bottom halves
    output_grid = top_half_output + bottom_half_output

    return output_grid