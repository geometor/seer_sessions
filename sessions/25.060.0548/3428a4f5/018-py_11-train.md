
## example 1
*input:*
```
0 0 0 2 2
0 0 2 0 2
2 0 0 2 2
2 2 0 0 2
0 0 0 0 2
0 2 0 0 0
4 4 4 4 4
2 0 0 0 0
2 2 0 0 0
2 0 2 0 0
0 0 2 0 0
0 0 0 2 2
2 0 0 2 0
```
*expected output:*
```
3 0 0 3 3
3 3 3 0 3
0 0 3 3 3
3 3 3 0 3
0 0 0 3 0
3 3 0 3 0
```
*transformed output:*
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
3 3 3 3 3
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 2 2 2 2
0 0 0 0 2
2 0 2 2 2
0 0 2 2 0
2 2 2 2 0
2 2 0 0 2
4 4 4 4 4
0 0 0 0 0
0 0 2 0 0
2 0 0 0 2
0 0 0 2 0
0 2 0 2 0
0 2 2 2 0
```
*expected output:*
```
0 3 3 3 3
0 0 3 0 3
0 0 3 3 0
0 0 3 0 0
3 0 3 0 0
3 0 3 3 3
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**

## example 3
*input:*
```
2 2 0 2 2
2 0 2 2 2
2 0 0 0 0
0 2 0 2 0
2 2 2 0 2
2 0 2 0 0
4 4 4 4 4
2 0 0 2 2
0 0 2 0 2
2 2 0 0 0
0 0 2 0 2
0 2 0 2 2
0 2 2 0 2
```
*expected output:*
```
0 3 0 0 0
3 0 0 3 0
0 3 0 0 0
0 3 3 3 3
3 0 3 3 0
3 3 0 0 3
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**

## example 4
*input:*
```
0 2 0 2 0
2 2 0 2 2
0 2 2 2 0
0 2 2 0 0
0 2 2 2 2
2 0 2 0 2
4 4 4 4 4
2 0 2 2 2
0 2 2 0 0
2 0 2 0 2
2 0 0 0 2
2 2 0 2 0
2 0 2 2 0
```
*expected output:*
```
3 3 3 0 3
3 0 3 3 3
3 3 0 3 3
3 3 3 0 3
3 0 3 0 3
0 0 0 3 3
```
size: None
palette: None
color count: None
pixels off: None
**FAILED!**
