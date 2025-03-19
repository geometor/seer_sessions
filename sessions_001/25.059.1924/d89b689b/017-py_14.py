import numpy as np

def transform_and_compare(input_grid, expected_output_grid):
    predicted_output_grid = transform(input_grid)
    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(expected_output_grid)
    print("Predicted Output Grid:")
    print(predicted_output_grid)

    objects = find_objects(input_grid)
    print("Objects found:", objects)
    
    # Find the largest azure object
    azure_objects = [obj for obj in objects if obj['color'] == 8]
    if azure_objects:
      largest_azure = max(azure_objects, key=lambda x: len(x['coords']))
      print("Largest azure object: ", largest_azure)
    else:
      print("Largest azure object: None")

    # Filter out single pixel azure, keep other single pixels,
    filtered_objects = [obj for obj in objects if obj['color'] != 8 or len(obj['coords']) == 1]
    print("filtered objects: ", filtered_objects)
    
    # sort the single pixels by color
    sorted_single_pixels = sorted([obj for obj in filtered_objects if len(obj['coords'])==1], key=lambda x: x['color'])
    print("sorted single pixels: ", sorted_single_pixels)

    diff = predicted_output_grid - expected_output_grid
    print("Difference (Predicted - Expected):")
    print(diff)
    print("-" * 20)
    return diff

# Assuming 'train' is a list of dictionaries, each with 'input' and 'output'
for i, example in enumerate(train):
  print("example: ", i)
  transform_and_compare(np.array(example['input']), np.array(example['output']))