import numpy as np

def analyze_grid(grid, title=""):
    grid = np.array(grid)
    print(f"--- {title} ---")
    print(f"Shape: {grid.shape}")

    unique_colors = np.unique(grid)
    print(f"Unique Colors: {unique_colors}")

    for color in unique_colors:
        indices = np.where(grid == color)
        coordinates = list(zip(indices[0], indices[1]))
        print(f"Color {color}:")
        print(f"  Count: {len(coordinates)}")
        print(f"  Coordinates: {coordinates}")

        # Check for connectivity (adjacent pixels)
        if len(coordinates) > 1:
            adjacent_count = 0
            for i in range(len(coordinates)):
                for j in range(i + 1, len(coordinates)):
                    y1, x1 = coordinates[i]
                    y2, x2 = coordinates[j]
                    if abs(y1 - y2) <= 1 and abs(x1 - x2) <= 1:
                        adjacent_count += 1
            print(f"  Adjacent Pairs: {adjacent_count}")

def compare_io(in_grid, expected_out, actual_out):
    print("----- comparing -------")
    analyze_grid(in_grid, "Input Grid")
    analyze_grid(expected_out, "Expected Output Grid")
    analyze_grid(actual_out, "Actual Output Grid")

# Example usage for provided I/O grids
compare_io(
    [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 8, 6, 8, 6, 8, 6, 6, 6, 6, 6, 6, 6, 8, 6, 8, 6, 8, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
    [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
)
compare_io(
   [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 8, 6, 8, 6, 8, 6, 6, 6, 8, 6, 8, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
    [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    [[1, 0, 1], [1, 1, 1], [1, 0, 1]]
)
compare_io(
    [[6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
    [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
)