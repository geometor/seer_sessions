import numpy as np

def describe_objects(grid):
    objects = find_objects(grid)
    descriptions = []
    for obj_id, obj_data in objects.items():
        color = obj_data['color']
        coords = obj_data['coords']
        min_r, min_c = np.min(coords, axis=0)
        max_r, max_c = np.max(coords, axis=0)
        width = max_c - min_c + 1
        height = max_r - min_r + 1
        descriptions.append({
            'object_id': obj_id,
            'color': color,
            'min_row': min_r,
            'min_col': min_c,
            'width': width,
            'height': height,
            'count': len(coords)
        })
    return descriptions

def analyze_example(input_grid, output_grid):
  input_description = describe_objects(input_grid)
  output_description = describe_objects(output_grid)

  print("Input objects:")
  for obj in input_description:
    print(obj)
  print("\nOutput objects:")
  for obj in output_description:
    print(obj)

  magenta_input = [o for o in input_description if o['color'] == 6]
  yellow_input = [o for o in input_description if o['color'] == 4]

  if magenta_input and yellow_input:
      print(f"\nmagenta width: {magenta_input[0]['width']}, yellow width: {yellow_input[0]['width']}")

examples = [
    (np.array([[0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 4, 0],
               [0, 0, 0, 0, 4, 6],
               [0, 0, 0, 0, 0, 6],
               [0, 0, 0, 0, 0, 6]]),
     np.array([[6, 6, 6],
               [4, 0, 6],
               [4, 0, 6]])),

    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 4, 0, 0, 0, 0, 0],
               [0, 4, 6, 6, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[6, 6, 6],
               [4, 0, 6],
               [4, 0, 6]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0],
               [0, 0, 6, 6, 6, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[6, 6, 6],
               [4, 0, 6],
               [0, 0, 6]])),
     (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 6, 6, 6, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[6, 6, 6],
               [0, 0, 6],
               [0, 0, 6]]))

]
for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    print("------")
