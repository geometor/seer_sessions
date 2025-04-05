import re

def transform(input_str: str) -> str:
  """
  Transforms a sequence of space-separated integers based on the following rule:
  1. Identify all non-zero integers and their positions (indices).
  2. For every sequence of zeros located strictly *between* two consecutive non-zero integers,
     replace those zeros with the value of the non-zero integer immediately to their right.
  3. Zeros appearing before the first non-zero integer remain zero.
  4. Zeros appearing after the last non-zero integer remain zero.
  5. Non-zero integers retain their original values and positions.
  """

  # Parse the input string into a list of integers
  numbers = [int(x) for x in input_str.split()]
  
  # Create a copy of the list to modify, preserving the original for checks
  output_numbers = list(numbers)

  # Find the indices of all non-zero elements in the original list
  non_zero_indices = [i for i, num in enumerate(numbers) if num != 0]

  # Check if there are at least two non-zero numbers to form a segment between them
  if len(non_zero_indices) >= 2:
      # Iterate through pairs of consecutive non-zero indices
      for i in range(len(non_zero_indices) - 1):
          idx_left = non_zero_indices[i]
          idx_right = non_zero_indices[i+1]
          
          # Get the value of the right boundary non-zero number
          fill_value = numbers[idx_right] 

          # Iterate through the indices strictly between the left and right non-zero indices
          for k in range(idx_left + 1, idx_right):
              # If the element at index k in the *original* list is zero,
              # update the corresponding element in the output list with the fill_value
              if numbers[k] == 0:
                  output_numbers[k] = fill_value

  # Convert the modified list of numbers back into a space-separated string
  output_str = " ".join(map(str, output_numbers))
  
  return output_str