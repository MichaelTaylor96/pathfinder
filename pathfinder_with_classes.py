from PIL import Image, ImageDraw
from random import randint, randrange, choice

class Data:
    def __init__(self, file):
        self.file = file
        self.list_of_rows = []
        with open(self.file) as data:
            for line in data.readlines():
                self.list_of_rows.append([int(num) for num in line.split()])
        self.width = len(self.list_of_rows[0])
        self.height = len(self.list_of_rows)
        self.min = min([min(row) for row in self.list_of_rows])
        self.max = max([max(row) for row in self.list_of_rows])

    def rgb(self, point_x, point_y):
        rgb_value = int(((self.list_of_rows[point_y][point_x] - self.min) / (self.max - self.min)) * 255)
        return (rgb_value, rgb_value, rgb_value)

    def get_elevation(self, point):
        return self.list_of_rows[point[1]][point[0]]

    def get_rgb(self, point):
        return self.rgb(point[0], point[1])[0]

class Map:
    def __init__(self, data):
        self.data = data
        self.image = Image.new('RGB', (self.data.width, self.data.height))
        self.draw = ImageDraw.Draw(self.image)

    def draw_map(self):
        for y in range(len(self.data.list_of_rows)):
            for x in range(len(self.data.list_of_rows[y])):
                self.draw.point((x, y), self.data.rgb(x, y))
        return self

    def draw_path(self, path, color):
        for point in path[0]:
            self.draw.point(point, color)
        return self

    def display(self):
        return self.image.show()

class Pathfinder:
    def __init__(self, starting_point, data):
        self.starting_point = starting_point
        self.data = data

    def greedy_path(self):
        current_point = self.starting_point
        path_cost = 0
        path = []
        path.append(current_point)
        for step in range(self.data.width-1):
            up = (step+1, max(current_point[1]-1, 0))
            straight = (step+1, current_point[1])
            down = (step+1, min(current_point[1]+1, self.data.height-1))
            choices = [up, straight, down]

            up_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(up))
            straight_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(straight))
            down_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(down))
            costs = [up_cost, straight_cost, down_cost]

            choices_costs = dict(zip(choices, costs))
            sorted_choices = sorted(choices_costs, key=choices_costs.__getitem__)

            if up_cost >= straight_cost <= down_cost:
                path_cost += straight_cost
                path.append(straight)
                current_point = straight

            elif up_cost == down_cost:
                    options = [up, down]
                    decision = choice(options)
                    path_cost += choices_costs[decision]
                    path.append(decision)
                    current_point = decision
            
            else:
                path_cost += choices_costs[sorted_choices[0]]
                path.append(sorted_choices[0])
                current_point = sorted_choices[0]

        return (path, path_cost)

    def recursive_path(self, starting_point):
        current_point = starting_point
        path_cost = 0
        path = []
        path.append(current_point)

        up = (current_point[0]+1, max(current_point[1]-1, 0))
        straight = (current_point[0]+1, current_point[1])
        down = (current_point[0]+1, min(current_point[1]+1, self.data.height-1))
        choices = [up, straight, down]

        up_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(up))
        straight_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(straight))
        down_cost = abs(self.data.get_elevation(current_point)-self.data.get_elevation(down))
        costs = [up_cost, straight_cost, down_cost]

        choices_costs = dict(zip(choices, costs))
        sorted_choices = sorted(choices_costs, key=choices_costs.__getitem__)

        if current_point[0] >= self.data.width - 587:
            path.append(sorted_choices[0])
            path_cost += choices_costs[sorted_choices[0]]
            return (path_cost, path)

        path_choices = [self.recursive_path(point) for point in choices]
        sorted_paths = sorted(path_choices, key=lambda x: x[0])
        path_cost += sorted_paths[0][0]
        path += sorted_paths[0][1]
        return (path_cost, path)

data = Data('elevation_small.txt')
a_map = Map(data)
a_map.draw_map()
pathfinder = Pathfinder((0, 0), data)
# paths = []
path = pathfinder.recursive_path((0, 300))
print(path)
# for y in range(data.height):
#     pathfinder.starting_point = (0, y)
#     path = pathfinder.greedy_path()
#     paths.append(pathfinder.greedy_path())
#     a_map.draw_path(path, (0, 255, 0))
# sorted_paths = sorted(paths, key=lambda x: x[1])
# a_map.draw_path(sorted_paths[0], (0, 0, 255))
# a_map.display()