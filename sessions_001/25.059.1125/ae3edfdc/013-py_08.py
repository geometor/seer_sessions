import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def is_adjacent(pixel1, pixel2):
    """Checks if two pixels are adjacent (horizontally or vertically)."""
    return (abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1])) == 1

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    output_grid = np.copy(input_grid)
    orange_pixels = find_pixels(input_grid, 7)
    blue_pixels = find_pixels(input_grid, 1)

    # Create a set for efficient checking of orange pixel locations
    orange_set = set(tuple(p) for p in orange_pixels)

    # Continue expanding until no more changes occur
    while True:
        new_orange_set = set(orange_set)  # Copy for iteration
        expansion_occurred = False

        for blue_pixel in blue_pixels:
            # Check for adjacent empty cells to this blue pixel
            for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Adjacent positions
                adj_row, adj_col = blue_pixel[0] + r, blue_pixel[1] + c

                # Check bounds and if the adjacent cell is empty
                if 0 <= adj_row < output_grid.shape[0] and 0 <= adj_col < output_grid.shape[1] and \
                   output_grid[adj_row, adj_col] == 0:

                    # Check if there's an *existing* orange pixel next to *this* empty
                    for orow, ocol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        neighbor_row, neighbor_col = adj_row + orow, adj_col + ocol

                        if (neighbor_row, neighbor_col) in orange_set:
                          #Found a neighbor, set it to orange
                          new_orange_set.add((adj_row,adj_col))
                          output_grid[adj_row, adj_col] = 7
                          expansion_occurred = True

        orange_set = new_orange_set
        if not expansion_occurred:
            break
    return output_grid

# Example grids (replace with actual data from the task)
example_inputs = [
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

example_outputs = [
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 7, 7, 0],
              [0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
              [0, 0, 0, 7, 7, 7, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 7, 7, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0],
              [0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0],
              [0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0],
              [0, 0, 7, 7, 1, 0, 0, 1, 7, 7, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
]


for i, (input_grid, expected_output) in enumerate(zip(example_inputs, example_outputs)):
    transformed_grid = transform(input_grid)
    comparison = np.array_equal(transformed_grid, expected_output)
    print(f"Example {i+1}: {'Success' if comparison else 'Failure'}")
    if not comparison:
        print ("Transformed")
        print(transformed_grid)
        print ("Expected")
        print(expected_output)