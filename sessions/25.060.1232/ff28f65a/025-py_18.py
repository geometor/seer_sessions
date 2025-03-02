import numpy as np

def check_output(predicted_output, expected_output):
    if predicted_output.shape != expected_output.shape:
        print(f"  Shape mismatch: Predicted {predicted_output.shape}, Expected {expected_output.shape}")
        return False
    else:
        comparison = predicted_output == expected_output
        if not np.all(comparison):
          print("  Differences:")
          print(comparison)
          return False
        else:
          print("  Outputs match")
          return True

def describe_grid(grid):
  return f"{grid.shape} {grid.tolist()}"