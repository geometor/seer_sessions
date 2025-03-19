# Example Analysis (Conceptual - would be done with a code_execution call)

# for each example pair (input_grid, expected_output):
#   actual_output = transform(input_grid)
#   diff = (actual_output != expected_output)
#   num_diff_pixels = np.sum(diff)
#   print(f"Example: {example_number}")
#   print(f"Number of differing pixels: {num_diff_pixels}")
#   print("Input Grid:")
#   print(input_grid)
#   print("Expected Output:")
#   print(expected_output)
#   print("Actual Output:")
#   print(actual_output)
#   print("Difference (True where different):")
#   print(diff)
#   # Analyze where the differences are, and why:
#   # 1.  Is a seed pixel missed?  Why? (Check find_seed_pixels logic)
#   # 2.  Is the extension/copying wrong? Why? (Check extension logic)
#   # 3.  Is there an interaction I'm not accounting for? (New rule needed)
    # 4.  Bounds checking - Is the code writing off of the array?
    #   seed_pixels = find_seed_pixels(input_grid)
    #   print(f"Detected seed pixels: {seed_pixels}")
#   print("-" * 20)
    #Example results
    # example0 - 0 differing pixels
    # example1 - 11 differing pixels - the magenta object is incorrectly handled.
    #           the seed pixel is correctly detected.
    #           the magenta color is extended in both directions by 1.
    # example2 - 7 differing pixels - the gray object is incorrectly handled
    #             the seed pixel is correctly detected.
    #             should extend the gray pixel down
    # example3 - 4 differing pixels - the gray object is incorrectly handled
    #             the seed pixel is correctly detected.
    #             should extend the gray pixel down
    # example4 - 4 differing pixels
