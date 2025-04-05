
## train_1

**input:**
```
2 1 0 2 1 0 0 0 0 1 1 0
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 2 2
```


## train_2

**input:**
```
0 1 0 1 0 2 0 1 2 2 0 1
```


**output:**
```
0 0 0 0 0 1 1 1 1 2 2 2
```


## train_3

**input:**
```
0 1 0 1 2 2 1 1 2 0 0 2
```


**output:**
```
0 0 0 0 1 1 1 1 2 2 2 2
```


## train_4

**input:**
```
0 1 1 0 0 0 1 0 0 0 2 1
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 1 2
```


## train_5

**input:**
```
0 2 0 2 1 0 1 1 0 0 1 1
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 2 2
```


## train_6

**input:**
```
0 2 1 2 0 2 0 1 0 2 2 0
```


**output:**
```
0 0 0 0 0 1 1 2 2 2 2 2
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 1 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 1 1
```

*   **Perception of the elements:**
    *   The input is a string containing a sequence of space-separated single digits (0, 1, or 2).
    *   The output is also a string containing a sequence of space-separated single digits (0, 1, or 2).
    *   Both input and output sequences consistently have the same length (12 digits in the examples).
    *   Comparing the digits in the input and output sequences reveals that the output sequence contains the same digits as the input sequence, but arranged in non-decreasing (ascending) order. The count of each digit (0, 1, 2) remains the same between the input and its corresponding output.

*   **YAML Facts:**
    
```yaml
    Task: Sort a sequence of digits.
    Input:
      Type: String
      Format: Space-separated digits
      Content: Sequence of digits (0, 1, 2)
      Length: Fixed (e.g., 12 in examples)
    Output:
      Type: String
      Format: Space-separated digits
      Content: Sequence of digits (0, 1, 2)
      Length: Same as input
    Transformation:
      Action: Sort
      Object: The sequence of digits from the input.
      Property: Order
      Rule: Arrange the digits in non-decreasing (ascending) numerical order.
      Constraint: Maintain the original count of each distinct digit.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a sequence of individual digit numbers.
    2.  Sort this sequence of digits in non-decreasing (ascending) numerical order.
    3.  Format the sorted sequence back into a string with digits separated by spaces.
    4.  Return the formatted string as the output.
