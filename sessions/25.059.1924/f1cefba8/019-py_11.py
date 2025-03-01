import numpy as np

def find_object(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    min_y, min_x = coords.min(axis=0)
    max_y, max_x = coords.max(axis=0)
    return (min_y, min_x), (max_y, max_x)

def get_object_details(grid, color):
    object_coords = find_object(grid, color)
    if object_coords:
      min_y, min_x = object_coords[0]
      max_y, max_x = object_coords[1]
      height = max_y - min_y + 1
      width = max_x - min_x + 1
      return f"color={color}, top_left=({min_y},{min_x}), height={height}, width={width}"
    else:
      return None
def assess_example(input_grid, output_grid, predicted_output):
    print("Input:")
    print(input_grid)
    print("Expected Output:")
    print(output_grid)
    print("Predicted Output:")
    print(predicted_output)


    colors = np.unique(np.concatenate((input_grid.flatten(), output_grid.flatten(), predicted_output.flatten())))
    print("Objects in Input:")
    for color in colors:
        details = get_object_details(input_grid, color)
        if details:
          print(details)

    print("Objects in Expected Output:")
    for color in colors:
        details = get_object_details(output_grid, color)
        if details:
            print(details)
    print("Objects in Predicted Output:")
    for color in colors:
        details = get_object_details(predicted_output,color)
        if details:
          print(details)
    print("-" * 20)

# Example usage (assuming train_in, train_out, and predicted_outputs are available)
task = '6f8cd79b'
train_in, train_out, test_in, test_out = load_task(task)
for i in range(len(train_in)):
    predicted_output = transform(train_in[i].copy())
    assess_example(train_in[i], train_out[i], predicted_output)

