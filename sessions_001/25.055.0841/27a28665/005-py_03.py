import numpy as np

def analyze_example(input_grid, expected_output):
    print(f"Input Grid:\n{input_grid}")
    print(f"Expected Output: {expected_output}")

    gray_pixels = np.argwhere(input_grid == 5)
    print(f"Gray Pixel Coordinates: {gray_pixels}")

    for r, c in gray_pixels:
        print(f"Analyzing pixel at ({r}, {c}):")
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0):
                    continue  # Skip the pixel itself
                nr, nc = r + i, c + j
                if 0 <= nr < input_grid.shape[0] and 0 <= nc < input_grid.shape[1]:
                    neighbors.append(input_grid[nr, nc])
                else:
                    neighbors.append(-1)  # Indicate out of bounds
        print(f"  Neighboring pixel values: {neighbors}")

# Example Input and Output
input_grids = [
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 5, 5, 5, 0, 0],
              [0, 5, 5, 5, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0],
              [0, 5, 5, 5, 0],
              [0, 5, 5, 5, 0],
              [0, 5, 5, 5, 0],
              [0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0],
              [0, 5, 5, 0],
              [0, 5, 5, 0],
              [0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0],
              [0, 0, 5, 5, 0, 0],
              [0, 0, 5, 5, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0],
               [0, 5, 5, 0, 0],
               [0, 5, 5, 0, 0],
               [0, 0, 0, 0, 0]])
]

expected_outputs = [
    np.array([[0]]),
    np.array([[1]]),
    np.array([[1]]),
    np.array([[0]]),
    np.array([[0]])
]
#run the code and print
for i, (input_grid, expected_output) in enumerate(zip(input_grids, expected_outputs)):
    print(f"--- Example {i+1} ---")
    analyze_example(input_grid, expected_output)
