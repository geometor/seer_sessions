import numpy as np

# Example 2 Data
expected_2 = [[2,0,0,0,2,4,4,4,2,0],[4,2,0,2,0,2,4,2,0,2],[4,4,2,0,0,0,2,0,0,0]]
transformed_2 = [[2,0,0,0,2,4,4,4,2,4],[4,2,0,2,0,2,4,2,0,2],[4,4,2,0,0,0,2,0,0,0]]

# Comparison Function (assuming it's available/defined elsewhere)
def compare_grids(grid1, grid2):
    if not isinstance(grid1, list) or not isinstance(grid2, list): return {"match": False, "reason": "Not list"}
    if not grid1 or not grid2: return {"match": False, "reason": "Empty grid"}
    if not isinstance(grid1[0], list) or not isinstance(grid2[0], list): return {"match": False, "reason": "Not 2D list"}

    arr1 = np.array(grid1, dtype=int)
    arr2 = np.array(grid2, dtype=int)

    if arr1.shape != arr2.shape:
        return {"match": False, "reason": "Shape mismatch", "shape1": arr1.shape, "shape2": arr2.shape}

    diff = arr1 != arr2
    mismatch_count = int(np.sum(diff))
    mismatch_coords = np.argwhere(diff).tolist()

    return {
        "match": mismatch_count == 0,
        "mismatch_count": mismatch_count,
        "mismatch_coords": mismatch_coords, # list of [row, col]
        "shape": arr1.shape,
    }

results = {
    "example_2_comparison": compare_grids(expected_2, transformed_2),
}

print(results)