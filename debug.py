def printif(message, enable=True):
    '''
    Function
    -----------------------------------------------------------------------------------------------
    Prints out a message only if user passed on a value to enable the message to be printed

    Parameters
    -----------------------------------------------------------------------------------------------
    message : str
        A message to be printed out
    enable : bool
        A boolean value that determines whether or not to print out the message

    Returns
    -----------------------------------------------------------------------------------------------
    Nothing
    '''
    if enable:
        print(message)