import numpy as np
from typing import List, Tuple, Dict

def get_largest_black_rectangle(grid):
    """Finds the largest black rectangle in a grid."""
    black_pixels = np.argwhere(grid == 0)
    if len(black_pixels) == 0:
        return None  # No black pixels

    min_row, min_col = black_pixels.min(axis=0)
    max_row, max_col = black_pixels.max(axis=0)

    # Check if it forms a rectangle
    expected_size = (max_row - min_row + 1) * (max_col - min_col + 1)
    actual_size = np.sum(grid[min_row:max_row+1, min_col:max_col+1] == 0)

    if expected_size == actual_size:
        return (min_row, min_col, max_row, max_col)
    else:
        return None
        
def find_black_rectangles(grid: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Finds all black rectangles in a grid.
    Returns a list of tuples: (min_row, min_col, max_row, max_col)
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    rectangles = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols and grid[r, c] == 0 and not visited[r, c]

    def dfs(r, c, min_r, min_c, max_r, max_c):
        visited[r, c] = True
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if is_valid(nr, nc):
                min_r, min_c, max_r, max_c = dfs(nr, nc, min_r, min_c, max_r, max_c)
        return min_r, min_c, max_r, max_c

    for r in range(rows):
        for c in range(cols):
            if is_valid(r, c):
                min_r, min_c, max_r, max_c = dfs(r, c, r, c, r, c)
                rectangles.append((min_r, min_c, max_r, max_c))
    return rectangles
    
def analyze_example(input_grid: np.ndarray, output_grid: np.ndarray) -> Dict:
    """Analyzes a single input-output pair and returns a dictionary of metrics."""

    input_dims = input_grid.shape
    output_dims = output_grid.shape
    input_colors = np.unique(input_grid).tolist()
    output_colors = np.unique(output_grid).tolist()

    black_rectangles_input = find_black_rectangles(input_grid)
    # largest_black_rect_input = get_largest_black_rectangle(input_grid)


    report = {
        "input_dimensions": input_dims,
        "output_dimensions": output_dims,
        "input_colors": input_colors,
        "output_colors": output_colors,
        "black_rectangles_input": black_rectangles_input,
        # "largest_black_rectangle_input": largest_black_rect_input,
    }
    return report

def pretty_print_report(report: Dict):
    """Prints the report in a human-readable format."""
    print("Analysis Report:")
    for key, value in report.items():
        print(f"  {key}: {value}")

# Example Usage (assuming train_input_0, train_output_0, etc. are defined)
examples = [
    (train_input_0, train_output_0),
    (train_input_1, train_output_1),
    (train_input_2, train_output_2)
]

reports = []
for i, (input_grid, output_grid) in enumerate(examples):
  print(f"\n--- Example {i} ---")
  report = analyze_example(input_grid, output_grid)
  pretty_print_report(report)
  reports.append(report)