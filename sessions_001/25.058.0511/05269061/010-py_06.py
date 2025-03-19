import numpy as np

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input/output pair from the ARC task.
    Identifies objects, their properties, and attempts to discern transformation rules.
    """

    def find_objects(grid):
        """
        Finds contiguous regions of the same color and labels them as objects.
        Returns a dictionary of objects, keyed by object ID, with properties.
        """
        objects = {}
        visited = np.zeros_like(grid, dtype=bool)
        object_id_counter = 1

        def dfs(row, col, color, object_id):
            """Depth-first search to find contiguous regions."""
            if (
                row < 0
                or row >= grid.shape[0]
                or col < 0
                or col >= grid.shape[1]
                or visited[row, col]
                or grid[row, col] != color
            ):
                return
            visited[row, col] = True
            objects[object_id]["pixels"].append((row, col))
            dfs(row + 1, col, color, object_id)
            dfs(row - 1, col, color, object_id)
            dfs(row, col + 1, color, object_id)
            dfs(row, col - 1, color, object_id)

        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if not visited[row, col]:
                    color = grid[row, col]
                    objects[object_id_counter] = {
                        "color": color,
                        "pixels": [],
                    }
                    dfs(row, col, color, object_id_counter)
                    object_id_counter += 1
        return objects

    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    # Calculate object properties (size, bounding box, etc.)
    for obj_id, obj_data in input_objects.items():
        pixels = obj_data["pixels"]
        rows, cols = zip(*pixels)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        obj_data["size"] = len(pixels)
        obj_data["bounding_box"] = (min_row, min_col, max_row, max_col)
        obj_data["shape"] = (max_row - min_row + 1, max_col - min_col + 1)  # height, width

    for obj_id, obj_data in output_objects.items():
        pixels = obj_data["pixels"]
        rows, cols = zip(*pixels)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        obj_data["size"] = len(pixels)
        obj_data["bounding_box"] = (min_row, min_col, max_row, max_col)
        obj_data["shape"] = (max_row - min_row + 1, max_col - min_col + 1)


    # Generate Report (for now, just print - later, structure as YAML)
    print("--- Input Objects ---")
    for obj_id, obj_data in input_objects.items():
        print(f"Object ID: {obj_id}")
        for key, value in obj_data.items():
            print(f"  {key}: {value}")

    print("--- Output Objects ---")
    for obj_id, obj_data in output_objects.items():
        print(f"  Object ID: {obj_id}")
        for key, value in obj_data.items():
            print(f"  {key}: {value}")
    
    print("--- Preliminary Analysis ---")
    # Very Basic Comparison (needs improvement)
    # Check for color changes:
    input_colors = {obj['color'] for obj in input_objects.values()}
    output_colors = {obj['color'] for obj in output_objects.values()}
    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")
    if input_colors == output_colors:
      print("The set of colors are the same between the input and output.")
    
    #check the number of objects
    print(f"Number of input objects: {len(input_objects)}")
    print(f"Number of output objects: {len(output_objects)}")
    if len(input_objects) == len(output_objects):
        print("The number of objects are the same.")

# Example Usage (replace with actual data)
# Example usage with the first training example (replace with actual grid data):
example1_input = np.array([
    [4, 0, 4, 0, 4],
    [0, 4, 0, 4, 0],
    [4, 0, 1, 0, 4],
    [0, 4, 0, 4, 0],
    [4, 0, 4, 0, 4]
])
example1_output = np.array([
    [4, 0, 4, 0, 4],
    [0, 4, 0, 4, 0],
    [4, 0, 2, 0, 4],
    [0, 4, 0, 4, 0],
    [4, 0, 4, 0, 4]
])
analyze_example(example1_input, example1_output)

example2_input = np.array([
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]])
example2_output = np.array([
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
analyze_example(example2_input, example2_output)

example3_input = np.array([
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]])
example3_output = np.array([
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
analyze_example(example3_input, example3_output)