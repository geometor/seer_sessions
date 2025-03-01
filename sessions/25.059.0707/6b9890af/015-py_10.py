def code_execution(input_grid, output_grid):
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    print(f"Input objects: {len(input_objects)}")
    for i, obj in enumerate(input_objects):
        color = input_grid[obj[0][0], obj[0][1]]
        min_row, max_row, min_col, max_col = get_object_bounds(obj)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        print(f"  Object {i+1}: Color={color}, TopLeft=({min_row},{min_col}), Size=({height},{width})")
        if height == width:
             print(f"  Object {i + 1}: is_square")

    print(f"Output objects: {len(output_objects)}")
    for i, obj in enumerate(output_objects):
        color = output_grid[obj[0][0], obj[0][1]]
        min_row, max_row, min_col, max_col = get_object_bounds(obj)
        height = max_row - min_row + 1
        width = max_col - min_col + 1
        print(f"  Object {i+1}: Color={color}, TopLeft=({min_row},{min_col}), Size=({height},{width})")
        if height == width:
             print(f"  Object {i + 1}: is_square")

# Example usage, need adapt with the task data structure
task_data = [
    {"input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     "output": np.array([[2, 2, 2, 2, 2],
                         [2, 0, 0, 0, 2],
                         [2, 0, 1, 0, 2],
                         [2, 0, 0, 0, 2],
                         [2, 2, 2, 2, 2]])},
    {"input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]]),
      "output": np.array([[2, 2, 2, 2, 2, 2, 2],
                          [2, 0, 0, 0, 0, 0, 2],
                          [2, 0, 0, 0, 0, 0, 2],
                          [2, 0, 1, 1, 0, 0, 2],
                          [2, 0, 1, 1, 0, 0, 2],
                          [2, 0, 0, 0, 0, 0, 2],
                          [2, 2, 2, 2, 2, 2, 2]])},
    {"input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]]),
     "output": np.array([[2, 2, 2, 2, 2, 2, 2, 2, 2],
                         [2, 0, 0, 0, 0, 0, 0, 0, 2],
                         [2, 0, 0, 0, 0, 0, 0, 0, 2],
                         [2, 0, 0, 0, 0, 0, 0, 0, 2],
                         [2, 0, 0, 0, 1, 1, 1, 0, 2],
                         [2, 0, 0, 0, 1, 1, 1, 0, 2],
                         [2, 0, 0, 0, 1, 1, 1, 0, 2],
                         [2, 0, 0, 0, 0, 0, 0, 0, 2],
                         [2, 2, 2, 2, 2, 2, 2, 2, 2]])
     },
     {"input": np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 8, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 8, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 8, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     "output": np.array([[2, 2, 2, 2, 2],
                         [2, 8, 0, 0, 2],
                         [2, 0, 1, 0, 2],
                         [2, 0, 0, 0, 2],
                         [2, 2, 2, 2, 2]])}
]


for i, ex in enumerate(task_data):
    print(f"Example {i+1}:")
    code_execution(ex["input"], ex["output"])

# Test input grid
test_input = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0]])

print("Test Input:")
code_execution(test_input, test_input)  # Pass test_input twice since there is no "output".