class Game:

    def a_decorator(self, a_func):
        def wrapTheFunction():
            print("I am doing some boring work before executing a_func()")
            a_func()
            print("I am doing some boring work after executing a_func()")

        return wrapTheFunction

    @a_decorator
    def a_function_requiring_decoration(self):
        print("I am the function which needs some decoration to remove my foul smell")

    a_function_requiring_decoration()
