import numpy as np

def count_colors(grid):
    """Counts the occurrences of each color (0-9) in a grid."""
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    # Ensure all colors 0-9 are present in the dictionary
    for i in range(10):
        if i not in color_counts:
            color_counts[i] = 0
    return color_counts

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair and returns color counts."""
    input_counts = count_colors(input_grid)
    output_counts = count_colors(output_grid)
    return input_counts, output_counts

# Example usage (replace with actual grids from the task):
# input_grid = np.array([[0, 1, 2], [3, 4, 5]])
# output_grid = np.array([[1, 2, 5]])

# task_data = json.loads(TASK)  # Load the actual ARC task JSON here
# examples = task_data['train']

examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1]]
    },
        {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
        "output": [[1]]
    },
    {
        "input": [[0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1]]
    },

]
results = []
for example in examples:
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    input_counts, output_counts = analyze_example(input_grid, output_grid)
    results.append({"input": input_counts, "output": output_counts})

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Counts:  {res['input']}")
    print(f"  Output Counts: {res['output']}")
    print("-" * 20)