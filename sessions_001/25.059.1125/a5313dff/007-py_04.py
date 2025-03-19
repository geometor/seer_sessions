import numpy as np

# Helper function to print grids (from ARC solver)
def format_grid(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

# Example Data (assuming this is available in a variable `task`)
task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 2, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 2, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 2, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 0, 2, 2, 0, 0, 2, 0],
                [0, 2, 0, 0, 2, 2, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 2, 0],
                [0, 2, 1, 1, 2, 2, 1, 1, 2, 0],
                [0, 2, 1, 1, 2, 2, 1, 1, 2, 0],
                [0, 2, 1, 1, 1, 1, 1, 1, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
           ]
        },
                {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 2, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 2, 0, 0, 0],
                [0, 0, 2, 1, 1, 1, 2, 0, 0, 0],
                [0, 0, 2, 2, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
        },
                {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 0, 0, 0, 0, 2, 0],
                [0, 2, 0, 2, 0, 0, 2, 0],
                [0, 2, 0, 0, 0, 0, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 2, 2, 2, 2, 2, 0],
                [0, 2, 1, 1, 1, 1, 2, 0],
                [0, 2, 1, 2, 1, 1, 2, 0],
                [0, 2, 1, 1, 1, 1, 2, 0],
                [0, 2, 2, 2, 2, 2, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
           ]
        },
    ]
}

def describe_red_regions(grid):
    """
    Identifies and describes contiguous red regions in the grid.
    Returns a list of dictionaries, each describing a region.
    """
    red_regions = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, region_pixels):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 2:
            return
        visited[r, c] = True
        region_pixels.append((r, c))
        # Explore adjacent cells (up, down, left, right)
        dfs(r + 1, c, region_pixels)
        dfs(r - 1, c, region_pixels)
        dfs(r, c + 1, region_pixels)
        dfs(r, c - 1, region_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2 and not visited[r, c]:
                region_pixels = []
                dfs(r, c, region_pixels)
                if region_pixels:
                    # basic description
                    min_r = min(p[0] for p in region_pixels)
                    max_r = max(p[0] for p in region_pixels)
                    min_c = min(p[1] for p in region_pixels)
                    max_c = max(p[1] for p in region_pixels)
                    region_description = {
                        'pixels': region_pixels,
                        'min_row': min_r,
                        'max_row': max_r,
                        'min_col': min_c,
                        'max_col': max_c,
                        'height': max_r-min_r + 1,
                        'width' : max_c - min_c + 1,
                    }

                    red_regions.append(region_description)
    return red_regions

for i, example in enumerate(task["train"]):
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    predicted = transform(input_grid)
    red_regions = describe_red_regions(input_grid)
    print(f"Example {i+1}:")
    print("Input:")
    print(format_grid(input_grid))
    print("Expected Output:")
    print(format_grid(output_grid))
    print("Predicted Output")
    print(format_grid(predicted))
    print("Red Regions:", red_regions)
    print("Correct Prediction:", np.array_equal(output_grid,predicted))
    print("-" * 20)