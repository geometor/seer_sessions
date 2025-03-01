def analyze_azure_objects(grid):
    """
    Analyzes azure objects in the grid and returns a list of dictionaries,
    each containing information about an azure object.
    """
    rows, cols = grid.shape
    azure = 8
    azure_objects = []
    visited = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == azure and (r, c) not in visited:
                min_row, max_row, min_col, max_col = get_object_bounds(grid, r, c, azure)
                width = max_col - min_col + 1
                height = max_row - min_row + 1

                #count non-azure neighbors of all azure in shape
                non_azure_neighbors = 0
                azure_pixels_in_shape = []
                for row in range(min_row, max_row + 1):
                  for col in range(min_col, max_col + 1):
                      azure_pixels_in_shape.append( (row, col) )
                      for nr, nc in get_neighbors(grid, row, col):
                        if grid[nr,nc] != azure:
                            non_azure_neighbors+=1

                object_info = {
                    'start_row': min_row,
                    'start_col': min_col,
                    'width': width,
                    'height': height,
                    'non_azure_neighbors': non_azure_neighbors,
                    'azure_pixels': azure_pixels_in_shape
                }
                azure_objects.append(object_info)
                visited.update(azure_pixels_in_shape) #add all to visited

    return azure_objects

# Example usage (replace with actual input grids):
# task = Task("path/to/task.json")  # Assuming 'Task' class is available
# for i, pair in enumerate(task.train):
#    input_grid = np.array(pair['input'])
#    output_grid = np.array(pair['output']) #the correct answer
#    transformed_grid = transform(np.array(pair['input'])) #the current code's output
#
#    print(f"Example {i+1}:")
#    print("Azure Objects:", analyze_azure_objects(input_grid))
#    print("Transformed Grid Matches Expected:", np.array_equal(transformed_grid, output_grid))
#    print("-" * 20)