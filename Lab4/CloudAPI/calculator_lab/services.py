# calculator/services.py
def calculate(num1, num2, operation):
    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        return None, "Invalid number format"

    if operation == 'add':
        return num1 + num2, None
    elif operation == 'subtract':
        return num1 - num2, None
    elif operation == 'multiply':
        return num1 * num2, None
    elif operation == 'divide':
        if num2 == 0:
            return None, "Division by zero"
        return num1 / num2, None
    else:
        return None, "Unsupported operation"
