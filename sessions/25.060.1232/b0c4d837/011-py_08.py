import numpy as np

def find_rectangle_by_color(grid, color):
    """Finds the top-left and bottom-right coordinates of a rectangle of a specific color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No rectangle found
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def analyze_example(input_grid, output_grid):
    azure_rect = find_rectangle_by_color(input_grid, 8)
    if azure_rect:
        top_left, bottom_right = azure_rect
        width = bottom_right[1] - top_left[1] + 1
        height = bottom_right[0] - top_left[0] + 1
        print(f"  Azure Rectangle: Top-Left: {top_left}, Bottom-Right: {bottom_right}, Width: {width}, Height: {height}")
        print(f"Output dimensions: {output_grid.shape}")
        print(f"Output grid: \n {output_grid}")
    else:
        print("  No Azure Rectangle found.")

#Dummy examples to avoid error on code execution
example_grids = [
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
     np.array([[8, 8, 8],
              [0, 0, 0],
              [0, 0, 0]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
             [5, 8, 8, 8, 8, 8, 8, 8, 5],
             [5, 8, 8, 8, 8, 8, 8, 8, 5],
             [5, 8, 8, 8, 8, 8, 8, 8, 5],
             [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    np.array([[8, 8, 8],
              [0, 0, 0],
              [0, 0, 0]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
     np.array([[8, 8, 8],
              [0, 0, 0],
              [0, 0, 0]]))
]

for i, (input_grid, output_grid) in enumerate(example_grids):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
