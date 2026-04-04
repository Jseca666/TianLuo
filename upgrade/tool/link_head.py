import numpy as np

def calculate_distance(p1, p2):
    """计算两个点的欧几里得距离"""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def merge_close_matches(matches, distance_threshold=20):
    """
    将相近的坐标取均值合并
    :param matches: 匹配点列表 [(x1, y1), (x2, y2), ...]
    :param distance_threshold: 距离阈值，小于该阈值的点将被合并
    :return: 合并后的坐标列表
    """
    if not matches:
        return matches

    # 保存合并后的结果
    merged_matches = []

    # 遍历每个匹配点
    for match in matches:
        merged = False
        for i, existing_match in enumerate(merged_matches):
            # 计算与已合并的点的距离
            if calculate_distance(match, existing_match) < distance_threshold:
                # 如果距离小于阈值，则合并，取均值
                merged_matches[i] = tuple((np.array(existing_match) + np.array(match)) / 2)
                merged = True
                break
        if not merged:
            # 如果没有合并到已有点，添加为新的独立点
            merged_matches.append(match)
    merged_matches = [tuple(map(int, match)) for match in merged_matches]
    return merged_matches

# # 示例匹配点
# matches = [(150, 300),(151,300), (152, 302), (450, 500), (455, 505), (750,701),(750, 700)]
#
# # 执行合并操作
# merged_matches = merge_close_matches(matches, distance_threshold=10)
#
# print("合并后的匹配点:", merged_matches)
