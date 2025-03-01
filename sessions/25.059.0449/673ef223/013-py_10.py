import numpy as np

def code_execution(input_grid, output_grid, actual_grid):
    """
    Calculates and prints metrics about the transformation, focusing on discrepancies.
    """
    
    def find_object(grid, color):
        return np.argwhere(grid == color)
    
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    actual_grid = np.array(actual_grid)

    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(output_grid)
    print("Actual Output Grid:")
    print(actual_grid)
    
    colors = [2,8,4]
    color_names = {
      2: "red",
      8: "azure",
      4: "yellow"
    }
    
    for color in colors:
        input_coords = find_object(input_grid, color)
        output_coords = find_object(output_grid, color)
        actual_coords = find_object(actual_grid, color)
        
        print(f"\nMetrics for color {color_names[color]} ({color}):")
        
        if input_coords.size > 0:
            print(f"  Input coordinates: {input_coords}")
        else:
            print(f"  No {color_names[color]} in input.")
            
        if output_coords.size > 0:
            print(f"  Expected output coordinates: {output_coords}")
        else:
            print(f"  No {color_names[color]} in expected output.")
            
        if actual_coords.size > 0:
              print(f"  Actual output coordinates: {actual_coords}")
        else:
            print(f"  No {color_names[color]} in actual output.")
        

# Example usage with the provided data:
# make sure input_output_pairs_train is properly defined from notebook

# Example data structure (replace with actual data)
input_output_pairs_train = [
    ([[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 8, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 2], [5, 5, 5, 5, 8, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]], [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 8], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 2], [5, 5, 5, 5, 8, 8, 8, 8, 8], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    ([[5, 5, 5, 5, 5, 5, 5, 8, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 4, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 8, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]], [[5, 5, 5, 5, 5, 5, 5, 8, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 2], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 8, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    ([[5, 5, 5, 5, 5, 5, 2, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 8, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]], [[5, 5, 5, 5, 5, 5, 2, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 8], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
]

for input_grid, output_grid in input_output_pairs_train:
  actual_grid = transform(input_grid)
  code_execution(input_grid, output_grid, actual_grid)
  print("-" * 30)