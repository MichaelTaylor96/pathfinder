small_map_min = 3139
small_map_max = 5648
small_map_dimensions = 600
big_map_min = 3139
big_map_max = 6933
big_map_dimensions = 1201
from PIL import Image, ImageDraw

def get_coordinate_list(file):
    list_of_rows = []
    with open(file) as data:
        for line in data:
            line = line.strip()
            row = line.split(' ')
            row[-1] = row[-1].replace('\n', '')
            for i in range(len(row)):
                row[i] = int(row[i])
            list_of_rows.append(row)
    return list_of_rows

def get_rgb_value(elevation, map_max):
    percent = (elevation - 3139) / (map_max - 3139)
    rgb = int(255 * percent)
    return rgb

def get_points_colors(list_of_rows, map_max):
    points_colors = {}
    for row in range(len(list_of_rows)):
        for item in range(len(list_of_rows[row])):
            rgb_value = get_rgb_value(list_of_rows[row][item], map_max)
            points_colors[(item, row)] = rgb_value
    return points_colors

def get_best_path(starting_y, points_colors, map_dimensions):
    current_point = (0, starting_y)
    current_elevation = (points_colors[current_point])
    path = [[current_point], 0]
    for i in range(len(list_of_rows[0]) - 1):
        step_choices = [(current_point[0]+1, current_point[1]-1), 
                        (current_point[0]+1, current_point[1]),
                        (current_point[0]+1, current_point[1]+1)]
        for choice in step_choices:
            if choice[1] < 0 or choice[1] >= map_dimensions:
                step_choices.remove(choice)
        elevation_choices = [points_colors[coord] for coord in step_choices]
        differences = [abs(current_elevation - choice) for choice in elevation_choices]
        choices = list(zip(step_choices, differences))
        sorted_choices = sorted(choices,key=lambda x: x[1])
        current_point = sorted_choices[0][0]
        current_elevation = points_colors[current_point]
        path[0].append(current_point)
        path[1] += sorted_choices[0][1]
    return path

list_of_rows = get_coordinate_list('elevation_small.txt')
points_colors = get_points_colors(list_of_rows, small_map_max)

img = Image.new('RGB', (small_map_dimensions, small_map_dimensions))
draw = ImageDraw.Draw(img)
for point in points_colors:
    draw.point(point, (points_colors[point],points_colors[point],points_colors[point]))
# paths = []
# for i in range(small_map_dimensions):
best_path = get_best_path(100, points_colors, small_map_dimensions)
    # paths.append(best_path)
for point in best_path[0]:
    draw.point(point, (0, 255, 0))
# sorted_paths = sorted(paths, key=lambda x: x[1])
# for point in sorted_paths[0][0]:
#     draw.point(point, (0, 0, 255))

# img.show()
