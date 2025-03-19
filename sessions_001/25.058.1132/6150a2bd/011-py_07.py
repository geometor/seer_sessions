# Hypothetical Code Execution - I would do something like this for EACH example
# and summarize the results in a structured way.

import numpy as np

def analyze_example(input_grid, output_grid, predicted_output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output_grid = np.array(predicted_output_grid)
    
    correct = np.array_equal(output_grid, predicted_output_grid)

    print(f"Input Grid:\n{input_grid}\n")
    print(f"Output Grid:\n{output_grid}\n")
    print(f"Predicted Grid (Vertical Flip):\n{predicted_output_grid}\n")
    print(f"Correct Prediction? {correct}\n")

    # Object detection (basic - assumes contiguous blocks)
    def find_objects(grid):
        objects = []
        visited = set()

        def dfs(r, c, color, obj):
            if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
                return
            visited.add((r, c))
            obj.append((r, c))
            dfs(r + 1, c, color, obj)
            dfs(r - 1, c, color, obj)
            dfs(r, c + 1, color, obj)
            dfs(r, c - 1, color, obj)

        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if (r, c) not in visited:
                    obj = []
                    dfs(r, c, grid[r, c], obj)
                    if obj:
                        objects.append(obj)
        return objects
    
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    print(f"Input Objects: {input_objects}")
    print(f"Output Objects: {output_objects}")
    print("-" * 20)

# Hypothetical example data (replace with actual examples)
examples = [
    {
        "input": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "output": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "predicted": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    },
      {
        "input": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        "output": [[0, 1, 0], [0, 0, 0], [0, 0, 0]],
          "predicted":  [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    },
     {
        "input": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "output": [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
         "predicted": [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
    },

]


for ex in examples:
    analyze_example(ex["input"], ex["output"], ex["predicted"])
