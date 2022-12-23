from turtle import Turtle, Screen, numinput
from random import randint, choice

LAYOUT_LENGTH = 20
NODE_ROWS = 1  # easier to visualize with one row
SPEED = 1
NORMAL_KEY = "n"
FAST_KEY = "f"
QUIT_KEY = "q"

LEVEL_COLOR = {
    0: "green",
    1: "yellow",
    2: "lightblue",
    3: "pink",
    4: "orange",
    5: "violet",
    6: "blue",
    7: "red",
    8: "indigo",
    9: "brown"
}


class Label(Turtle):
    def __init__(self, font_size=24, color="black", speed=6):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.pencolor(color)
        self.speed(speed)
        self.FONT = ('Arial', font_size, 'normal')

    def write(self, text, x, y):
        self.goto(x, y)
        super().write(text, move=False, align='center', font=self.FONT)


class Node(Turtle):
    def __init__(self, value, speed=6):
        super().__init__()
        self.shape("circle")
        self.color("green")
        self.shapesize(2)
        self.penup()
        self.speed(speed)
        self.label = Label(font_size=22)
        # node properties
        self.value = value
        self.memory_location = None

    def __lt__(self, other):
        return self.value < other.value

    def goto(self, x, y):
        self.label.clear()
        super().goto(x, y)
        self.label.write(f"{self.value}", self.xcor(), self.ycor() - 0.4)

    def get_value(self):
        return self.value

    def cleanup(self):
        self.clear()
        self.label.clear()
        self.hideturtle()


class MemoryManager:
    def __init__(self, x=10, y=1, length=12, offset=2.5):
        self.x = x
        self.y = y
        self.length = length
        self.offset = offset
        self.spaces = x * y
        # create all possible positions
        self.positions = {}
        self.init_grid()
        # mark all spaces None
        self.available = {n: None for n in range(self.spaces)}  # range(self.spaces, 0, -1)} for reverse

        # todo: currently grid, will need tree
    def init_grid(self):
        key = 0
        for y in range(self.y):
            for x in range(self.x):
                self.positions[key] = (self.length / 2 - self.x / 2 + x, y + self.offset)
                key += 1

    def allocate(self, node: Node):
        if self.spaces > 0:
            for key, value in self.available.items():
                if value is None:
                    self.available[key] = node
                    self.available[key].goto(self.positions[key][0], self.positions[key][1])
                    node.memory_location = key
                    self.spaces -= 1
                    return key

    def garbage(self, node: Node):
        for key, value in self.available.items():
            if value == node:
                self.available[key] = None
                self.spaces += 1

    def reset(self):
        self.spaces = self.x * self.y
        self.available = {n: None for n in range(self.spaces)}  # range(self.spaces, 0, -1)} for reverse


def merge_sort(items, current_level=0):
    next_level = current_level + 1

    if len(items) <= 1:
        return items

    middle_index = len(items) // 2

    left_split = items[:middle_index]
    right_split = items[middle_index:]

    # visualizing by moving
    # find x distances between items in recursive level
    x_distance = (LAYOUT_LENGTH / (2 ** next_level + 1)) / 4

    for el in left_split:  #
        el.goto(el.xcor() - x_distance, el.ycor() + 2)  #
        el.color(LEVEL_COLOR[next_level])

    for el in right_split:  #
        el.goto(el.xcor() + x_distance, el.ycor() + 2)  #
        el.color(LEVEL_COLOR[next_level])

    left_sorted = merge_sort(left_split, next_level)
    right_sorted = merge_sort(right_split, next_level)

    return merge(left_sorted, right_sorted, current_level)


def merge(left, right, current_level):
    result = []
    result_position_x = (left[0].xcor() + right[0].xcor()) / 2 - ((len(left) + len(right)) / 4)
    position_counter = 0
    while left and right:
        if left[0] < right[0]:
            result.append(left[0])
            # move node
            left[0].goto(result_position_x + position_counter, left[0].ycor() - 2)
            left[0].color(LEVEL_COLOR[current_level])
            position_counter += 1
            left.pop(0)
        else:
            result.append(right[0])
            # move node
            right[0].goto(result_position_x + position_counter, right[0].ycor() - 2)
            right[0].color(LEVEL_COLOR[current_level])
            position_counter += 1
            right.pop(0)

    if left:
        # move nodes
        for node in left:
            node.goto(result_position_x + position_counter, node.ycor() - 2)
            node.color(LEVEL_COLOR[current_level])
            position_counter += 1
        result += left

    if right:
        # move node
        for node in right:
            node.goto(result_position_x + position_counter, node.ycor() - 2)
            node.color(LEVEL_COLOR[current_level])
            position_counter += 1
        result += right

    return result


def start(num_items):
    s.onkeypress(None, FAST_KEY)
    s.onkeypress(None, NORMAL_KEY)

    # create memory layout
    m = MemoryManager(num_items, NODE_ROWS, LAYOUT_LENGTH)

    # create list of nodes
    unordered_node_list = []
    for _ in range(num_items):
        new = Node(randint(1, 1000), speed=SPEED)
        new.hideturtle()
        new.speed(9)
        unordered_node_list.append(new)
        m.allocate(new)
        new.showturtle()
        new.speed(1)

    # ACTION!
    ordered_list = merge_sort(unordered_node_list)

    # Yay!
    for _ in range(30):
        for node in ordered_list:
            node.color(choice(LEVEL_COLOR))

    # Bye!
    for node in ordered_list:
        node.cleanup()

    s.onkeypress(fast, FAST_KEY)
    s.onkeypress(normal, NORMAL_KEY)


def fast():
    s.tracer(10)
    try:
        num = int(numinput("Number of items", "Number of items to sort (<= 16 recommended): "))
    except TypeError:
        return
    else:
        start(num)
    finally:
        s.getcanvas().focus_force()
    s.update()


def normal():
    s.tracer(1)
    try:
        num = int(numinput("Number of items", "Number of items to sort (20 max): "))
    except TypeError:
        return
    else:
        start(num)
    finally:
        s.getcanvas().focus_force()
    s.update()


def finish():
    s.bye()

###############################################################################
# END OF DEFs
###############################################################################


s = Screen()
s.reset()
s.setworldcoordinates(llx=0.0, urx=LAYOUT_LENGTH, lly=LAYOUT_LENGTH, ury=0.0)

labeler = Label(speed=9)
labeler.write("Merge Sort Recursive Visualization: Levels down when recursion", 10, 0.5)
labeler.write("Press:\n"
              "F for fast speed run\n"
              "N for normal speed run\n"
              "Q to quit\n"
              "Enlarge windows as necessary", 5, 15)


s.onkeypress(fast, FAST_KEY)
s.onkeypress(normal, NORMAL_KEY)
s.onkeypress(finish, QUIT_KEY)

s.listen()

s.mainloop()
