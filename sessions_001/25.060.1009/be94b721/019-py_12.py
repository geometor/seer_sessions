import numpy as np
from typing import List, Tuple, Dict, Any

# Provided examples - put into the expected format
train_examples:List[Dict[str,Any]] = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0], [0, 8, 8, 8], [0, 8, 8, 8], [0, 8, 8, 8], [0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0], [0, 8, 8, 0], [0, 8, 8, 0], [0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [0, 0, 0, 0]]
    },
]

def analyze_example(example: Dict[str, Any]) -> Dict[str, Any]:
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])

    input_azure_objects = []
    output_azure_objects = []

    # very simple object finding - just contiguous blocks
    def find_objects(grid, color):
        objects = []
        visited = np.zeros_like(grid, dtype=bool)
        rows, cols = grid.shape

        def dfs(r, c, obj):
            if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
                return
            visited[r, c] = True
            obj.append((r, c))
            dfs(r + 1, c, obj)
            dfs(r - 1, c, obj)
            dfs(r, c + 1, obj)
            dfs(r, c - 1, obj)

        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color and not visited[r, c]:
                    obj = []
                    dfs(r, c, obj)
                    if(obj):
                        objects.append(obj)
        return objects

    input_azure_objects = find_objects(input_grid, 8)
    output_azure_objects = find_objects(output_grid, 8)
    
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    return {
        'input_grid_shape': (input_height, input_width),
        'output_grid_shape': (output_height, output_width),
        'num_input_azure_objects': len(input_azure_objects),
        'num_output_azure_objects': len(output_azure_objects),
        'input_azure_object_shapes': [str(np.array(obj).shape) for obj in input_azure_objects],
        'output_azure_object_shapes': [str(np.array(obj).shape) for obj in output_azure_objects],
        'output_contains_all_input_azure': output_grid.size > 0 and np.all(input_grid[input_grid == 8] == output_grid[input_grid == 8]),
        'input_min_row': int(np.min(np.where(input_grid == 8)[0])) if len(np.where(input_grid == 8)[0])>0 else -1,
        'input_max_row': int(np.max(np.where(input_grid == 8)[0])) if len(np.where(input_grid == 8)[0])>0 else -1,
        'input_min_col': int(np.min(np.where(input_grid == 8)[1])) if len(np.where(input_grid == 8)[1])>0 else -1,
        'input_max_col': int(np.max(np.where(input_grid == 8)[1])) if len(np.where(input_grid == 8)[1])>0 else -1,
    }

results = [analyze_example(ex) for ex in train_examples]

for i,r in enumerate(results):
    print(f"Example {i+1}:")
    for k,v in r.items():
        print(f"  {k}: {v}")