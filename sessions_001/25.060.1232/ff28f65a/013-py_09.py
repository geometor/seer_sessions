import numpy as np

def find_squares(grid, color, size):
    """Finds top-left coordinates of squares of a specific color and size."""
    squares = []
    height, width = grid.shape
    for y in range(height - size + 1):
        for x in range(width - size + 1):
            if grid[y, x] == color and np.all(grid[y:y+size, x:x+size] == color):
                squares.append((x, y))  # Note: Appending (x, y)
    return squares

# Example data (replace with actual data from the task)

example_inputs = [
    np.array([[5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0, 5, 0],
              [5, 0, 2, 2, 0, 2, 2, 0, 5],
              [0, 5, 2, 2, 0, 2, 2, 0, 5],
              [5, 0, 5, 0, 5, 0, 5, 0, 5]]),
    np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 2, 2, 5, 5, 2, 2, 5, 5, 5],
               [5, 5, 5, 2, 2, 5, 5, 2, 2, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5],
              [0, 5, 0, 5, 0, 2, 2, 0, 5, 0],
              [0, 5, 0, 5, 0, 2, 2, 0, 5, 0],
              [0, 5, 0, 5, 0, 5, 0, 5, 0, 5]]),
    np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 2, 2, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 2, 2, 9, 9, 9, 9, 9]]),
    np.array([[2, 2, 7, 7, 7, 7],
              [2, 2, 7, 7, 7, 7],
              [7, 7, 2, 2, 7, 7],
              [7, 7, 2, 2, 7, 7],
              [7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7],
              [7, 7, 7, 7, 7, 7]])
]

example_outputs = [
    np.array([[1, 0, 1, 0, 1]]),
    np.array([[1, 1, 1, 1]]),
    np.array([[1, 0, 1]]),
    np.array([[1]]),
    np.array([[1,1],
              [1,1]])
]

for i, (input_grid, output_grid) in enumerate(zip(example_inputs, example_outputs)):
    red_squares = find_squares(input_grid, 2, 2)
    print(f"Example {i+1}:")
    print(f"  Input shape: {input_grid.shape}")
    print(f"  Output shape: {output_grid.shape}")
    print(f"  Red squares found (top-left coords): {red_squares}")
    for x,y in red_squares:
        ix = x - (input_grid.shape[1] - output_grid.shape[1])
        iy = y - (input_grid.shape[0] - output_grid.shape[0])

        print(f"  checking placement: {ix}, {iy}")
        if ix >= 0 and iy >= 0 and ix < output_grid.shape[1] and iy < output_grid.shape[0]:

            print(f"  Pixel at output[{iy}, {ix}]: {output_grid[iy, ix]}")
        else:
            print(f"  coordinates {ix, iy} are out of bounds")
