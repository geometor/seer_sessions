import numpy as np
from collections import Counter
import json

def analyze_grid(grid_list):
    if not grid_list:
        return {"error": "Empty grid"}
    try:
        grid = np.array(grid_list)
    except ValueError: # Handle potentially ragged lists if they occur
         return {"error": "Invalid grid format"}

    if grid.size == 0:
        return {"dims": (0, 0), "unique_colors": [], "background": None, "non_background_colors": []}

    dims = grid.shape
    counts = Counter(grid.flatten())
    # Convert numpy types to standard python types for JSON serialization
    unique_colors = sorted([int(c) for c in counts.keys()])

    if not counts:
        background = 0 # Default assumption
    else:
        # Find most common, ensuring it's a standard int
        background = int(counts.most_common(1)[0][0])

    non_background_colors = sorted([c for c in unique_colors if c != background])

    return {
        "dims": dims,
        "unique_colors": unique_colors,
        "background": background,
        "non_background_colors": non_background_colors
    }

# Example 1 Data
input1 = [
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 3, 3, 8, 3, 3, 8, 8, 4, 8, 8, 8],
    [8, 8, 3, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8],
    [8, 8, 3, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 3, 8, 3, 8, 8, 8, 8, 8, 4, 8],
    [8, 8, 3, 3, 8, 3, 3, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 1, 1, 1, 8, 8, 8, 6, 8, 8, 8, 8],
    [8, 8, 1, 1, 1, 8, 8, 8, 6, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
]
output1 = [
    [3, 3, 4, 3, 3],
    [3, 1, 1, 1, 3],
    [3, 1, 1, 1, 3],
    [4, 3, 6, 3, 4],
    [3, 3, 6, 3, 3]
]

# Example 2 Data
input2 = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 6, 3, 3, 3, 3, 3, 3, 8, 8, 8, 3, 3],
    [3, 6, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3],
    [3, 3, 3, 1, 1, 1, 3, 3, 3, 8, 3, 5, 3],
    [3, 3, 1, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3],
    [3, 3, 1, 1, 3, 1, 1, 3, 5, 3, 3, 3, 3],
    [3, 3, 3, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 2, 3, 2, 3, 3, 3, 3, 4, 3, 3],
    [3, 3, 2, 2, 3, 2, 2, 3, 3, 3, 4, 3, 3],
    [3, 3, 2, 3, 3, 3, 2, 3, 3, 4, 4, 4, 3],
    [3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3],
    [3, 6, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3],
    [3, 6, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3]
]
output2 = [
    [5, 1, 1, 1, 5],
    [1, 8, 8, 8, 1],
    [1, 1, 8, 1, 1],
    [6, 1, 8, 1, 6],
    [6, 2, 4, 2, 6],
    [2, 2, 4, 2, 2],
    [2, 4, 4, 4, 2],
    [5, 2, 2, 2, 5]
]

analysis = {
    "example1_input": analyze_grid(input1),
    "example1_output": analyze_grid(output1),
    "example2_input": analyze_grid(input2),
    "example2_output": analyze_grid(output2),
}

# Convert the analysis dict to JSON and print
print(json.dumps(analysis, indent=2))