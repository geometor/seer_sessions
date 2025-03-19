import numpy as np

def code_execution(input_grid, output_grid, transform_fn):
    """
    Executes the transformation function, compares the result with the expected output,
    and provides detailed information about objects and transformations.

    Args:
        input_grid: The input grid.
        output_grid: The expected output grid.
        transform_fn: The transformation function to be tested.

    Returns:
        A dictionary containing analysis results, including:
          'success': Whether the transformation was successful,
          'input_objects': Information about objects in the input,
          'output_objects': Information about objects in the output,
          'transformed_grid': The result of applying the transform function,
          'comparison': A comparison grid highlighting differences, or None if successful.
    """

    # 1.  Identify Objects:  Identify all distinct objects in the input grid. An object is a group of connected pixels of the same color.
    # 2.  Compare Objects: For each input object find the matching object in the output object by location.
    # 3.  Determine Color Change**:  If the color changed to blue, then change that object in the input to blue.
    # 4.  Output: Return the modified grid.

    def find_objects(grid):
        """
        Identifies distinct objects in the grid.
        An object is a group of connected pixels of the same color.
        """
        objects = {}
        visited = np.zeros_like(grid, dtype=bool)

        def dfs(row, col, color, object_id):
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
            objects[object_id].append((row, col))
            dfs(row + 1, col, color, object_id)
            dfs(row - 1, col, color, object_id)
            dfs(row, col + 1, color, object_id)
            dfs(row, col - 1, color, object_id)

        object_count = 0
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if not visited[row, col]:
                    color = grid[row, col]
                    object_id = f"object_{object_count}"
                    objects[object_id] = []
                    dfs(row, col, color, object_id)
                    object_count += 1
        return objects

    def get_object_center(object_pixels):
        """Calculates the center (centroid) of an object."""
        rows = [p[0] for p in object_pixels]
        cols = [p[1] for p in object_pixels]
        center_row = int(np.mean(rows))
        center_col = int(np.mean(cols))
        return center_row, center_col

    def get_object_color(grid, object_pixels):
        first_pixel = object_pixels[0]
        return grid[first_pixel]
      
    transformed_grid = transform_fn(input_grid, output_grid)
    success = np.array_equal(transformed_grid, output_grid)

    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    
    input_objects_data = {}
    for obj_id, pixels in input_objects.items():
        input_objects_data[obj_id] = {
            "pixels": pixels,
            "center": get_object_center(pixels),
            "color": get_object_color(input_grid, pixels)
        }
    output_objects_data = {}
    for obj_id, pixels in output_objects.items():
      output_objects_data[obj_id] = {
            "pixels": pixels,
            "center": get_object_center(pixels),
            "color": get_object_color(output_grid, pixels)
        }

    comparison = None
    if not success:
        comparison = np.where(
            transformed_grid != output_grid,
            np.abs(transformed_grid - output_grid) * 9,  # Highlight differences
            0,
        )

    return {
        "success": success,
        "input_objects": input_objects_data,
        "output_objects": output_objects_data,
        "transformed_grid": transformed_grid,
        "comparison": comparison,
    }
def get_first_row_colors(grid):
    """Returns a set of unique colors present in the first row of the grid."""
    return set(grid[0])

# Example Usage (assuming train_in, train_out, and transform are defined)
task_data = []
for i in range(len(train_in)):

    analysis = code_execution(
        np.array(train_in[i]), np.array(train_out[i]), transform
    )
    task_data.append(analysis)

    print(f"--- Example {i+1} ---")
    print(f"Success: {analysis['success']}")
    print(f"First row colors: {get_first_row_colors(np.array(train_in[i]))}")
    if not analysis['success']:
      print(f"Differences:\n{analysis['comparison']}")
