
## example 1
*input:*
```
8 6
6 8
```
*expected output:*
```
8 6 6 8
6 8 8 6
6 8 8 6
8 6 6 8
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 2 is out of bounds for axis 0 with size 2

## example 2
*input:*
```
7 7 8
7 7 8
8 8 8
```
*expected output:*
```
7 7 8 8 7 7
7 7 8 8 7 7
8 8 8 8 8 8
8 8 8 8 8 8
7 7 8 8 7 7
7 7 8 8 7 7
```
*transformed output:*
```
7 7 7 8
7 7 7 8
7 7 7 8
8 8 8 8
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
6 9 9
6 4 4
6 4 4
```
*expected output:*
```
6 9 9 6 6 6
6 4 4 4 4 9
6 4 4 4 4 9
9 4 4 4 4 6
9 4 4 4 4 6
6 6 6 9 9 6
```
*transformed output:*
```
6 9 9 9
6 4 4 4
6 4 4 4
6 4 4 4
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
