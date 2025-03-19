import numpy as np
from collections import Counter

def analyze_grid(grid):
    color_counts = Counter(grid.flatten())
    dimensions = grid.shape
    return color_counts, dimensions

def find_contiguous_regions(grid):
    """Finds all contiguous regions of all colors."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = {}

    def dfs(row, col, color, region):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        region.append((row, col))
        dfs(row + 1, col, color, region)
        dfs(row - 1, col, color, region)
        dfs(row, col + 1, color, region)
        dfs(row, col - 1, color, region)

    for row in range(rows):
        for col in range(cols):
            color = grid[row, col]
            if not visited[row, col]:
                region = []
                dfs(row, col, color, region)
                if color not in regions:
                    regions[color] = []
                regions[color].append(region)
    return regions

def calculate_region_extents(region):
    """Calculate the bounding box (min_row, min_col, max_row, max_col) for a region."""
    if not region:
        return None  # Handle empty regions
    min_row = min(r for r, _ in region)
    min_col = min(c for _, c in region)
    max_row = max(r for r, _ in region)
    max_col = max(c for _, c in region)
    return (min_row, min_col, max_row, max_col)

def is_rectangle(region, grid):
   """check if region consists of connected cells forming a rectangle"""
   min_row, min_col, max_row, max_col = calculate_region_extents(region)
   color = grid[region[0][0], region[0][1]]

   for r in range(min_row, max_row + 1):
       for c in range(min_col, max_col + 1):
          if (r,c) not in region:
            return False
          if grid[r,c] != color:
            return False

   return True

def analyze_shapes(grid):
    regions = find_contiguous_regions(grid)
    shapes = {}
    for color, region_list in regions.items():
        shapes[color] = []
        for region in region_list:
            extents = calculate_region_extents(region)
            if is_rectangle(region, grid):              
              shapes[color].append( {"type": "rectangle", "extents": extents})
            else:
              shapes[color].append( {"type": "other", "extents": extents})
    return shapes

examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 5, 5, 5, 0, 0],
                           [0, 5, 1, 1, 1, 1, 1, 5, 0, 0],
                           [0, 5, 1, 1, 1, 1, 1, 5, 0, 0],
                           [0, 5, 1, 1, 1, 1, 1, 5, 0, 0],
                           [0, 5, 5, 5, 5, 5, 5, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1]]),
        "result": np.array([[1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 5, 8, 8, 5, 0, 0, 0],
                           [0, 0, 0, 5, 8, 8, 5, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[8, 8],
                            [8, 8]]),
        "result": np.array([[8, 8],
                            [8, 8]])

    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 5, 5, 5, 0, 0],
                           [0, 5, 1, 1, 1, 1, 5, 0, 0],
                           [0, 5, 1, 1, 1, 1, 5, 0, 0],
                           [0, 5, 1, 1, 1, 1, 5, 0, 0],
                           [0, 5, 5, 5, 5, 5, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[1, 1, 1, 1],
                            [1, 1, 1, 1],
                            [1, 1, 1, 1]]),
        "result": np.array([[1, 1, 1, 1],
                            [1, 1, 1, 1],
                            [1, 1, 1, 1]])

    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 0, 5, 4, 4, 4, 5, 0, 0],
                           [0, 5, 4, 4, 4, 4, 4, 5, 0],
                           [0, 0, 5, 4, 4, 4, 5, 0, 0],
                           [0, 0, 0, 5, 5, 5, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[4, 4, 4],
                            [4, 4, 4],
                            [4, 4, 4]]),
        "result": np.array([])
    }
]

for i, example in enumerate(examples):
    input_color_counts, input_dimensions = analyze_grid(example["input"])
    output_color_counts, output_dimensions = analyze_grid(example["output"])
    result_color_counts, result_dimensions = analyze_grid(example["result"])

    input_shapes = analyze_shapes(example["input"])
    output_shapes = analyze_shapes(example["output"])
    result_shapes = analyze_shapes(example["result"])

    print(f"Example {i+1}:")
    print(f"  Input:  Dimensions: {input_dimensions}, Color Counts: {input_color_counts}, Shapes: {input_shapes}")
    print(f"  Output: Dimensions: {output_dimensions}, Color Counts: {output_color_counts}, Shapes:{output_shapes}")
    print(f"  Result: Dimensions: {result_dimensions}, Color Counts: {result_color_counts}, Shapes:{result_shapes}")
    print("-" * 40)