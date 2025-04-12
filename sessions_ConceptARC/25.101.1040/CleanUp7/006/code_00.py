import numpy as np
from typing import List, Tuple, Set, Dict

# Re-use data from previous analysis
train_data = [
    { # Train 1 (S=3)
        "input": np.array([
            [0,0,0,0,0,0,0,0,0], [3,3,3,0,0,0,0,0,0], [0,3,0,0,3,3,3,0,0],
            [0,3,0,0,8,8,8,0,0], [0,0,0,0,8,8,8,0,0], [0,0,0,0,8,8,8,3,3],
            [0,0,0,0,0,0,0,3,0], [0,3,3,3,0,0,0,3,0], [0,0,3,0,0,0,0,0,0]
        ]),
        "output": np.array([
            [0,0,0,0,0,0,0,0,0], [3,3,3,0,0,0,0,0,0], [0,3,0,0,3,3,3,0,0],
            [0,3,0,0,0,3,0,0,0], [0,0,0,0,0,3,0,0,0], [0,0,0,0,0,0,3,3,3],
            [0,0,0,0,0,0,0,3,0], [0,3,3,3,0,0,0,3,0], [0,0,3,0,0,0,0,0,0]
        ])
    },
    { # Train 2 (S=4)
        "input": np.array([
            [4,0,4,0,0,0,0,0,0], [4,4,4,0,4,0,4,0,0], [4,0,4,0,4,4,4,0,0],
            [0,0,0,0,8,8,8,8,8], [0,0,0,0,8,8,8,8,8], [4,0,4,0,8,8,8,8,8],
            [4,4,4,0,0,0,4,4,4], [4,0,4,0,0,0,4,0,4], [0,0,0,0,0,0,0,0,0]
        ]),
        "output": np.array([
            [4,0,4,0,0,0,0,0,0], [4,4,4,0,4,0,4,0,0], [4,0,4,0,4,4,4,0,0],
            [0,0,0,0,4,0,4,0,0], [0,0,0,0,0,0,0,0,0], [4,0,4,0,0,0,4,0,4],
            [4,4,4,0,0,0,4,4,4], [4,0,4,0,0,0,4,0,4], [0,0,0,0,0,0,0,0,0]
        ])
    },
    { # Train 3 (S=6)
        "input": np.array([
            [0,6,0,0,0,0,0,6,0], [6,6,6,0,0,0,6,6,6], [0,6,0,0,6,0,8,8,8],
            [0,0,0,6,6,6,8,8,8], [0,0,0,0,6,0,8,8,8], [0,0,0,0,0,6,8,8,8],
            [0,0,6,0,6,6,8,8,8], [0,6,6,6,0,6,8,8,8], [0,0,6,0,0,0,0,0,0]
        ]),
        "output": np.array([
            [0,6,0,0,0,0,0,6,0], [6,6,6,0,0,0,6,6,6], [0,6,0,0,6,0,0,6,0],
            [0,0,0,6,6,6,0,0,0], [0,0,0,0,6,0,0,0,0], [0,0,0,0,0,6,0,0,0],
            [0,0,6,0,6,6,6,0,0], [0,6,6,6,0,6,0,0,0], [0,0,6,0,0,0,0,0,0]
        ])
    }
]

def find_source_color(grid: np.ndarray) -> int:
    unique_colors = np.unique(grid)
    for color in unique_colors:
        int_color = int(color)
        if int_color != 0 and int_color != 8:
            return int_color
    return -1 # Should not happen

def get_neighborhood(grid: np.ndarray, r: int, c: int, pad_value: int = 0) -> tuple[tuple[int, ...], ...]:
    rows, cols = grid.shape
    # Use standard int type
    neighborhood = np.full((3, 3), pad_value, dtype=int) 
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighborhood[dr + 1, dc + 1] = grid[nr, nc]
    # Convert final numpy array to tuple of tuples of standard ints
    return tuple(tuple(int(x) for x in row) for row in neighborhood)

# Dictionary to store success patterns keyed by source color
success_patterns_by_source: Dict[int, Set[Tuple[Tuple[int, ...], ...]]] = {}

print("--- Extracting Raw Success Patterns per Source Color ---")
for i, example in enumerate(train_data):
    input_grid = example["input"]
    output_grid = example["output"]
    rows, cols = input_grid.shape
    source_color = find_source_color(input_grid)

    if source_color == -1:
        print(f"Warning: No source color found for example {i+1}")
        continue

    # Initialize the set for this source color if it doesn't exist
    if source_color not in success_patterns_by_source:
        success_patterns_by_source[source_color] = set()
        print(f"\n--- Initializing patterns for Source={source_color} ---")

    count = 0
    for r in range(rows):
        for c in range(cols):
            # Check if input is 8 and output is S
            if input_grid[r, c] == 8 and output_grid[r, c] == source_color:
                # Get the raw neighborhood tuple from the input grid
                neighborhood_tuple = get_neighborhood(input_grid, r, c, pad_value=0)
                
                # Add the raw pattern to the set for this specific source color
                if neighborhood_tuple not in success_patterns_by_source[source_color]:
                     print(f"  Adding pattern for S={source_color} at ({r},{c}): {neighborhood_tuple}")
                success_patterns_by_source[source_color].add(neighborhood_tuple)
                count += 1
    print(f"  Found {count} instances for S={source_color}.")


print("\n--- Final Unique Raw Success Patterns by Source Color ---")
for S, patterns in success_patterns_by_source.items():
    print(f"\nSource Color = {S} (Count = {len(patterns)}):")
    # Sort patterns for consistent display
    sorted_patterns = sorted(list(patterns))
    for p in sorted_patterns:
        print(f"  {p}")
