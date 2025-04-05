## Perception of Task Elements

The task involves transforming a sequence of integers provided as a space-separated string into another sequence of the same length, also represented as a space-separated string. The core operation appears to be related to the order of the elements within the sequence. The numerical values themselves (0, 1, 2) are preserved, but their positions are rearranged. The output sequence consistently displays the integers in ascending order.

## Documented Facts


```yaml
Task: SortSequence
Input:
  Type: string
  Format: Space-separated integers
  Elements: Integers (e.g., 0, 1, 2)
  Properties:
    - Unordered sequence
    - Fixed length (e.g., 12 elements in examples)
Output:
  Type: string
  Format: Space-separated integers
  Elements: The same set of integers as the input
  Properties:
    - Ordered sequence (ascending)
    - Same length as the input
Transformation:
  Action: Sorting
  Object: The sequence of integers derived from the input string
  Rule: Arrange the integers in non-decreasing (ascending) numerical order.
Relationship:
  - The output sequence contains exactly the same integers as the input sequence.
  - The count of each unique integer is preserved between input and output.
  - The output sequence is the sorted version of the input sequence.
```


## Natural Language Program

1.  Parse the input string into a list of integers.
2.  Sort the list of integers in non-decreasing (ascending) numerical order.
3.  Format the sorted list of integers back into a space-separated string.
4.  Return the formatted string as the output.