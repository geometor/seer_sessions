
## example 1
*input:*
```
0 7 0
0 0 7
0 7 7
```
*expected output:*
```
0 7 0 0 7 0
0 0 7 7 0 0
0 7 7 7 7 0
```
*transformed output:*
```
0 0 7 7 0 0
0 0 0 0 7 7
0 7 7 7 7 0
```
size: True
palette: True
color count: True
pixels off: 8
**FAILED!**

## example 2
*input:*
```
0 0 0
0 7 7
0 0 0
```
*expected output:*
```
0 0 0 0 0 0
0 7 7 7 7 0
0 0 0 0 0 0
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0
7 0 0
0 0 0
```
*expected output:*
```
0 0 0 0 0 0
7 0 0 0 0 7
0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0
7 7 0 0 0 0
0 0 0 0 0 0
```
size: True
palette: True
color count: True
pixels off: 2
**FAILED!**
