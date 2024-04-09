import sys

# Registry and decorator to add functions called with --args without explicitly coding them
# Improper number of arguments or no arguments must be errored within the function and caught by the try block at function call
registry = {}
def register(callstring):
    def funcRegister(func):
        registry[callstring] = func
        return func
    return funcRegister

@register("--SNIP")
def controlTest(arguments):
    print("I'm sniffing now")
    print(f"I was given {arguments[0]} arguments")
    print(f"The argument list is {arguments[1]}")

@register("--CTIP")
def controlTest(arguments):
    print("I'm controlling now")
    print(f"I was given {arguments[0]} arguments")
    print(f"The argument list is {arguments[1]}")

if __name__ == "__main__":
    argumentGroups = {}
    argPrev = ""

    for arg in sys.argv[1:]:
        if (arg[0:2] == "--"):
            argumentGroups[arg] = [0, []]
            argPrev = arg
        else:
            argumentGroups[argPrev][1].append(arg)
            argumentGroups[argPrev][0] += 1
    
    if "--CTIP" not in argumentGroups:
        raise Exception("Controller IP must be specified with --CTIP [IP]")

    if "--SNIP" not in argumentGroups:
        raise Exception("Interface to sniff must be specified with --SNIP [IP]")
    
    for flag, params in argumentGroups.items():
        try:
            registry[flag](params)
        except KeyError as err:
            raise Exception(f"Flag \"{flag}\" is not implemented") from err
        except Exception as err:
            raise err
    
    print(argumentGroups)
