import numpy as np

def transform(input_grid, example_index):
    """Transforms the input grid and prints debugging information."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    print(f"Example {example_index}: Input Grid\n{input_grid}")

    azure_pixels = np.argwhere(input_grid == 8)
    print(f"Example {example_index}: Azure Pixel Locations: {azure_pixels}")


    for row, col in azure_pixels:
        print(f"Example {example_index}: Processing Azure Pixel at ({row}, {col})")
        # Check and place green pixel above.
        if row > 0 and output_grid[row-1, col] != 3 and output_grid[row-1, col] != 8:
            print(f"Example {example_index}: ({row}, {col}) - Placing Green Above")
            output_grid[row-1, col] = 3
        # Check and place green pixel below.
        if row < rows - 1 and output_grid[row+1, col] != 3 and output_grid[row+1, col] != 8:
            print(f"Example {example_index}: ({row}, {col}) - Placing Green Below")
            output_grid[row+1, col] = 3
        # Check and place green pixel to the left.
        if col > 0 and output_grid[row, col-1] != 3 and output_grid[row, col-1] != 8:
            print(f"Example {example_index}: ({row}, {col}) - Placing Green Left")
            output_grid[row, col-1] = 3
        # Check and place green pixel to the right.
        if col < cols - 1 and output_grid[row, col+1] != 3 and output_grid[row, col+1] != 8 :
            print(f"Example {example_index}: ({row}, {col}) - Placing Green Right")
            output_grid[row, col+1] = 3

    print(f"Example {example_index}: Output Grid\n{output_grid}")

    return output_grid