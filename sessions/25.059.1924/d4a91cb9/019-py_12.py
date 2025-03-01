import numpy as np

def find_pixel(grid, color):
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])
    return None

def calculate_distance(pixel1, pixel2):
    if pixel1 is None or pixel2 is None:
      return float('inf')
    return abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1])
    
def analyze_example(input_grid, output_grid):
  
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    azure_pixel_in = find_pixel(input_grid, 8)
    red_pixel_in = find_pixel(input_grid, 2)
    azure_pixel_out = find_pixel(output_grid, 8)
    red_pixel_out = find_pixel(output_grid, 2)

    dist = calculate_distance(azure_pixel_in, red_pixel_in)

    yellow_pixels_in = np.where(input_grid == 4)
    yellow_pixels_out = np.where(output_grid == 4)
    yellow_added = len(yellow_pixels_out[0]) - len(yellow_pixels_in[0])

    print(f"  Azure Pixel (Input): {azure_pixel_in}")
    print(f"  Red Pixel (Input): {red_pixel_in}")
    print(f"  Distance between: {dist}")
    print(f"  Azure Pixel (Output): {azure_pixel_out}")
    print(f"  Red Pixel (Output): {red_pixel_out}")
    print(f"  Yellow Pixels Added: {yellow_added}")

    diff = output_grid - input_grid
    changes = np.where(diff != 0)
    if (len(changes[0])) > 0:
      print(f"  Changes: {list(zip(changes[0], changes[1]))} values: {[output_grid[r,c] for r,c in zip(changes[0], changes[1])]}")
    else:
      print("No Changes")

    # Adjacent positions for azure.
    azure_adj = []
    if azure_pixel_in is not None:
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        r, c = azure_pixel_in[0] + dr, azure_pixel_in[1] + dc
        if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
            azure_adj.append((r,c))
      print(f" Azure Adj: {azure_adj}")

    # Adjacent positions for red.
    red_adj = []
    if red_pixel_in is not None:
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        r, c = red_pixel_in[0] + dr, red_pixel_in[1] + dc
        if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
            red_adj.append((r,c))
      print(f" Red Adj: {red_adj}")

    #check prediction
    predicted_output = transform(input_grid)
    if np.array_equal(predicted_output, output_grid):
      print("  Prediction: Correct")
    else:
      print("  Prediction: Incorrect")


examples = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 0, 0, 0, 0, 0, 0, 2, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 8, 4, 4, 4, 4, 4, 4, 2, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 8, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 2, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 8, 0, 0, 0],
         [0, 0, 0, 0, 4, 0, 0, 0],
         [0, 0, 0, 0, 2, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]
    ),
     (
       [[8, 3, 2]],
       [[8, 3, 2]]
     )

]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    print("-" * 30)