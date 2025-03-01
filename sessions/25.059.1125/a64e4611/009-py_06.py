import numpy as np

def get_bounding_box(obj):
    """
    Returns the bounding box (min_row, min_col, max_row, max_col) of an object.
    """
    min_row = min(pixel[0] for pixel in obj)
    max_row = max(pixel[0] for pixel in obj)
    min_col = min(pixel[1] for pixel in obj)
    max_col = max(pixel[1] for pixel in obj)
    return (min_row, min_col, max_row, max_col)

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output pair and returns relevant metrics.
    """
    blue_objects = get_objects(input_grid, 1)
    white_objects_input = get_objects(input_grid, 0)
    white_objects_output = get_objects(output_grid, 0)
    green_objects_output = get_objects(output_grid,3)

    blue_bounding_boxes = [get_bounding_box(obj) for obj in blue_objects]
    # find the white object in input that overlaps a green object in output
    white_to_green_input = []
    for w_obj in white_objects_input:
      w_bb = get_bounding_box(w_obj)
      for g_obj in green_objects_output:
        g_bb = get_bounding_box(g_obj)
        # check overlap
        if not (w_bb[2] < g_bb[0] or w_bb[0] > g_bb[2] or w_bb[3] < g_bb[1] or w_bb[1] > g_bb[3]):
          white_to_green_input.append(w_obj)
          break

    white_to_green_bounding_boxes = [get_bounding_box(obj) for obj in white_to_green_input]

    print("Blue Bounding Boxes:", blue_bounding_boxes)
    print("Transformed White Bounding Box(es) in Input:", white_to_green_bounding_boxes)
    #print("White Bounding Boxes (Output):", [get_bounding_box(obj) for obj in white_objects_output])

# this needs to be updated with the actual train pairs
for i in range(len(train)):
  print(f"--- Example {i+1} ---")
  analyze_example(train[i][0], train[i][1])
