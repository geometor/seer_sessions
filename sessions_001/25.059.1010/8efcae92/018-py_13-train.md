
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 2 1 1 1 0 0
0 0 1 1 1 1 1 0 0 0 1 1 1 1 1 1 1 1 0 0
0 0 1 1 1 2 1 0 0 0 1 2 1 1 1 1 2 1 0 0
0 0 1 1 2 1 1 0 0 0 1 1 1 1 1 1 1 1 0 0
0 0 1 1 1 1 1 0 0 0 1 1 1 2 1 1 1 1 0 0
0 0 1 2 1 1 1 0 0 0 1 1 1 1 1 1 1 1 0 0
0 0 1 1 1 1 1 0 0 0 1 1 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 2 1 2 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 2 1 2 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 2 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 2 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
1 1 1 1 1 1
1 2 1 2 1 1
1 1 2 1 2 1
1 2 1 1 1 1
1 1 1 2 1 1
```
*transformed output:*
```
1 1 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 1 1 1 1 1 2 1 1 1 1 2 1 1 1
1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 2 1 1 1 1 1 1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 2 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 1 2 1 1 1 1 1 1 2 0 0 0 1 1 1 1 1 2
0 0 1 1 1 1 1 2 1 1 1 0 0 0 1 1 2 1 1 1
0 0 1 1 1 2 1 1 1 2 1 0 0 0 1 1 1 1 1 1
0 0 2 1 1 1 1 1 1 1 1 0 0 0 1 1 1 2 1 1
0 0 1 1 1 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1
0 0 1 1 1 1 1 2 1 1 1 0 0 0 1 2 1 1 1 1
0 0 1 2 1 1 1 1 1 1 1 0 0 0 1 1 1 1 2 1
0 0 1 1 1 2 1 1 1 1 2 0 0 0 1 2 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
1 1 1 2 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
1 2 1 1 1 1 1 2 1 0 0 1 1 1 1 1 1 0 0 0
1 1 1 1 2 1 1 1 1 0 0 1 1 1 2 1 1 0 0 0
1 1 1 1 1 1 2 1 1 0 0 1 2 1 1 1 1 0 0 0
1 1 2 1 1 1 1 1 1 0 0 1 1 1 1 1 1 0 0 0
1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
1 1 1 1 2 1 1 1 1
1 2 1 1 1 1 1 1 2
1 1 1 1 1 2 1 1 1
1 1 1 2 1 1 1 2 1
2 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1
1 1 1 1 1 2 1 1 1
1 2 1 1 1 1 1 1 1
1 1 1 2 1 1 1 1 2
```
*transformed output:*
```
1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 2 1 1 1 1 1 1 2 1 1 1 1 1 1 1
1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 2 1
1 1 1 1 2 1 1 1 2 1 1 1 1 1 1 1 1
1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 2 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 2 1 1 1 0 0 1 1 1 1 1 1 1 1 1 0 0
0 1 1 1 1 1 1 0 0 1 1 1 1 1 1 1 1 2 0 0
0 1 2 1 1 2 1 0 0 1 1 2 1 1 1 1 1 1 0 0
0 1 1 1 1 1 1 0 0 1 1 1 1 1 2 1 1 1 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 1 1 1 2 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 0 2 1 2 1 0 0 1 1 1 2 1 1 1 2 1 0 0
0 0 0 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 0 1 2 1 2 0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 0 1 1 1 1 0 0 1 1 1 1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 1 1 1 1 1 1 1 2 1 1 1 1 1 2 1 1 1 0
0 0 1 1 1 2 1 1 1 1 1 2 1 1 1 1 1 1 1 0
0 0 1 2 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 0
0 0 1 1 1 1 1 1 1 1 1 1 2 1 1 2 1 1 1 0
```
*expected output:*
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 1 1 1 1 1 2 1 1 1
1 1 1 2 1 1 1 1 1 2 1 1 1 1 1 1 1
1 2 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 2 1 1 2 1 1 1
```
*transformed output:*
```
2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
1 2 1 1 2 1 1 1 1 1 2 1 1 1 1 1 1
```
size: True
palette: True
color count: False
pixels off: 13
**FAILED!**
