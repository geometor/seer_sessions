# CODE_EXECUTION (Hypothetical)
import numpy as np

# Assume these are loaded from the actual data
expected_output_example_2 = np.array([[...], [...], ...])  # Expected output grid
actual_output_example_2 = transform(input_example_2) #result of calling transform

comparison_result = (expected_output_example_2 == actual_output_example_2)
match_percentage = np.sum(comparison_result) / comparison_result.size * 100
print(f"Match Percentage: {match_percentage:.2f}%")

mismatched_indices = np.where(comparison_result == False)
print(f"Mismatched Pixel Indices: {mismatched_indices}")
print(f"Expected Values at Mismatches: {expected_output_example_2[mismatched_indices]}")
print(f"Actual Values at Mismatches: {actual_output_example_2[mismatched_indices]}")
