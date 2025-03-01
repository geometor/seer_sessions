import numpy as np

def get_objects(grid):
    """Find distinct colored regions, excluding the most frequent color."""
    unique_colors = np.unique(grid)
    counts = [np.sum(grid == color) for color in unique_colors]
    most_frequent_color = unique_colors[np.argmax(counts)]
    
    objects = []
    for color in unique_colors:
        if color != most_frequent_color:
            objects.append(color)
    return objects, most_frequent_color

def transform(input_grid):
    # Find distinct objects and the most frequent (background) color
    objects, background_color = get_objects(input_grid)

    #insert background color as white
    objects.insert(1,0)

    # Create the output grid:  Duplicate Row
    output_grid = np.array([objects, objects])

    return output_grid

def analyze_example(input_grid, output_grid):
    input_dims = input_grid.shape
    output_dims = output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    correct = np.array_equal(transform(input_grid), output_grid)
    return {
        "input_dims": input_dims,
        "output_dims": output_dims,
        "input_colors": input_colors.tolist(),
        "output_colors": output_colors.tolist(),
        "correct": correct
    }

task_data = {
    "train": [
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 3, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            "output": [[3, 0, 2], [3, 0, 2]],
        },
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 3, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2, 1, 1, 1, 1, 1]],
            "output": [[3, 0, 2], [3, 0, 2]],
        },
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            "output": [[3, 0, 2], [3, 0, 2]],
        },
    ]
}

results = [analyze_example(np.array(ex["input"]), np.array(ex["output"])) for ex in task_data["train"]]
print(results)