def dec(some_function):
    def wrapper():
        print("decorator")
        some_function()
        print("decorator after")
    return wrapper

@dec
def sample():
    print("sample")

if __name__ == "__main__":
    sample()
