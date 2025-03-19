
## example 1
*input:*
```
0 0
0 0
0 0
0 0
0 0
0 0
0 0
0 0
0 0
1 0
```
*expected output:*
```
0 1
1 0
0 1
1 0
0 1
1 0
0 1
1 0
0 1
1 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: index 2 is out of bounds for axis 1 with size 2

## example 2
*input:*
```
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
1 0 0
```
*expected output:*
```
0 1 0
1 0 0
0 1 0
0 0 1
0 1 0
1 0 0
0 1 0
0 0 1
0 1 0
1 0 0
```
*transformed output:*
```
0 0 1
1 0 0
0 0 0
0 1 0
0 0 1
1 0 0
0 0 0
0 1 0
0 0 1
1 0 0
```
size: True
palette: True
color count: False
pixels off: 12
**FAILED!**

## example 3
*input:*
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
1 0 0 0
```
*expected output:*
```
0 0 0 1
0 0 1 0
0 1 0 0
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
0 0 1 0
0 1 0 0
1 0 0 0
```
*transformed output:*
```
0 0 1 0
1 0 0 0
0 0 0 0
0 1 0 0
0 0 1 0
1 0 0 0
0 0 0 0
0 1 0 0
0 0 1 0
1 0 0 0
```
size: True
palette: True
color count: False
pixels off: 16
**FAILED!**
