import pygame
import random
import heapq
import copy
import sys

# 初始化Pygame库，用于游戏开发和图形显示
pygame.init()

# 定义颜色，使用RGB元组表示
COLOR_BG = (255, 255, 255)          # 白色背景
COLOR_WALL = (0, 0, 0)              # 黑色墙壁（初始障碍物）
COLOR_PATH = (0, 255, 0)            # 绿色路径
COLOR_CURRENT = (255, 0, 0)         # 红色当前位置
COLOR_START = (0, 0, 255)           # 蓝色起点
COLOR_GOAL = (255, 165, 0)          # 橙色终点
COLOR_DISCOVERED = (200, 200, 200)  # 灰色已探索区域
COLOR_OBSTACLE = (0, 0, 0)          # 黑色发现的障碍物

# 设置格子大小和间距（像素）
CELL_SIZE = 40
MARGIN = 2

# 定义网格的行数和列数
GRID_ROWS = 13
GRID_COLS = 13

# 计算屏幕宽度和高度，包括网格和额外信息显示区域
SCREEN_WIDTH = GRID_COLS * (CELL_SIZE + MARGIN) + MARGIN
SCREEN_HEIGHT = GRID_ROWS * (CELL_SIZE + MARGIN) + MARGIN + 100  # 额外空间用于显示信息

# 创建Pygame显示窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("迷宫探索模拟")  # 设置窗口标题

# 设置字体，用于在屏幕上显示文字信息
font = pygame.font.SysFont(None, 24)

# 定义初始迷宫地图，0表示墙壁，1表示可通行路径
maze_grid = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 行0（顶部）
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # 行1
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 行2
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 行3
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 行4
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 行5
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 行6
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 行7
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 行8
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],  # 行9
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # 行10
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # 行11
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]   # 行12（底部）
]

def generate_maze_with_obstacles(maze_grid, num_obstacles=4):
    """
    生成带有随机障碍物的迷宫。

    参数:
        maze_grid (list): 原始迷宫地图。
        num_obstacles (int): 要放置的障碍物数量。

    返回:
        tuple: (生成的迷宫地图, 障碍物位置列表)
    """
    N = len(maze_grid)  # 迷宫的行数
    M = len(maze_grid[0])  # 迷宫的列数
    maze = copy.deepcopy(maze_grid)  # 深拷贝迷宫地图，避免修改原始数据

    # 获取所有可放置障碍物的空格子（值为1）
    empty_cells = [(i, j) for i in range(N) for j in range(M) if maze[i][j] == 1]

    # 定义入口和出口位置，以及它们周围的保护区域，防止放置障碍物堵塞路径
    entrance_exit = [(0, 6), (12, 6)]
    protected_cells = set(entrance_exit)
    for (i, j) in entrance_exit:
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < N and 0 <= nj < M:
                protected_cells.add((ni, nj))

    # 过滤掉受保护的格子，获取可用的障碍物放置位置
    available_cells = [cell for cell in empty_cells if cell not in protected_cells]

    # 检查是否有足够的可用格子放置障碍物
    if len(available_cells) < num_obstacles:
        raise ValueError("可放置障碍物的格子不足。")

    # 随机选择障碍物位置
    obstacles = random.sample(available_cells, num_obstacles)
    for (i, j) in obstacles:
        maze[i][j] = 0  # 将选中的格子设为墙壁

    return maze, obstacles

def calculate_degrees_with_discovered(maze, positions, discovered, visited):
    """
    计算指定格子的度数，考虑已发现的障碍物和已访问的区域。

    参数:
        maze (list): 当前迷宫地图。
        positions (list): 要计算度数的格子位置列表。
        discovered (dict): 已发现的格子信息，值为1表示可通行，0表示障碍物。
        visited (set): 已访问过的格子集合。
    返回:
        dict: 每个格子位置对应的度数。
    """
    N = len(maze)
    M = len(maze[0])
    degrees = {}
    # maze[position[0]][position[1]]=1
    # print('discover',discovered)
    # print('positions',positions)
    for (i, j) in positions:
        degree = 0
        # 检查上方邻居
        if i > 0 and maze[i - 1][j] == 1 and (i - 1, j) not in visited and discovered.get((i - 1, j), 1) == 1:
            degree += 1
        # 检查下方邻居
        if i < N - 1 and maze[i + 1][j] == 1 and (i + 1, j) not in visited and discovered.get((i + 1, j), 1) == 1:
            degree += 1
        # 检查左侧邻居
        if j > 0 and maze[i][j - 1] == 1 and (i, j - 1) not in visited and discovered.get((i, j - 1), 1) == 1:
            degree += 1
        # 检查右侧邻居
        if j < M - 1 and maze[i][j + 1] == 1 and (i, j + 1) not in visited and discovered.get((i, j + 1), 1) == 1:
            degree += 1
        degrees[(i, j)] = degree
    print(degrees)
    return degrees

def get_first_layer_indices(maze_grid):
    """
    获取第四象限边第一层格子的索引。

    参数:
        maze_grid (list): 迷宫地图。

    返回:
        list: 第一层格子的位置列表。
    """
    N = len(maze_grid)
    anti_diagonals = [[] for _ in range(2*N - 1)]  # 反对角线列表
    for i in range(N):
        for j in range(N):
            k = i + j  # 反对角线编号
            anti_diagonals[k].append(((i, j), maze_grid[i][j]))
    first_layer_indices = []
    for k in range(len(anti_diagonals)):
        anti_diag = anti_diagonals[k]
        if k < 6:
            continue  # 只考虑第四象限
        if all(value == 0 for (pos, value) in anti_diag):
            continue  # 全部为墙壁则跳过
        for index, (pos, value) in enumerate(anti_diag):
            if value != 0:
                first_layer_indices.append(pos)
                break  # 只取第一层非墙壁的格子
    # print('第四象限第一层', first_layer_indices)
    return first_layer_indices

def get_second_layer_indices(maze_grid):
    """
    获取第四象限边第二层格子的索引。

    参数:
        maze_grid (list): 迷宫地图。

    返回:
        list: 第二层格子的位置列表。
    """
    N = len(maze_grid)
    M = len(maze_grid[0])
    anti_diagonals = [[] for _ in range(N + M - 1)]
    for i in range(N):
        for j in range(M):
            k = i + j
            anti_diagonals[k].append(((i, j), maze_grid[i][j]))
    second_layer_indices = []
    for k in range(len(anti_diagonals)):
        anti_diag = anti_diagonals[k]
        if k < 6:
            continue  # 只考虑第四象限
        if all(value == 0 for (pos, value) in anti_diag):
            continue  # 全部为墙壁则跳过
        non_zero_count = 0
        for index, (pos, value) in enumerate(anti_diag):
            if value != 0:
                non_zero_count += 1
                if non_zero_count == 2:
                    second_layer_indices.append(pos)
                    break  # 只取第二层非墙壁的格子
    print('第四象限第二层格子',second_layer_indices)
    return second_layer_indices

def get_layers_indices_third_quadrant(maze_grid):
    """
    获取第三象限边第一层和第二层格子的索引。

    参数:
        maze_grid (list): 迷宫地图。

    返回:
        tuple: (第一层格子列表, 第二层格子列表)
    """
    N = len(maze_grid)
    M = len(maze_grid[0])
    diagonals = [[] for _ in range(N + M - 1)]
    for i in range(N):
        for j in range(M):
            k = j - i + (N - 1)  # 对角线编号，平移以避免负数
            diagonals[k].append(((i, j), maze_grid[i][j]))
    first_layer_indices = []
    second_layer_indices = []
    start_k = 6 - 0 + (N - 1)  # 起始对角线编号
    end_k = 6 - (N - 1) + (N - 1)  # 结束对角线编号
    for k in range(end_k, start_k + 1):
        diag = diagonals[k]
        if all(value == 0 for (pos, value) in diag):
            continue  # 全部为墙壁则跳过
        non_zero_positions = [pos for (pos, value) in diag if value != 0]
        if len(non_zero_positions) >= 1:
            first_layer_indices.append(non_zero_positions[0])  # 第一层
        if len(non_zero_positions) >= 2:
            second_layer_indices.append(non_zero_positions[1])  # 第二层
    print('第三象限第一层格子',first_layer_indices)
    print('第三象限第er层格子', second_layer_indices)
    return first_layer_indices, second_layer_indices

def heuristic(a, b):
    """
    曼哈顿距离启发式函数，用于A*算法。

    参数:
        a (tuple): 第一个点的坐标 (i, j)。
        b (tuple): 第二个点的坐标 (i, j)。

    返回:
        int: 曼哈顿距离。
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze_grid,maze, start, end, discovered):
    """
    实现A*搜索算法，找到从start到end的最短路径。

    参数:
        maze (list): 当前已知的迷宫地图。
        start (tuple): 起点坐标 (i, j)。
        end (tuple): 终点坐标 (i, j)。
        discovered (dict): 已发现的格子信息，值为1表示可通行，0表示障碍物。

    返回:
        list or None: 路径列表，如果无路径则返回None。
    """
    N = len(maze_grid)
    M = len(maze_grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 四个可能的移动方向（上下左右）

    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, end), 0, start, [start]))  # (f值, g值, 当前节点, 路径)
    closed_set = set()  # 已关闭的节点集合

    while open_list:
        f, g, current, path = heapq.heappop(open_list)  # 获取f值最小的节点
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = current[0] + dir[0], current[1] + dir[1]
            if 0 <= ni < len(maze_grid) and 0 <= nj < len(maze_grid[0]):
                if (ni, nj) not in discovered:
                    discovered[(ni, nj)] = maze[ni][nj]  # 标记为可通行或障碍物
        if current == end:
            return path  # 找到终点，返回路径

        if current in closed_set:
            continue  # 如果节点已处理，跳过

        closed_set.add(current)  # 标记当前节点为已处理

        for dir in directions:
            neighbor = (current[0] + dir[0], current[1] + dir[1])  # 计算邻居节点

            # 检查邻居节点是否在迷宫范围内且可通行且未被处理
            if (0 <= neighbor[0] < N and 0 <= neighbor[1] < M and
                maze_grid[neighbor[0]][neighbor[1]] == 1 and
                neighbor not in closed_set):

                # 如果邻居是已知的障碍物或已走过的区域（除了当前位置），则跳过
                if neighbor in discovered and discovered[neighbor] == 0:
                    continue

                g_neighbor = g + 1  # 计算从起点到邻居的代价
                f_neighbor = g_neighbor + heuristic(neighbor, end)  # 计算f值

                # 检查open_list中是否已有更优的路径
                in_open = False
                for item in open_list:
                    if item[2] == neighbor and item[1] <= g_neighbor:
                        in_open = True
                        break

                if not in_open:
                    heapq.heappush(open_list, (f_neighbor, g_neighbor, neighbor, path + [neighbor]))  # 将邻居加入open_list

    return None  # 如果open_list为空，表示无路径

def print_maze_pygame(screen, maze, discovered, path, position, score, stamina):
    """
    使用Pygame可视化迷宫及其状态。

    参数:
        screen (pygame.Surface): Pygame显示表面。
        maze (list): 迷宫地图。
        discovered (dict): 已发现的格子信息。
        path (list): 当前路径历史。
        position (tuple): 当前玩家位置。
        score (int): 当前得分。
        stamina (int): 剩余体力。
    """
    N = len(maze)
    M = len(maze[0])
    screen.fill(COLOR_BG)  # 填充背景色

    for i in range(N):
        for j in range(M):
            # 计算每个格子的矩形区域
            rect = pygame.Rect(
                MARGIN + j * (CELL_SIZE + MARGIN),
                MARGIN + i * (CELL_SIZE + MARGIN),
                CELL_SIZE,
                CELL_SIZE
            )
            # 根据格子的状态绘制不同颜色
            if (i, j) == position:
                pygame.draw.rect(screen, COLOR_CURRENT, rect)  # 当前玩家位置
            elif (i, j) == (0, 6):
                pygame.draw.rect(screen, COLOR_START, rect)  # 起点
            elif (i, j) == (12, 6):
                pygame.draw.rect(screen, COLOR_GOAL, rect)  # 终点
            elif (i, j) in path and (i, j) != position:
                pygame.draw.rect(screen, COLOR_PATH, rect)  # 路径
            elif (i, j) in discovered:
                if discovered[(i, j)] == 0:
                    pygame.draw.rect(screen, COLOR_OBSTACLE, rect)  # 已发现的障碍物
                else:
                    pygame.draw.rect(screen, COLOR_DISCOVERED, rect)  # 已探索的区域
            elif maze[i][j] == 0:
                pygame.draw.rect(screen, COLOR_WALL, rect)  # 墙壁
            else:
                pygame.draw.rect(screen, COLOR_BG, rect)  # 默认背景色

    # 绘制得分和剩余体力信息
    info_y = GRID_ROWS * (CELL_SIZE + MARGIN) + MARGIN + 10
    info_text = f"得分: {score}    剩余体力: {stamina}"
    text_surface = font.render(info_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, info_y))

    pygame.display.flip()  # 更新显示内容

def simulate_movement_pygame(maze):
    """
    模拟小人在迷宫中的移动过程，并进行可视化展示。

    参数:
        maze (list): 生成的迷宫地图。
    """
    N = len(maze)
    M = len(maze[0])
    position = (0, 6)  # 初始位置为起点
    stamina = 45       # 初始体力
    score = 0          # 初始得分
    discovered = {}    # 已发现的区域，值为1表示可通行，0表示障碍物
    discovered[position] = 1  # 标记起点为已发现
    path_history = [position]  # 路径历史记录
    visited = set()
    preposition=None
    visited.add(preposition)  # 标记起点为已访问
    goal = (12, 6)  # 终点位置

    clock = pygame.time.Clock()  # 创建时钟对象，用于控制帧率

    # 打印第四象限第一层的第二层索引（调试信息）


    # 定义阶段列表，每个阶段包含不同的移动策略
    phases = [
        {
            'layer_func': get_first_layer_indices,  # 获取第一层格子
            'order': 'left_to_right',               # 从左到右排序
            'layer': 'first',
            'quadrant': 'fourth'
        },
        {
            'layer_func': get_second_layer_indices, # 获取第二层格子
            'order': 'right_to_left',               # 从右到左排序
            'layer': 'second',
            'quadrant': 'fourth'
        },
        {
            'layer_func': lambda maze_grid: get_layers_indices_third_quadrant(maze_grid)[0],  # 获取第三象限第一层
            'order': 'closest_first',            # 最近的优先
            'layer': 'first',
            'quadrant': 'third'
        },
        {
            'layer_func': lambda maze_grid: get_layers_indices_third_quadrant(maze_grid)[1],  # 获取第三象限第二层
            'order': 'reverse',                   # 反向排序
            'layer': 'second',
            'quadrant': 'third'
        }
    ]

    phase_index = 0  # 当前阶段索引
    count = 0
    while True:

        while stamina > 0 and phase_index < len(phases):
            phase = phases[phase_index]  # 获取当前阶段
            # 获取当前阶段的层索引，使用原始maze_grid而不是当前迷宫
            layer_indices = phase['layer_func'](maze_grid)
            # print(phase_index,'阶段的层格子',layer_indices)
            # 过滤出未访问且可通行的目标格子
            targets = [pos for pos in layer_indices if pos not in visited and maze[pos[0]][pos[1]] == 1]
            # 计算这些目标格子的度数
            degrees = calculate_degrees_with_discovered(maze_grid, targets, discovered, visited)
            # 只考虑度数为2的目标格子

            targets = [pos for pos in targets if degrees.get(pos, 0) >= 2]
            # print('度数为2 ',targets)

            # 根据阶段的排序方式对目标格子进行排序
            if phase['order'] == 'left_to_right':
                targets.sort(key=lambda x: x[1])  # 按列从左到右排序
            elif phase['order'] == 'right_to_left':
                targets.sort(key=lambda x: -x[1])  # 按列从右到左排序
            elif phase['order'] == 'closest_first':
                targets.sort(key=lambda x: heuristic(position, x))  # 按与当前位置的距离最近排序
            elif phase['order'] == 'reverse':
                targets.reverse()  # 反向排序
            targets_back = copy.deepcopy(targets)
            while stamina > 0 and targets:
                # 重新计算剩余目标的度数
                degrees = calculate_degrees_with_discovered(maze_grid, targets, discovered, visited)
                targets = [pos for pos in targets if degrees.get(pos, 0) >= 2]
                if not targets:
                    break  # 如果没有符合条件的目标，退出循环

                target = targets[0]  # 选择第一个目标

                # 检查是否有足够的体力直接前往终点
                path_to_goal = astar_known_maze(maze_grid, maze, position, goal, discovered, visited)
                if path_to_goal and stamina - len(path_to_goal) < 3:
                    # 如果体力不足以完成当前任务，直接前往终点
                    previous_position = position  # 保存移动前的位置
                    position, stamina, score, preposition, path_history, visited = move_along_path(maze, position, goal,
                                                                                                   discovered, visited,
                                                                                                   path_history,
                                                                                                   stamina, score,
                                                                                                   clock,
                                                                                                   preposition=preposition
                                                                                                   )

                    # if position == previous_position:
                    #     # 如果位置未改变，说明无法前进，移除该目标
                    #     targets.pop(0)
                    #     continue  # 继续尝试下一个目标

                    print("剩余体力不足，直接前往出口。")
                    return  # 结束模拟

                # 使用A*算法找到到目标的路径
                # path = astar_known_maze(maze_grid,maze, position, target, discovered, visited)
                # if path is None:
                #     # 如果无法到达目标，移除该目标并继续
                #     targets.pop(0)
                #
                #     continue
                # else:
                #     # 沿路径移动到目标
                #     previous_position = position  # 保存移动前的位置
                #     position, stamina, score, preposition, path_history,visited  = move_along_path(
                #         maze, position, target, discovered, visited, path_history, stamina, score, clock,
                #         preposition=preposition
                #     )
                #     if position == previous_position:
                #         # 如果位置未改变，说明无法前进，移除该目标
                #         # targets.pop(0)
                #         continue  # 继续尝试下一个目标
                #
                #     # visited.add(target)  # 标记目标为已访问
                #     break  # 重新开始循环，以便重新计算目标列表
                previous_position = position  # 保存移动前的位置
                print('preposition', preposition)
                print('previous_position', previous_position)
                position, stamina, score, preposition, path_history, visited = move_along_path(
                    maze, position, target, discovered, visited, path_history, stamina, score, clock,
                    preposition=preposition
                )
                print('position', position)
                guzhangloc = []
                if position == previous_position:
                    guzhangloc.append(target)
                    # 如果位置未改变，说明无法前进，移除该目标
                    targets.pop(0)
                    print('移除后的', targets)
                    continue  # 继续尝试下一个目标
                else:
                    count=0

            else:
                # 如果当前阶段的所有目标都无法到达或度数不为2，进入下一个阶段
                phase_index += 1

        # 所有阶段完成后，前往终点
        path_to_goal = astar_known_maze(maze_grid, maze, position, goal, discovered, visited)
        if path_to_goal:
            position, stamina, score, preposition, path_history, visited = move_along_path(
                maze, position, goal, discovered, visited, path_history, stamina, score, clock, preposition=preposition
            )
        else:
            position=path_history[-2]
            count+=1
            visited.remove(position)
            visited.add(path_history[-1])
            path_history.pop()
            phase_index=0
            stamina=stamina-1
            print(stamina)
            print("无法到达出口。")


    # # 模拟结束，保持窗口打开，显示最终状态
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #
    # print_maze_pygame(screen, maze, discovered, path_history, position, score, stamina)
    # clock.tick(5)  # 控制帧率为5帧每秒

def astar_known_maze(maze_grid,maze, start, end, discovered, visited):
    """
    根据已知的迷宫信息执行A*搜索，找到从start到end的路径。

    参数:
        maze (list): 原始迷宫地图。
        start (tuple): 起点坐标 (i, j)。
        end (tuple): 终点坐标 (i, j)。
        discovered (dict): 已发现的格子信息，值为1表示可通行，0表示障碍物。
        visited (set): 已访问过的格子集合。

    返回:
        list or None: 路径列表，如果无路径则返回None。
    """
    N = len(maze_grid)
    M = len(maze_grid[0])
    # known_maze = [[1]*M for _ in range(N)]  # 初始化已知迷宫，默认所有可通行
    known_maze=copy.deepcopy(maze_grid)

    # 根据已发现的信息更新已知迷宫
    for i in range(N):
        for j in range(M):
            if (i, j) in discovered and discovered[(i, j)] == 0:
                known_maze[i][j] = 0  # 已发现的障碍物
            if (i, j) in visited and (i, j) != start:
                known_maze[i][j] = 0  # 已访问过的区域（除起点）
    # print(known_maze)
    # 使用A*算法搜索路径
    path = astar(known_maze,maze, start, end, discovered)
    # print('path=',path)
    return path


def move_along_path(maze,position, target, discovered, visited, path_history, stamina, score, clock,preposition):
    """
    沿指定路径移动到目标位置，同时更新状态和可视化。

    参数:
        maze (list): 迷宫地图。
        position (tuple): 当前玩家位置。
        target (tuple): 目标位置。
        discovered (dict): 已发现的格子信息。
        visited (set): 已访问过的格子集合。
        path_history (list): 路径历史记录。
        stamina (int): 当前剩余体力。
        score (int): 当前得分。
        clock (pygame.time.Clock): 时钟对象，用于控制帧率。

    返回:
        tuple: 更新后的 (position, stamina, score)。
    """
    # 使用A*算法找到到目标的路径
    # for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    #     ni, nj = position[0] + dir[0], position[1] + dir[1]
    #     if 0 <= ni < len(maze_grid) and 0 <= nj < len(maze_grid[0]):
    #         if (ni, nj) not in discovered:
    #             discovered[(ni, nj)] = maze[ni][nj]  # 标记为可通行或障碍物
    path = astar_known_maze(maze_grid,maze, position, target, discovered, visited)
    if path is None:

        preposition=position
        # path = astar_known_maze(maze_grid, maze, position, target, discovered, visited)
        return position, stamina, score, preposition, path_history,visited  # 如果无路径，返回当前状态

    for step in path[:]:  # 跳过起点
        for dir in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = position[0] + dir[0], position[1] + dir[1]
            if 0 <= ni < len(maze_grid) and 0 <= nj < len(maze_grid[0]):
                if (ni, nj) not in discovered:
                    discovered[(ni, nj)] = maze[ni][nj]  # 标记为可通行或障碍物
        # print('discover',discovered)
        # print('step',step)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        indx_step=path.index(step)
        if indx_step!=0:
            stamina = stamina - 1  # 移动一步，消耗1点体力

        if stamina < 0:
            stamina = 0  # 确保体力不为负
        preposition=position
        position = step  # 更新当前位置

        visited.add(preposition)  # 标记为已访问
        # print(visited)
        # 发现当前位置周围的格子

        # 如果当前位置是未探索的可通行区域，得分加1
        if  step not in path_history :
            score += 1
        if position not in path_history:
            path_history.append(position)  # 记录路径

        print(path_history)
        # 可视化当前状态
        print_maze_pygame(screen, maze, discovered, path_history, position, score, stamina)
        clock.tick(5)  # 控制帧率为5帧每秒

    return position, stamina, score,preposition,path_history, visited   # 返回更新后的状态

# def move_along_path(maze, position, target, discovered, visited, path_history, stamina, score, clock, preposition):
#     # 使用已知迷宫信息寻找路径
#     path = astar_known_maze(maze_grid, maze, position, target, discovered, visited)
#     if path is None:
#         # 无法找到路径，回退到上一个位置
#         visited.discard(position)
#         if path_history and path_history[-1] == position:
#             path_history.pop()
#         position = preposition
#         return position, stamina, score, preposition, path_history
#
#     # 沿路径移动
#     for step in path[1:]:  # 跳过第一个元素，因为它是当前的位置
#         for dir in [(-1,0),(1,0),(0,-1),(0,1)]:
#             ni, nj = position[0] + dir[0], position[1] + dir[1]
#             if 0 <= ni < len(maze_grid) and 0 <= nj < len(maze_grid[0]):
#                 if (ni, nj) not in discovered:
#                     discovered[(ni, nj)] = maze[ni][nj]  # 更新已发现的格子
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#
#         # 更新位置和状态
#         preposition = position
#         position = step
#         stamina -= 1  # 消耗体力
#         if stamina < 0:
#             stamina = 0
#
#         visited.add(position)  # 标记为已访问
#
#         if position not in path_history:
#             score += 1  # 增加得分
#         path_history.append(position)
#
#         # 可视化当前状态
#         print_maze_pygame(screen, maze, discovered, path_history, position, score, stamina)
#         clock.tick(5)  # 控制帧率
#
#     return position, stamina, score, preposition, path_history

def main():
    """
    主函数，生成迷宫并开始模拟小人的移动。
    """
    # 生成迷宫并放置障碍物，障碍物数量为4
    maze, obstacles = generate_maze_with_obstacles(maze_grid, num_obstacles=15)
    print("随机生成的障碍物位置（隐藏）：", obstacles)  # 打印障碍物位置（可以隐藏以增加挑战性）
    simulate_movement_pygame(maze)  # 开始模拟移动

if __name__ == "__main__":
    main()  # 执行主函数
