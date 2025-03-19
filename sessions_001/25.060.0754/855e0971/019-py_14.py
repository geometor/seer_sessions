def code_execution(input_grid, output_grid):
    import numpy as np

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    def find_objects(grid):
        objects = []
        visited = np.zeros_like(grid, dtype=bool)

        def dfs(r, c, color, current_object):
            if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                    visited[r, c] or grid[r, c] != color):
                return
            visited[r, c] = True
            current_object.append((r, c))
            dfs(r + 1, c, color, current_object)
            dfs(r - 1, c, color, current_object)
            dfs(r, c + 1, color, current_object)
            dfs(r, c - 1, color, current_object)

        for r in range(grid.shape[0]):
            for c in range(grid.shape[1]):
                if not visited[r, c]:
                    current_object = []
                    dfs(r, c, grid[r, c], current_object)
                    objects.append(current_object)
        return objects
    
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    input_white_pixels = [len([(r, c) for r, c in obj if input_grid[r, c] == 0]) for obj in input_objects]
    output_white_pixels = [len([(r, c) for r, c in obj if output_grid[r, c] == 0]) for obj in output_objects]
    
    input_heights = [max(r for r, c in obj) - min(r for r, c in obj) + 1 for obj in input_objects]
    output_heights = [max(r for r, c in obj) - min(r for r, c in obj) + 1 for obj in output_objects]

    results = {
        "input_objects": len(input_objects),
        "output_objects": len(output_objects),
        "input_white_pixel_counts": input_white_pixels,
        "output_white_pixel_counts": output_white_pixels,
        "input_object_heights": input_heights,
        "output_object_heights": output_heights,
    }
    return results
    

task = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5]],
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0]],
            "output": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0]],
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0]],
            "output": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0]],
        },
                {
            "input": [[5, 5, 5, 5, 0, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 0, 5, 5]],
            "output": [[5, 5, 5, 5, 0, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 0, 5, 5],[5, 5, 5, 5, 0, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 0, 5, 5]],
        },

    ]
}

for i, example in enumerate(task["train"]):
    results = code_execution(example["input"], example["output"])
    print(f"Example {i}:")
    print(results)
