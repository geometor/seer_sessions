def analyze_example(input_grid, output_grid, predicted_output):
    """Analyzes a single example and gathers relevant metrics."""

    # Find objects
    red_coords = find_objects(input_grid, 2)
    grey_coords = find_objects(input_grid, 5)

    # bounding box of red
    red_bbox = bounding_box(red_coords) if red_coords else None

    # grey shape in output
    grey_out_coords = find_objects(output_grid, 5)
    grey_out_bbox = bounding_box(grey_out_coords) if grey_out_coords else None

    # predicted output
    grey_predicted_coords = find_objects(predicted_output, 5)
    grey_predicted_bbox = bounding_box(grey_predicted_coords) if grey_predicted_coords else None    

    print("Red BBox:", red_bbox)
    print("Grey Output BBox:", grey_out_bbox)
    print("Grey Predicted BBox:", grey_predicted_bbox)
    print("Input Grid")
    print(input_grid)
    print("Expected Output Grid")
    print(output_grid)    
    print("Predicted Output Grid")
    print(predicted_output)

# loop through first three examples to keep token use down
for i in range(3):
  predicted_output = transform(task["train"][i]["input"])  
  analyze_example(np.array(task["train"][i]["input"]), np.array(task["train"][i]["output"]), predicted_output)
