class Menu:
    def __init__(self, title, parent):
        self.title = title
        self.choices = []
        self.parent = parent
        self.pos = 0
        self.top = 0

    def get_parent(self):
        return self.parent

    def add_entry(self, desc, action):
        self.choices.append(Choice(desc, action))

    def get_size(self):
        return len(self.choices)

    def check_pos(self, pos):
        return (pos >= 0) and (pos < self.get_size())

    def choose(self, pos):
        return self.choices[pos].get_action()

    def print_menu(self):
        print(self.title)
        for x in range(self.get_size()):
            print("{}: {}".format(x + 1, self.choices[x].get_desc()))

    def get_lines(self):
        lines = []
        for x in range(self.get_size()):
            lines.append(self.choices[x].get_desc())
        return lines

    def get_screen_lines(self):
        lines = []
        x = self.top
        while x < self.top + 5 and x < self.get_size():
            lines.append(self.choices[x].get_desc())
            x += 1
        return lines

    def get_screen_pos(self):
        return self.pos - self.top

    def up(self):
        if self.pos > 0:
            self.pos -= 1
            if self.pos < self.top:
                self.top -= 1

    def down(self):
        if self.pos < self.get_size() - 1:
            self.pos += 1
            if self.pos > self.top + 4:
                self.top += 1

    def select(self):
        return self.choices[self.pos].get_action()


class Choice:
    def __init__(self, desc, action):
        self.description = desc
        self.action = action

    def get_desc(self):
        return self.description

    def get_action(self):
        return self.action

    def print_description(self):
        print(self.description)
