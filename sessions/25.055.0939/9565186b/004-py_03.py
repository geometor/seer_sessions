import numpy as np

# Provided task data (replace with actual data loading if necessary)
task_data = {
    'train': [
        ([[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 8], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]], [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]),
        ([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [8, 1, 1, 1], [1, 1, 1, 1]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [8, 0, 0, 0], [0, 0, 0, 0]]),
        ([[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 8, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        ([[1, 1, 1, 8, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1]], [[0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
    ]
}

def analyze_grid(grid, name):
    """Analyzes a single grid and returns a dictionary of color counts."""
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"Analysis of {name}:")
    print(f"  Color Counts: {color_counts}")
    blue_count = color_counts.get(1, 0)
    azure_count = color_counts.get(8, 0)
    red_count = color_counts.get(2,0)
    print(f" blue:{blue_count}, azure:{azure_count}, red:{red_count}")
    return

print("---Example Analysis---")
for i, (input_grid, output_grid) in enumerate(task_data['train']):
    print(f"Example Pair {i+1}:")
    analyze_grid(np.array(input_grid), f"Input Grid {i+1}")
    analyze_grid(np.array(output_grid), f"Output Grid {i+1}")