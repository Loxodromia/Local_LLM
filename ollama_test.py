import ollama

# Test usage of the ollama library to generate a response using the DeepSeek-R1 model.

response = ollama.generate(
    model="deepseek-r1:8b",
    prompt="Write a Python function to calculate the factorial of a number."
)
print(response['response'])

# Sample output:
'''
<think>
We are going to write a function that calculates the factorial of a non-negative integer.    
 The factorial of a number n (denoted as n!) is the product of all positive integers up to n.
 For example: 5! = 5 * 4 * 3 * 2 * 1

 We can do this iteratively or recursively. Let's write an iterative version.

 Steps:
 1. Check if the input number is negative, then return None or raise an error (since factorial 
 2. If the number is zero, return 1 because by definition, 0! = 1.
 3. Otherwise, initialize a variable 'result' to 1 and multiply it by every integer from 1 up t

 However, note that factorials can be very large numbers for even moderately large inputs (e.g.
 We should consider using an iterative method with a loop or recursion? But let's avoid recursi

 Let's write the function accordingly.
</think>
To calculate the factorial of a number, we can use either an iterative or recursive approach in

**Approach:**
1. **Iterative Approach**: Start with 1 and multiply each subsequent integer up to `n` to accum
2. **Recursive Approach**: Define a base case (factorial of 0 is 1) and recursively call the fu

**Solution Code:**
```python
def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

        raise ValueError("Factorial is not defined for negative numbers.")
    else:
        return n * factorial_recursive(n - 1)
```

**Explanation:**
- **Iterative Approach**: This method uses a loop to multiply all integers from 1 up to `n`, which is efficient and avoids recursion depth issues. It handles edge cases like `n = 0` by initializing 
the result to 1.
- **Recursive Approach**: This approach directly follows the mathematical definition of factorial (base case: factorial(0) = 1, recursive step: n! = n * (n-1)!). However, it can lead to maximum recursion depth errors for large `n`, so it's provided as an alternative but not recommended for very large numbers.

Both approaches raise a `ValueError` if the input is negative. The iterative method uses O(n) time complexity and constant space, while the recursive method has the same time complexity but may use 
more space due to recursion stack overhead.
'''