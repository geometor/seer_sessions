import numpy as np

# Previous find_objects function (provided in original prompt)
def find_objects(grid):
    """Finds and groups contiguous non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)
        dfs(r+1,c+1,color,obj) # diagonal
        dfs(r-1,c-1,color,obj) # diagonal
        dfs(r-1,c+1,color,obj) # diagonal
        dfs(r+1,c-1,color,obj) # diagonal

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append((grid[r,c], obj)) # (color, list of positions)
    return objects

# Example Grids (from the provided problem - manually transcribed)
example_grids = {
    "train_0_in": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 8, 2, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 1, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    "train_0_out": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 0, 0, 8, 8, 8, 0],
        [8, 2, 0, 0, 0, 8, 2, 0],
        [8, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0],
        [0, 1, 3, 0, 0, 0, 0, 0],
        [0, 1, 3, 0, 0, 0, 0, 0]
    ]),
    "train_1_in": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 8, 2, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 3, 0, 0, 0, 0, 0]
    ]),
    "train_1_out": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 0, 0, 0, 0, 0, 0],
        [8, 2, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 8, 8, 8, 0, 0],
        [0, 0, 1, 3, 8, 2, 0, 0, 0]
    ]),
    "train_2_in": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 8, 2, 0, 0, 0],
        [0, 2, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
      "train_2_out": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [8, 8, 8, 0, 0, 0, 0, 0, 0],
        [8, 2, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    "train_3_in": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 8, 8, 0, 0],
        [0, 0, 0, 0, 8, 2, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 1, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2]
    ]),
      "train_3_out": np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 8, 8, 0, 0, 2, 8, 8, 8],
        [8, 2, 0, 0, 0, 0, 8, 2],
        [8, 0, 0, 0, 0, 0, 8, 0],
        [0, 1, 3, 0, 0, 0, 0, 0],
        [0, 1, 3, 0, 0, 0, 0, 0]
    ])
}

def analyze_examples(grids):
    for key in grids:
        if key.endswith("_in"):
            output_key = key.replace("_in", "_out")
            if output_key in grids:
                print(f"Analyzing {key} and {output_key}:")
                input_objects = find_objects(grids[key])
                output_objects = find_objects(grids[output_key])
                print(f"  Input Objects: {input_objects}")
                print(f"  Output Objects: {output_objects}")
            else:
                print(f"  Could not find matching output for {key}")

analyze_examples(example_grids)
