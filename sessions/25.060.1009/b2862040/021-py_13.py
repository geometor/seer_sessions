import numpy as np

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output pair and gathers metrics.
    """
    maroon_pixels = np.sum(input_grid == 9)
    blue_pixels = np.sum(input_grid == 1)
    adjacent_maroon_to_blue = 0
    changed_maroon_to_grey = np.sum((input_grid == 9) & (output_grid == 8))

    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 9:
                for r, c in get_adjacent_pixels(input_grid, row, col):
                    if input_grid[r, c] == 1:
                        adjacent_maroon_to_blue += 1
                        break  # Only need to count once per maroon pixel

    rule_holds = (adjacent_maroon_to_blue == changed_maroon_to_grey)

    return {
        "maroon_pixels": maroon_pixels,
        "blue_pixels": blue_pixels,
        "adjacent_maroon_to_blue": adjacent_maroon_to_blue,
        "changed_maroon_to_grey": changed_maroon_to_grey,
        "rule_holds": rule_holds,
    }

def get_adjacent_pixels(grid, row, col):
    """
    Gets the adjacent pixels of a given cell in a grid.
    """
    rows, cols = grid.shape
    adjacent_pixels = []

    # Check above
    if row > 0:
        adjacent_pixels.append((row - 1, col))
    # Check below
    if row < rows - 1:
        adjacent_pixels.append((row + 1, col))
    # Check left
    if col > 0:
        adjacent_pixels.append((row, col - 1))
    # Check right
    if col < cols - 1:
        adjacent_pixels.append((row, col + 1))

    return adjacent_pixels

# Example data (replace with your actual data)
examples = [
    (np.array([[9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9], [9, 9, 1, 9, 9, 9], [9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9]]),
     np.array([[9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9], [9, 9, 1, 9, 9, 9], [9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9]])),

    (np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 1, 9, 9, 1, 9, 9, 1, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9]]),
     np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 1, 9, 9, 1, 9, 9, 1, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9]])),

     (np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]]),
     np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]]))
]

results = [analyze_example(input_grid, output_grid) for input_grid, output_grid in examples]

# Print results in a table format
print("| Example | Maroon Pixels | Blue Pixels | Adjacent Maroon to Blue | Changed to Grey | Rule Holds |")
print("|---------|---------------|-------------|--------------------------|-----------------|------------|")
for i, result in enumerate(results):
    print(f"| {i + 1}       | {result['maroon_pixels']:<13} | {result['blue_pixels']:<11} | {result['adjacent_maroon_to_blue']:<24} | {result['changed_maroon_to_grey']:<15} | {result['rule_holds']:<10} |")