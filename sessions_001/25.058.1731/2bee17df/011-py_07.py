import numpy as np

def analyze_example(input_grid, output_grid, result_grid):
    """Analyzes a single example pair and returns relevant metrics."""

    def get_contiguous_regions(grid, color):
        visited = set()
        regions = []

        def dfs(row, col, current_region):
            if (
                row < 0
                or row >= grid.shape[0]
                or col < 0
                or col >= grid.shape[1]
                or grid[row, col] != color
                or (row, col) in visited
            ):
                return
            visited.add((row, col))
            current_region.add((row, col))
            dfs(row + 1, col, current_region)
            dfs(row - 1, col, current_region)
            dfs(row, col + 1, current_region)
            dfs(row, col - 1, current_region)

        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if grid[row, col] == color and (row, col) not in visited:
                    current_region = set()
                    dfs(row, col, current_region)
                    regions.append(current_region)
        return regions
    
    def region_border(grid, region):
        rows, cols = zip(*region)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        # Check for red borders around the bounding box of the region
        top = all(grid[min_row-1,c] == 2 if min_row > 0 else False for c in range(min_col, max_col + 1) )
        bottom = all(grid[max_row + 1,c] == 2 if max_row < grid.shape[0] -1 else False for c in range(min_col, max_col+1))
        left = all(grid[r,min_col-1] == 2 if min_col > 0 else False for r in range(min_row, max_row+1))
        right = all(grid[r, max_col + 1] == 2 if max_col < grid.shape[1] - 1 else False for r in range(min_row, max_row+1))

        return top, bottom, left, right

    input_dims = input_grid.shape
    output_dims = output_grid.shape
    white_regions = get_contiguous_regions(input_grid, 0)
    white_region_data = []
    for region in white_regions:
        border = region_border(input_grid, region)
        white_region_data.append({
            "size": len(region),
            "border": border
            })
    
    errors = np.sum(output_grid != result_grid)


    return {
        "input_dims": input_dims,
        "output_dims": output_dims,
        "white_regions": white_region_data,
        "errors":errors
    }

# Example data (replace with your actual data)
example_data = [
  (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 2, 2, 2, 5, 5, 5], [5, 5, 5, 2, 0, 2, 5, 5, 5], [5, 5, 5, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 2, 2, 2, 5, 5, 5], [5, 5, 5, 2, 3, 2, 5, 5, 5], [5, 5, 5, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 2, 2, 2, 5, 5, 5], [5, 5, 5, 2, 3, 2, 5, 5, 5], [5, 5, 5, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]])
),
  (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 0, 0, 0, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 0, 0, 0, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
),
  (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 2, 0, 0, 0, 0, 0, 0, 2, 5, 5, 5], [5, 5, 5, 5, 2, 0, 0, 0, 0, 0, 0, 2, 5, 5, 5], [5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 2, 3, 3, 3, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 2, 3, 3, 3, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]),
np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 2, 3, 3, 3, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 2, 3, 3, 3, 3, 3, 3, 2, 5, 5, 5], [5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
)
]

results = [analyze_example(inp, out, res) for inp, out, res in example_data]

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Dims: {res['input_dims']}")
    print(f"  Output Dims: {res['output_dims']}")
    print(f"  White Regions:")
    for j, region in enumerate(res['white_regions']):
        print(f"  Region: {j + 1}")
        print(f"      Size: {region['size']}")
        print(f"      Border (T,B,L,R): {region['border']}")
    print(f"Errors: {res['errors']}")
    print("-" * 20)