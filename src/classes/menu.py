class Menu:
    def __init__(self, options, functions):
        self.options = options
        self.functions = functions

    def display(self):
        for i, option in enumerate(self.options, 1):
            print(f"{i}) {option}")

    def get_user_choice(self):
        while True:
            try:
                choice = int(input("Choose an option: "))
                if 1 <= choice <= len(self.options):
                    return choice
                else:
                    print("Invalid option. Please try again.")
                    self.display()   
            except ValueError:
                print("Invalid input. Please enter a number.")

    def execute_choice(self):
        choice = self.get_user_choice()

        function_to_execute = self.functions[choice - 1]
        function_to_execute()
