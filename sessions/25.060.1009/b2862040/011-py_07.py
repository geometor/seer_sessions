import numpy as np

# Assuming 'task' and 'transform' are defined elsewhere as described above.

def describe_objects(objects):
    desc = []
    for obj in objects:
        desc.append(f"color={obj['color']}, size={len(obj['coords'])}")
    return ", ".join(desc)

for i, example in enumerate(task["train"]):
    input_grid = example["input"]
    expected_output_grid = example["output"]
    predicted_output_grid = transform(input_grid)

    input_objects = find_objects(input_grid)
    expected_output_objects = find_objects(expected_output_grid)
    predicted_output_objects = find_objects(predicted_output_grid)
    
    try:
      predicted_output_grid = transform(input_grid)
      same = np.array_equal(predicted_output_grid,expected_output_grid)
    except Exception as e:
      same = False

    print(f"Example {i+1}:")
    print(f"  Input objects: {describe_objects(input_objects)}")
    print(f"  Expected output objects: {describe_objects(expected_output_objects)}")
    print(f"  Predicted output objects: {describe_objects(predicted_output_objects)}")
    print(f"  Prediction is correct: {same}")

    # Determine changed object and color in expected output
    changed_object_expected = None
    new_color_expected = None
    for obj_in in input_objects:
        found = False
        for obj_out in expected_output_objects:
            if len(obj_in['coords']) == len(obj_out['coords']):
                coords_match = True
                for coord_in, coord_out in zip(obj_in['coords'], obj_out['coords']):
                  if coord_in != coord_out:
                    coords_match = False
                    break
                if coords_match:
                  found = True
                  if obj_in['color'] != obj_out['color']:
                      changed_object_expected = obj_in
                      new_color_expected = obj_out['color']
                  break
        if found == False:
          changed_object_expected = obj_in
          
          # find the color of the matching coordinates in obj_out
          for obj_out in expected_output_objects:
            if len(obj_out['coords']) > 0:
              first_coord = obj_out['coords'][0]
              for inner_obj in expected_output_objects:
                for inner_coord in inner_obj['coords']:
                  if first_coord == inner_coord:
                    new_color_expected = inner_obj['color']

    print(f"  Expected changed object: {describe_objects([changed_object_expected]) if changed_object_expected else 'None'}")
    print(f"  Expected new color: {new_color_expected if new_color_expected is not None else 'None'}")
          

    # Determine changed object and color in predicted output
    changed_object_predicted = None
    new_color_predicted = None
    
    if len(input_objects) > 0:
        changed_object_predicted = input_objects[0]  # this is what the code currently does
        if len(predicted_output_objects) > 0:
            new_color_predicted = predicted_output_objects[0]['color'] if predicted_output_objects[0]['color'] != changed_object_predicted['color'] else None

    print(f"  Predicted changed object: {describe_objects([changed_object_predicted]) if changed_object_predicted else 'None'}")
    print(f"  Predicted new color: {new_color_predicted if new_color_predicted is not None else 'None'}")

    print("-" * 20)