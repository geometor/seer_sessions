def get_object_extents(grid, color):
    """
    returns a dictionary that describes a bounding box around each object in the grid
    """
    objects = get_objects(grid, color)  # Reuse existing get_objects function
    extents = {}
    for i, obj in enumerate(objects):
        rows, cols = zip(*obj)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        extents[i] = {
            'min_row': min_row,
            'max_row': max_row,
            'min_col': min_col,
            'max_col': max_col,
            'height': max_row - min_row + 1,
            'width': max_col - min_col + 1,
            'pixels': len(obj)
        }
    return extents

def analyze_example(example):

    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    transformed_grid = transform(input_grid)

    print("Input:")
    print(input_grid)
    print("Expected Output:")
    print(output_grid)
    print("Transformed Output:")
    print(transformed_grid)

    input_red_extents = get_object_extents(input_grid, 2)
    output_red_extents = get_object_extents(output_grid, 2)  # Check for red in output
    output_maroon_extents = get_object_extents(output_grid, 9) #check for maroon in output
    transformed_red_extents = get_object_extents(transformed_grid, 2)
    transformed_maroon_extents = get_object_extents(transformed_grid, 9)


    print("\nInput Red Object Extents:", input_red_extents)
    print("Expected Output Red Object Extents:", output_red_extents)
    print("Expected Output Maroon Object Extents:", output_maroon_extents)
    print("Transformed Red Object Extents:", transformed_red_extents)
    print("Transformed Maroon Object Extents:", transformed_maroon_extents)
    print("Matches Expected Output:", np.array_equal(output_grid, transformed_grid))
    print("-" * 20)


for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    analyze_example(example)