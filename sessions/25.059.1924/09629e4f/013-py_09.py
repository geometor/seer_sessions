import numpy as np
from collections import Counter, deque

def get_connected_component(grid, start_row, start_col, color):
    """Finds a connected component of a given color using Breadth-First Search (BFS)."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque([(start_row, start_col)])
    component = []

    while queue:
        row, col = queue.popleft()
        if (0 <= row < rows and 0 <= col < cols and
                grid[row, col] == color and not visited[row, col]):
            visited[row, col] = True
            component.append((row, col))
            # Add orthogonal neighbors
            queue.append((row + 1, col))
            queue.append((row - 1, col))
            queue.append((row, col + 1))
            queue.append((row, col - 1))
    return component

def analyze_grid(grid):
    """Analyzes a grid and returns properties."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = Counter(grid.flatten())
    connected_components = {}
    for color in unique_colors:
        if color != 5:  # Skip gray for connected components
            connected_components[color] = []
            visited = np.zeros((rows, cols), dtype=bool)
            for i in range(rows):
                for j in range(cols):
                    if grid[i, j] == color and not visited[i, j]:
                        component = get_connected_component(grid, i, j, color)
                        connected_components[color].append(component)
                        for r, c in component:
                            visited[r, c] = True
    return {
        "dimensions": (rows, cols),
        "unique_colors": unique_colors.tolist(),
        "color_counts": dict(color_counts),
        "connected_components": connected_components,
    }

def compare_grids(predicted, expected):
    mismatched = np.where(predicted != expected)
    return list(zip(mismatched[0], mismatched[1]))

task = {
    "train": [
        {
            "input": [
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            ],
            "output": [
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            ]
        },
        {
            "input": [
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 2, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            ],
            "output": [
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            ]
        },
        {
            "input": [
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            ],
            "output": [
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5]
            ]
        }
    ]
}

for i, example in enumerate(task["train"]):
    input_grid = np.array(example["input"])
    expected_output = np.array(example["output"])
    predicted_output = transform(input_grid)  # Use the provided transform function

    input_analysis = analyze_grid(input_grid)
    output_analysis = analyze_grid(expected_output)
    mismatches = compare_grids(predicted_output, expected_output)

    print(f"Example {i+1}:")
    print("  Input Analysis:", input_analysis)
    print("  Output Analysis:", output_analysis)
    print("Mismatched Pixels", mismatches)
    print("-" * 40)