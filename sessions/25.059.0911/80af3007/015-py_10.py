# Conceptual Code Execution (for demonstration -  would be interactive)
import numpy as np

def describe_objects(grid, color):
    objects = find_objects(grid, color)
    descriptions = []
    for i, obj in enumerate(objects):
        min_r = min(r for r, c in obj)
        max_r = max(r for r, c in obj)
        min_c = min(r for r, c in obj)
        max_c = max(r for r, c in obj)
        width = max_c - min_c + 1
        height = max_r - min_r + 1
        descriptions.append({
            "object_id": i,
            "bounding_box": (min_r, min_c, max_r, max_c),
            "width": width,
            "height": height,
            "num_pixels": len(obj),
            "shape_description": "Placeholder - to be filled based on relative pixel positions" # added for future steps
        })
    return descriptions

# Example usage (conceptual - needs actual input grids)
input_grids = [...]  # Replace with actual input grids from the examples
for i, input_grid in enumerate(input_grids):
   descriptions = describe_objects(np.array(input_grid), 5)
   print(f"Example {i+1} Object Descriptions:")
   for desc in descriptions:
      print(desc)