import numpy as np

def analyze_grid(grid, grid_name):
    objects = find_objects(grid)
    
    analysis = {
        "grid_name": grid_name,
        "dimensions": grid.shape,
        "num_objects": len(objects),
        "object_details": [],        
    }
        
    for obj in objects:
      pixels = np.array(obj["pixels"])
      min_row, min_col = np.min(pixels, axis=0)
      max_row, max_col = np.max(pixels, axis=0)
      width = max_col - min_col + 1
      height = max_row - min_row + 1
      obj_info = {
        'color' : obj['color'],
        'width' : width,
        'height': height,
        'area' : len(obj['pixels'])
      }
      analysis["object_details"].append(obj_info)
    return analysis

def print_analysis(input_grid, output_grid, example_num):
  input_analysis = analyze_grid(input_grid, f"input_{example_num}")
  output_analysis = analyze_grid(output_grid, f"output_{example_num}")

  print(f"Example {example_num}:")
  print(f"  Input: {input_analysis}")
  print(f"  Output: {output_analysis}")
  print("---")
  

# Example usage with the training data (replace with actual grids)
task_data = task["train"]

for i, example in enumerate(task_data):
  input_grid = np.array(example['input'])
  output_grid = np.array(example['output'])
  print_analysis(input_grid, output_grid, i)