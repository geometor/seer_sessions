import numpy as np

def compare_grids(grid1, grid2):
    if not isinstance(grid1, np.ndarray): grid1 = np.array(grid1)
    if not isinstance(grid2, np.ndarray): grid2 = np.array(grid2)

    if grid1.shape != grid2.shape:
        return {"error": "Mismatched shapes"}
    diff = grid1 != grid2
    count = int(np.sum(diff)) # Use int() for JSON compatibility
    locations = np.argwhere(diff).tolist()
    error_details = []
    for r, c in locations:
        error_details.append({
            "location": (r, c),
            "expected": int(grid2[r, c]), # Use int() for JSON compatibility
            "transformed": int(grid1[r, c]) # Use int() for JSON compatibility
        })
    return {
        "pixels_off": count,
        "error_locations": locations,
        "error_details": error_details
    }

# Example 1 Data (code_02 output)
transformed_1 = np.array([
    [8, 7, 7, 8, 3, 8, 7],
    [3, 8, 8, 3, 3, 3, 8],
    [3, 3, 3, 3, 7, 3, 3],
    [3, 7, 3, 7, 3, 3, 8],
    [3, 3, 3, 3, 3, 8, 7],
    [3, 3, 7, 3, 8, 7, 7],
    [3, 7, 3, 8, 7, 7, 7]
])

expected_1 = np.array([
    [8, 7, 7, 8, 7, 8, 7],
    [7, 8, 8, 3, 3, 3, 8],
    [7, 7, 7, 3, 7, 3, 7],
    [3, 3, 3, 3, 3, 3, 8],
    [7, 7, 7, 3, 7, 8, 7],
    [3, 3, 3, 3, 8, 7, 7],
    [7, 7, 7, 8, 7, 7, 7]
])

# Example 2 Data (code_02 output)
transformed_2 = np.array([
    [7, 8, 3, 8, 7],
    [8, 3, 3, 3, 8],
    [3, 3, 7, 3, 3],
    [3, 3, 3, 3, 8],
    [3, 3, 7, 8, 7]
])

expected_2 = np.array([
    [7, 8, 7, 8, 7],
    [8, 3, 3, 3, 8],
    [7, 3, 7, 3, 7],
    [3, 3, 3, 3, 8],
    [7, 3, 7, 8, 7]
])

results_1 = compare_grids(transformed_1, expected_1)
results_2 = compare_grids(transformed_2, expected_2)

print(f"Example 1 Metrics (code_02):\n{results_1}\n")
print(f"Example 2 Metrics (code_02):\n{results_2}\n")