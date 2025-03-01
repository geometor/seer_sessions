import numpy as np

def get_grid_info(grid):
    return {
        'shape': grid.shape,
        'unique_colors': np.unique(grid).tolist()
    }

train_examples = [
    (np.array([[5, 0, 5], [0, 5, 0], [5, 0, 5]]), np.array([[3, 4, 3], [4, 3, 4], [3, 4, 3]])),
    (np.array([[5, 0, 5], [0, 5, 0], [5, 0, 5]]), np.array([[3, 4, 3], [4, 3, 4], [3, 4, 3]])),
    (np.array([[5, 5, 5], [0, 0, 0], [5, 5, 5]]), np.array([[3, 3, 3], [4, 4, 4], [3, 3, 3]])),
    (np.array([[0, 0, 0], [0, 5, 0], [0, 0, 0]]), np.array([[4, 4, 4], [4, 3, 4], [4, 4, 4]])),
     (np.array([[1, 0, 1], [0, 5, 0], [1, 0, 1]]), np.array([[1, 4, 1], [4, 3, 4], [1, 4, 1]])),
]

results = []
for i, (input_grid, output_grid) in enumerate(train_examples):
    input_info = get_grid_info(input_grid)
    output_info = get_grid_info(output_grid)
    results.append({
        'example': i,
        'input': input_info,
        'output': output_info
    })

print(results)
