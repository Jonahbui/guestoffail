#--------------------------------------------------------------------------------------------------
# Author: Jonah Bui
# Date: 4/17/2020
# Purpose: implements the functions necessary to convert an infix expression into a postfix
# expression while calculating the output of the postfix expression 
# To-do List:
#  > Error handling incorrect input
# Changelogs:

from debug import printif

def contains_operand(number):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Checks if a string contains only characters 0-9

    Parameters
    -----------------------------------------------------------------------------------------------
    number : str
        A string to check if it contains only numbers

    Returns
    -----------------------------------------------------------------------------------------------
    True if string only has numbers
    False if string has more than numbers
    '''
    # Iterate through each character in the string and check if is a number 
    for char in number:
        number_found = False
        for num in "1234567890":
            if char == num:
                number_found = True
                break
        if not number_found:
            return False
    # If all characters are numbers, return True
    return True

def contains_operator(op):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Checks if a char contains an operator

    Parameters
    -----------------------------------------------------------------------------------------------
    op: str
        A string to check if it is an operator such as ^, *, /, (), -, or +

    Returns
    -----------------------------------------------------------------------------------------------
    True if string is an operator
    False if string is not an operator
    '''
    for operator in "^*/()-+":
        if op == operator:
            return True

def precedence(op):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Determines the order of precedence of an operator

    Parameters
    -----------------------------------------------------------------------------------------------
    op: str
        A string with an operator such as ^, *, /, (), -, or +

    Returns
    -----------------------------------------------------------------------------------------------
    1 for (,)
    2 for +,-
    3 for *,/
    4 for ^
    -1 for invalid input
    '''
    if op == "(":
        return 1
    elif op == "+" or op =="-":
        return 2
    elif op == "*" or op =="/":
        return 3
    elif op == "^":
        return 4
    else:
        return -1

def associativity(op):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Determines the order of precedence of an operator

    Parameters
    -----------------------------------------------------------------------------------------------
    op: str
        A string with an operator such as ^, *, /, (), -, or +

    Returns
    -----------------------------------------------------------------------------------------------
    0 for (,)
    2 for +,-
    3 for *,/
    4 for ^
    -1 for invalid input
    '''
    if op == "+" or op == "-" or op == "*" or op == "/":
        return 'ltr'
    else:
        return 'rtl'

def parse_expression(input, show_steps=False):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Takes in a string that represents a mathematical expression  and parses it into a list

    Parameters
    -----------------------------------------------------------------------------------------------
    input : str
        A string that represents a mathematical expression (with no spaces in between
        operators and operands)
    show_steps : bool
        A boolean that determines whether the debugging log should be enabled or disabled
    Returns
    -----------------------------------------------------------------------------------------------
    A list containing a parsed mathematical expression
    '''
    # Use to store regular expression string
    parsed_expression = ''
    for char in input:
        # If the char is a number add it to the string normally. The operators will place the
        # the spaces properly
        if contains_operand(char):
            parsed_expression=parsed_expression+char
            break
        # If a ( is encountered first while string is empty, don't add a space to the left
        elif contains_operator(char):
            parsed_expression=parsed_expression+" "+char+" "
        break
    
    # Get rid of leading/trailing white spaces to avoid improper separations with .split()
    parsed_expression = parsed_expression.strip()
    
    # Remove any double spaces with single spaces to properly seperate the expresssion
    parsed_expression = parsed_expression.replace("  ", " ")
    
    # Turn expression into a list
    parsed_expression = parsed_expression.split(sep=' ')

    printif(f"Parsed Expression = {parsed_expression}\n", show_steps)
    return parsed_expression

def infix_to_postfix(infix, show_steps=False):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Turns an infix expression into a postfix expression

    Parameters
    -----------------------------------------------------------------------------------------------
    infix : str
        A mathematical expression represented as a string that will be converted to a postfix
        expression
    show_steps : bool
        A boolean that determines whether the debugging log should be enabled or disabled

    Returns
    -----------------------------------------------------------------------------------------------
    A postfix expression represented as a list
    '''
    # Store postfix expression
    postfix = []

    # Keeps track of operators to order them properly
    stack = []
    
    # Iterate through each operator and operand and convert it to a postfix expression
    for element in infix:
        printif(f"Element being worked on: {element}", show_steps)

        # If element is an operand, add it to the postfix expression (keep ordering the same)
        # just like in the infix expression
        if contains_operand(element):
            printif(f"A number is found", show_steps)
            postfix.append(element)
        
        # If element is a (, push it to the stack
        elif element == "(":
            printif(f"A \'(\' is found", show_steps)
            stack.append("(")
        
        # If the element is a ), pop all operators off stack until ( is found.
        elif element == ")":
            printif(f"A \')\' is found", show_steps)
            val = stack.pop()
            while val is not "(":
                postfix.append(val)
                if len(stack) > 0:
                    val = stack.pop()
                else:
                    break
        
        # If there are nothing in the stack, push the operator to fill the stack
        # Prevents IndexError and starts the translation
        elif contains_operator(element) and len(stack) == 0:
            printif(f"No element in stack", show_steps)
            stack.append(element)
        
        # If the element is an operator with a greater precedence than the top, add it to stack
        elif contains_operator(element) and (precedence(element) > precedence(stack[len(stack)-1])):
            printif(f"Greater precedence", show_steps)
            stack.append(element)
        
        # If the element is an operator with lower precedence than top, pop until lower precedence
        # is found. If empty, push op to stack
        elif contains_operator(element) and (precedence(element) < precedence(stack[len(stack)-1])):
            printif(f"Lower precedence", show_steps)
            val = stack.pop()
            while (precedence(element) <= precedence(val)):
                postfix.append(val)
                if len(stack) > 0:
                    val = stack.pop()
                else:
                    break
            stack.append(element)
        
        # If the element is an operator with an equal precedence compared to the top, and the
        # operator on top of the stack is left-to-right associative, pop operators off stack until
        # lower precedence found
        elif contains_operator(element) and (precedence(element) == precedence(stack[len(stack)-1])):
            printif(f"Equal precedence", show_steps)
            val = stack.pop()
            postfix.append(val)
            while (precedence(element) <= precedence(val)):
                if len(stack) > 0:
                    val = stack.pop()
                    postfix.append(val)
                else:
                    break
            stack.append(element)
        
        # Print the results from each step
        printif(f"Stack = {stack}", show_steps)
        printif(f"Postfix Expression = {postfix}\n", show_steps)
    
    # Clear out the stack and push the remaining elements onto the postfix expression
    while len(stack) > 0:
        postfix.append(stack.pop())

    # Print the final result of the infix to postfix
    printif(f"End Result", show_steps)
    printif(f"Stack = {stack}", show_steps)
    printif(f"Postfix Expression = {postfix}", show_steps)

    return postfix

def calculate(input, show_steps=False):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Calculate the value of a postfix mathematical expression.

    Parameters
    -----------------------------------------------------------------------------------------------
    input : str
        A postfix mathematical expression to calculate value from
    show_steps : bool
        A boolean that determines whether the debugging log should be enabled or disabled

    Returns
    -----------------------------------------------------------------------------------------------
    The value of the postfix mathematical expression
    '''
    stack = []
    for element in input:
        if contains_operand(element):
            stack.append(element)
        elif element == "+":
            b = stack.pop()
            a = stack.pop()
            stack.append(float(a)+float(b))
        elif element == "-":
            b = stack.pop()
            a = stack.pop()
            stack.append(float(a)-float(b))
        elif element == "*":
            b = stack.pop()
            a = stack.pop()
            stack.append(float(a)*float(b))
        elif element == "/":
            b = stack.pop()
            a = stack.pop()
            stack.append(float(a)/float(b))
        elif element == "^":
            b = stack.pop()
            a = stack.pop()
            stack.append(pow(float(a),float(b)))
        printif(f"Stack = {stack}", show_steps)
    return stack.pop()