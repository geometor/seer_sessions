import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    metrics = {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "predicted_shape": predicted_output.shape,
        "red_changes": [],
        "blue_changes": [],
        "other_changes": [],
        "correct": np.array_equal(output_grid, predicted_output)
    }
    
    for color in range(10):  # Check all colors
      input_coords = np.array(np.where(input_grid == color)).T.tolist()
      output_coords = np.array(np.where(output_grid == color)).T.tolist()
      predicted_coords = np.array(np.where(predicted_output == color)).T.tolist()

      if color == 2:
          changes = metrics["red_changes"]
      elif color == 1:
          changes = metrics["blue_changes"]
      else:
        changes = metrics["other_changes"]
          

      # added
      for coord in input_coords:
          if coord not in output_coords:
              changes.append({"type": "removed", "location": coord, 'color': color})

      # removed
      for coord in output_coords:
          if coord not in input_coords:
              changes.append({"type": "added", "location": coord, 'color': color})
              
      # predicted added
      for coord in input_coords:
          if coord not in predicted_coords:
              changes.append({"type": "removed_predicted", "location": coord, 'color': color})

      # predicted removed
      for coord in predicted_coords:
          if coord not in input_coords:
              changes.append({"type": "added_predicted", "location": coord, 'color': color})

    return metrics

def show_examples(task):
  # mock out agent context to allow local execution
  class MockAgent:
    def __init__(self):
      self.scratchpad = {}
  agent = MockAgent()

  from পাইয়া.tasks import get_task
  task = get_task(task)

  # Previous Code:
  previous_code = """
  import numpy as np

  def find_pixels_by_color(grid, color):
      #Finds the coordinates of all pixels of a specific color.
      return np.array(np.where(grid == color)).T

  def transform(input_grid):
      input_grid = np.array(input_grid)  # Ensure input is a NumPy array.
      
      # Find coordinates of red and blue pixels.
      red_pixels = find_pixels_by_color(input_grid, 2)
      blue_pixels = find_pixels_by_color(input_grid, 1)

      # Determine the rows to keep (exclude gray row).
      gray_row_index = -1
      for i, row in enumerate(input_grid):
          if np.all(row == 5):
              gray_row_index = i
              break
              
      rows_to_keep = [i for i in range(input_grid.shape[0]) if i != gray_row_index]
      
      # create new output grid without the gray row
      output_grid = input_grid[rows_to_keep]

      # copy red pixel x coordinates to the first row of the output grid.
      if len(red_pixels) > 0:
        for coord in red_pixels:
            output_grid[0, coord[1]] = 2
      
      # Find the bottom-right red pixel in the *input* grid and change last one to blue (1) in *output*.
      red_pixels_in_last_row = []
      
      if gray_row_index == -1:
          last_row_input_index = input_grid.shape[0] - 1
      else:
          last_row_input_index = input_grid.shape[0] - 1

      
      for x,y in red_pixels:
          if x == last_row_input_index:
            red_pixels_in_last_row.append([x,y])    
      
      if len(red_pixels_in_last_row) > 0:
          last_red_pixel = max(red_pixels_in_last_row, key=lambda item: item[1])
          # change last red pixel to blue in last row
          output_grid[-1, last_red_pixel[1]] = 1

      return output_grid.tolist()
  """
  exec(previous_code, globals())

  
  all_metrics = []
  for example in task['train']:
      input_grid = example['input']
      output_grid = example['output']
      predicted_output = transform(input_grid)
      metrics = analyze_example(input_grid, output_grid, predicted_output)
      all_metrics.append(metrics)
      
  for i, metrics in enumerate(all_metrics):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {metrics['input_shape']}")
    print(f"  Output Shape: {metrics['output_shape']}")
    print(f"  Predicted Shape: {metrics['predicted_shape']}")
    print(f"  Correct: {metrics['correct']}")    
    print(f"  Red Changes: {metrics['red_changes']}")
    print(f"  Blue Changes: {metrics['blue_changes']}")
    print(f"  Other Changes: {metrics['other_changes']}")

# show_examples('6f8cd79b') # original
show_examples('29c11459')
