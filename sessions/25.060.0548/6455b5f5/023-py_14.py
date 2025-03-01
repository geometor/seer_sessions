import numpy as np

def analyze_grid(grid):
    """Provides basic information about a grid."""
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    height = grid.shape[0]
    width = grid.shape[1]
    print(f"  Dimensions: {height}x{width}")
    print(f"  Color Counts: {color_counts}")
    red_regions = find_connected_components(grid, 2)
    white_regions = find_connected_components(grid,0)
    enclosed = find_enclosed_regions(grid, 2)
    print(f"  Red regions: {len(red_regions)}")
    print(f"  Number of white regions: {len(white_regions)}")
    print(f"   Number of enclosed regions {len(enclosed)}")
    if enclosed:
      sizes = [len(region) for region in enclosed]
      print(f"  Enclosed region sizes: {sizes}")

def compare_grids(grid1, grid2):
    """Compares two grids and prints differences."""
    if grid1.shape != grid2.shape:
        print("  Grids have different shapes!")
        return
    diff = grid1 != grid2
    if np.any(diff):
        print("  Grids differ:")
        diff_indices = np.where(diff)
        for row, col in zip(*diff_indices):
            print(f"    Pixel at ({row}, {col}): Grid1={grid1[row, col]}, Grid2={grid2[row, col]}")
    else:
        print("  Grids are identical.")
        
# Example Usage (assuming 'train' is your list of training examples)
for i, example in enumerate(train):
  print(f"Example Input {i+1}")
  analyze_grid(example['input'])

  print(f"Example Output {i+1}")
  analyze_grid(example['output'])
    
  predicted_output = transform(example['input'])
  print(f"Prediction {i+1}:")
  compare_grids(example['output'], predicted_output)
  print("---")