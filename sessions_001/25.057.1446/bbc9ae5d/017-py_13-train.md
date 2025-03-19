
## example 1
*input:*
```
1 1 0 0 0 0
```
*expected output:*
```
1 1 0 0 0 0
1 1 1 0 0 0
1 1 1 1 0 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 0 is out of bounds for axis 0 with size 0

## example 2
*input:*
```
2 0 0 0 0 0 0 0
```
*expected output:*
```
2 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 2 0 0 0 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 0 is out of bounds for axis 0 with size 0

## example 3
*input:*
```
5 5 5 0 0 0 0 0 0 0
```
*expected output:*
```
5 5 5 0 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0
5 5 5 5 5 5 5 0 0 0
```
*transformed output:*
```
5 5 5 0 0 0 0 0 0 0
5 5 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 0 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 4
*input:*
```
8 8 8 8 0 0
```
*expected output:*
```
8 8 8 8 0 0
8 8 8 8 8 0
8 8 8 8 8 8
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 0 is out of bounds for axis 0 with size 0

## example 5
*input:*
```
7 0 0 0 0 0
```
*expected output:*
```
7 0 0 0 0 0
7 7 0 0 0 0
7 7 7 0 0 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 0 is out of bounds for axis 0 with size 0
