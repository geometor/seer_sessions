import numpy as np

def get_objects(grid):
    """
    Identifies objects in a grid.

    Args:
    grid: A 2D numpy array representing the grid.

    Returns:
    A dictionary where keys are colors and values are lists of object
    descriptions.  Each object description is a tuple: ((row, col), area).
    """

    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, cells):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return
        visited.add((row, col))
        cells.append((row, col))
        dfs(row + 1, col, color, cells)
        dfs(row - 1, col, color, cells)
        dfs(row, col + 1, color, cells)
        dfs(row, col - 1, color, cells)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                color = grid[row, col]
                cells = []
                dfs(row, col, color, cells)
                if color not in objects:
                    objects[color] = []
                objects[color].append((cells, len(cells)))  # Store cells and area
    return objects

def analyze_task(task):
    print("Analyzing task examples...")
    for example_index, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        input_objects = get_objects(input_grid)
        output_objects = get_objects(output_grid)
        
        print(f"Example {example_index + 1}:")
        print("Input Objects:")
        for color, obj_list in input_objects.items():
            for obj_data, area in obj_list:
                print(f"  Color: {color}, Area: {area}, Cells: {obj_data}")

        print("Output Objects:")
        for color, obj_list in output_objects.items():
           for obj_data, area in obj_list:
                print(f"  Color: {color}, Area: {area}, Cells: {obj_data}")
        print("-" * 20)