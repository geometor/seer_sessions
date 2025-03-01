import numpy as np

def get_objects(grid):
    """
    Identify contiguous blocks of the same color as objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj:
                    objects.append(obj)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((5, 5), dtype=int)
    # find objects in the input grid
    objects = get_objects(input_grid)
    
    # selection pattern.
    # define offsets for row and col and block sizes

    row_offsets = [0, 1, 2, 3, 4]
    col_offsets = [2, 3, 4, 4, 5]

    # extract the selected pixels
    row_idx = 0
    for i in range(len(row_offsets)):
          col_idx = 0
          for j in range(len(col_offsets)):
            output_grid[row_idx, col_idx] = input_grid[row_offsets[i], col_offsets[j]]
            col_idx +=1
          row_idx += 1

    return output_grid

def test_transform(task_examples):
    for example_num, example in enumerate(task_examples):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        
        print(f"Example {example_num + 1}:")
        print("Input Grid:")
        print(input_grid)
        print("Objects in Input Grid:")
        objects = get_objects(input_grid)
        print(objects)
        
        transformed_grid = transform(input_grid)
        print("Transformed Grid:")
        print(transformed_grid)
        print("Expected Output:")
        print(expected_output)

        print("Comparison (Transformed == Expected):")
        comparison = np.array_equal(transformed_grid, expected_output)
        print(comparison)
        print("-" * 20)

task_examples = [
    {'input': [[0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0]], 'output': [[3, 0, 0, 0, 0], [3, 0, 0, 0, 0], [3, 0, 0, 0, 0], [3, 0, 0, 0, 0], [3, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2]], 'output': [[0, 0, 0, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 2]]},
    {'input': [[0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0]], 'output': [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]]}
]

test_transform(task_examples)