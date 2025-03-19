def get_dimensions(grid):
    return len(grid), len(grid[0]) if grid else 0

def analyze_example(example):
    input_grid = example['input']
    output_grid = example['output']
    input_dims = get_dimensions(input_grid)
    output_dims = get_dimensions(output_grid)
    return {
        'input_dimensions': input_dims,
        'output_dimensions': output_dims,
    }

task_data = { 'train': [
    {'input': [[5, 5, 5], [5, 5, 5]], 'output': [[5, 5], [5, 5], [5, 5]]},
    {'input': [[0, 8, 8, 8, 8, 8, 8, 0], [0, 8, 8, 0, 0, 0, 0, 0], [0, 8, 8, 0, 0, 7, 7, 7], [0, 8, 8, 0, 0, 7, 7, 7], [0, 8, 8, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 0]], 'output': [[0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 8], [8, 0, 0, 7, 0, 8], [8, 0, 0, 7, 0, 8], [0, 0, 7, 7, 0, 0]]},
    {'input': [[1, 0, 3, 0, 5], [9, 2, 7, 4, 8], [0, 1, 0, 0, 6]], 'output': [[0, 9, 1], [1, 2, 0], [0, 7, 3], [0, 4, 0], [6, 8, 5]]},
    {'input': [[5, 0, 7, 7, 7, 7, 7, 0, 5], [0, 0, 7, 7, 7, 7, 7, 0, 0], [5, 0, 7, 7, 7, 7, 7, 0, 5]], 'output': [[5, 0, 5], [0, 0, 0], [7, 7, 7], [7, 7, 7], [7, 7, 7], [7, 7, 7], [7, 7, 7], [0, 0, 0], [5, 0, 5]]}
]}

results = [analyze_example(example) for example in task_data['train']]
print(results)
