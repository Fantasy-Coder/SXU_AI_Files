import numpy as np
import pulp
import random

# 高消费城市列表
HIGH_COST_CITIES = ["北京", "上海", "重庆", "天津", "深圳", "广州", "杭州"]

def calculate_ahp_weights(pairwise_matrix):
    """计算AHP权重及一致性比率"""
    col_sum = pairwise_matrix.sum(axis=0)
    norm_matrix = pairwise_matrix / col_sum
    weights = norm_matrix.mean(axis=1)
    eigval = np.linalg.eigvals(pairwise_matrix).real
    max_eigval = max(eigval)
    ci = (max_eigval - len(pairwise_matrix)) / (len(pairwise_matrix) - 1)
    ri_dict = {3: 0.58, 4: 0.90, 5: 1.12}
    ri = ri_dict.get(len(pairwise_matrix), 1.0)
    cr = ci / ri
    return weights, cr

def get_ahp_weights():
    print("\n===== AHP方法确定指标权重 =====")
    print("1=同等重要, 3=稍微重要, 5=明显重要, 7=强烈重要, 9=极端重要")
    matrix = np.ones((3, 3))
    matrix[0, 1] = float(input("消费 vs 舒适度 (1-9): "))
    matrix[1, 0] = 1 / matrix[0, 1]
    matrix[0, 2] = float(input("消费 vs 娱乐性 (1-9): "))
    matrix[2, 0] = 1 / matrix[0, 2]
    matrix[1, 2] = float(input("舒适度 vs 娱乐性 (1-9): "))
    matrix[2, 1] = 1 / matrix[1, 2]
    weights, cr = calculate_ahp_weights(matrix)
    print(f"AHP权重: 消费 {weights[0]:.2f}, 舒适度 {weights[1]:.2f}, 娱乐 {weights[2]:.2f}")
    if cr > 0.1:
        print("⚠️ 一致性比率较高，请重新评估判断矩阵")
        print("⚠️ 默认使用平衡权重: 消费 0.33, 舒适度 0.33, 娱乐 0.34")
        return [0.33, 0.33, 0.34]
    return weights

def calculate_total_cost(route, days_per_city, attractions_per_city, distances):
    total_cost = 0
    for i in range(len(route)-1):
        total_cost += distances[route[i]][route[i+1]] * 0.3
    for i, city in enumerate(route[1:-1]):
        days = days_per_city[i]
        if city in HIGH_COST_CITIES:
            total_cost += 250 * days + 200 * days
        else:
            total_cost += 150 * days + 100 * days
    total_cost += sum(attractions_per_city) * 50
    return total_cost

def calculate_comfort_score(route, days_per_city, start_temps):
    comfort_score = 0
    day_count = 0
    for i, city in enumerate(route[1:-1]):
        days = days_per_city[i]
        for d in range(days):
            temp = start_temps[city] + 0.5 * ((day_count + d) // 4)
            diff = max(0, temp - 28)
            comfort_score += max(0, 100 - diff * 2)
        day_count += days
    return (comfort_score / (day_count * 100)) * 100 if day_count > 0 else 0

def calculate_entertainment_score(attractions_per_city, max_days):
    return min(1.0, sum(attractions_per_city) / (2 * max_days)) * 100

def calculate_cost_score(cost, budget):
    return 100 if cost <= budget else max(0, 100 - (cost - budget) / 50)

def solve_fixed_all_visit(cities, distances, start_temps, max_days, budget, weights):
    n = len(cities)
    problem = pulp.LpProblem("Tourism_Optimized", pulp.LpMaximize)

    x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", cat='Binary') for i in range(n) for j in range(n) if i != j}
    u = {i: pulp.LpVariable(f"u_{i}", 1, n-1, cat='Integer') for i in range(1, n)}
    
    # 调整城市天数上限，引入城市类型差异
    avg_days = max_days // (n-2)
    min_days_limit = 1  # 降低最小天数要求到1天
    
    # 基于城市特性为不同城市分配不同的最大天数
    city_types = {}
    for i, city in enumerate(cities[1:-1]):
        # 基于城市特性确定类型: 1=小城市(偏低), 2=中等城市(适中), 3=大城市(偏高)
        if city in HIGH_COST_CITIES or distances[cities[0]][city] > 1000:
            city_types[i+1] = 3  # 大城市或远距离城市
        elif distances[cities[0]][city] > 600:
            city_types[i+1] = 2  # 中等城市
        else:
            city_types[i+1] = 1  # 小城市
    
    # 根据城市类型分配不同的最大天数
    max_days_per_city = {}
    for i in range(1, n-1):
        if city_types[i] == 3:  # 大城市
            max_days_per_city[i] = min(max_days, max(avg_days + 3, int(max_days * 0.5)))
        elif city_types[i] == 2:  # 中等城市
            max_days_per_city[i] = min(max_days, max(avg_days + 1, int(max_days * 0.35)))
        else:  # 小城市
            max_days_per_city[i] = min(max_days, max(avg_days - 1, int(max_days * 0.25)))
    
    # 创建城市天数和景点数变量，考虑城市类型
    days = {i: pulp.LpVariable(f"days_{i}", min_days_limit, max_days_per_city[i], cat='Integer') 
            for i in range(1, n-1)}
    
    # 针对城市类型的景点数上限
    attr_limits = {}
    for i in range(1, n-1):
        if city_types[i] == 3:  # 大城市景点多
            attr_limits[i] = min(3 * max_days_per_city[i], int(max_days * 0.6))
        elif city_types[i] == 2:  # 中等城市
            attr_limits[i] = min(2 * max_days_per_city[i], int(max_days * 0.4))
        else:  # 小城市景点少
            attr_limits[i] = min(2 * max_days_per_city[i], int(max_days * 0.3))
    
    attr = {i: pulp.LpVariable(f"attr_{i}", min_days_limit, attr_limits[i], cat='Integer') 
            for i in range(1, n-1)}
    visited = {i: pulp.LpVariable(f"visited_{i}", cat='Binary') for i in range(1, n-1)}

    # 保持原有约束
    # 起点出发一次，终点进入一次
    problem += pulp.lpSum(x[0, j] for j in range(1, n)) == 1
    problem += pulp.lpSum(x[i, n-1] for i in range(n-1)) == 1

    # 每个中间城市的流入流出平衡
    for j in range(1, n-1):
        incoming = pulp.lpSum(x[i, j] for i in range(n) if i != j)
        outgoing = pulp.lpSum(x[j, k] for k in range(n) if k != j)
        problem += incoming == visited[j]
        problem += outgoing == visited[j]
        problem += visited[j] == 1  # 强制经过所有中间城市
    
    # 修复子回路消除约束 - 使用MTZ公式
    for i in range(1, n-1):
        for j in range(1, n):
            if i != j:
                problem += u[i] - u[j] + n * x[i, j] <= n - 1
    
    # 确保起点到终点是连接的路径
    problem += pulp.lpSum(x[i, j] for i in range(n) for j in range(n) if i != j) == n - 1

    # 添加景点与天数的关联约束，考虑城市类型和旅游偏好
    for i in range(1, n - 1):
        # 基本约束：景点数不超过天数上限的2倍
        problem += attr[i] <= 2 * days[i]
        
        # 根据城市类型设置景点密度倾向 - 放宽约束
        if city_types[i] == 3:  # 大城市景点多
            problem += attr[i] >= 1.0 * days[i]  # 每天至少1个景点
        elif city_types[i] == 2:  # 中等城市
            problem += attr[i] >= 0.8 * days[i]  # 平均每天0.8个景点
        else:  # 小城市景点少
            problem += attr[i] >= 0.5 * days[i]  # 平均每天0.5个景点
    
    # 总天数约束
    total_days = pulp.lpSum(days[i] for i in range(1, n - 1))
    problem += total_days <= max_days
    
    # 天数分配约束 - 确保不同类型城市有不同的天数分配模式
    city_type_days = {}
    for t in range(1, 4):  # 1, 2, 3类型城市
        city_type_days[t] = pulp.lpSum(days[i] for i in range(1, n-1) 
                                      if city_types.get(i) == t)
    
    # 计算成本
    transport = pulp.lpSum(x[i, j] * distances[cities[i]][cities[j]] * 0.3 for (i, j) in x)
    lodge = pulp.lpSum(days[i] * (250 if cities[i] in HIGH_COST_CITIES else 150) for i in days)
    food = pulp.lpSum(days[i] * (200 if cities[i] in HIGH_COST_CITIES else 100) for i in days)
    scenic = pulp.lpSum(attr[i] * 50 for i in attr)
    cost = transport + lodge + food + scenic

    # 成本得分 - 允许超出预算，但惩罚更大
    cost_penalty = pulp.LpVariable("cost_penalty", 0)
    problem += cost_penalty >= (cost - budget) / 25  # 加大超出预算的惩罚
    score_cost = 100 - cost_penalty

    # 舒适度得分
    comfort = pulp.LpVariable("comfort", 0, 100)
    problem += comfort <= 100 - 1 * total_days

    # 娱乐性得分 
    entertain = pulp.lpSum(attr[i] for i in attr) / (2 * max_days) * 100

    # 天数分配的多样性调整 - 鼓励非平均分配
    city_1_bonus = pulp.LpVariable("city_1_bonus", 0, 50)  # 给特定城市额外奖励
    
    # 给第一个城市(西安)设置特殊权重，允许它有更多天数，但不要占据全部
    # 我们希望西安占据主要天数，但不要太极端
    i_special = 1  # 西安的索引
    problem += city_1_bonus <= days[i_special] * 3  # 西安每天有3分奖励  
    problem += days[i_special] >= 3  # 确保西安至少3天
    
    # 确保其他城市也有合理天数
    for i in range(1, n-1):
        if i != i_special:
            problem += days[i] >= 1  # 其他城市至少1天
    
    # 防止第一个城市占据所有天数的约束
    problem += days[i_special] <= max_days * 0.7  # 西安最多占总天数的70%
    
    # 目标函数：综合考虑多种因素，特别强调西安的重要性，但也确保其他城市有合理安排
    total_score = weights[0] * score_cost + weights[1] * comfort + weights[2] * entertain + city_1_bonus
    problem += total_score

    # 求解器设置 - 增加时间限制
    solver = pulp.PULP_CBC_CMD(msg=1, timeLimit=180)
    result = problem.solve(solver)

    print(f"\n[调试] 求解状态: {pulp.LpStatus[result]}")
    
    # 其余代码保持不变
    # ...
    
    if pulp.LpStatus[result] in ['Optimal', 'Feasible']:
        # 输出所有城市的访问状态
        print("\n[调试] 城市访问状态:")
        for i in range(1, n-1):
            print(f"城市 {cities[i]} (索引 {i}): visited = {pulp.value(visited[i])}")
        
        # 输出所有可能的路径选择
        print("\n[调试] 路径选择变量值:")
        for i in range(n):
            for j in range(n):
                if i != j and (i, j) in x and pulp.value(x[i, j]) > 0.01:
                    print(f"从 {cities[i]} 到 {cities[j]}: {pulp.value(x[i, j])}")

        path = [0]
        current = 0
        visited_nodes = set([0])
        
        print("\n[调试] 路径构建过程:")
        while current != n - 1:
            nexts = [j for j in range(n) if j != current and (current, j) in x and pulp.value(x[current, j]) > 0.5]
            print(f"当前节点: {cities[current]} (索引 {current}), 可能的下一节点: {[cities[j] for j in nexts]}")
            if not nexts:
                print(f"[警告] 在 {cities[current]} 没有找到下一个节点! 路径构建中断!")
                break
            current = nexts[0]
            print(f"选择下一节点: {cities[current]} (索引 {current})")
            path.append(current)
            visited_nodes.add(current)
            
        if path[-1] != n - 1:
            print(f"[警告] 路径未能正常到达终点! 强制添加终点 {cities[n-1]}")
            path.append(n - 1)
        
        print(f"\n[调试] 访问的节点: {visited_nodes}")
        print(f"[调试] 构建的路径: {path}")
        print(f"[调试] 对应城市: {[cities[i] for i in path]}")
        
        missed_cities = [cities[i] for i in range(1, n-1) if i not in visited_nodes]
        if missed_cities:
            print(f"\n[警告] 未经过的城市: {', '.join(missed_cities)}")
            print("[警告] 解决方案没有经过所有指定城市，尽管约束条件要求所有城市都必须经过!")

        route = [cities[i] for i in path]
        dlist = [int(pulp.value(days[i])) for i in path[1:-1]]
        alist = [int(pulp.value(attr[i])) for i in path[1:-1]]
        final_cost = calculate_total_cost(route, dlist, alist, distances)
        cscore = calculate_cost_score(final_cost, budget)
        comscore = calculate_comfort_score(route, dlist, start_temps)
        es = calculate_entertainment_score(alist, max_days)
        ts = weights[0] * cscore + weights[1] * comscore + weights[2] * es

        return {
            'route': route,
            'days_per_city': dlist,
            'attractions_per_city': alist,
            'total_cost': final_cost,
            'cost_score': cscore,
            'comfort_score': comscore,
            'entertainment_score': es,
            'total_score': ts
        }
    else:
        print(f"\n[错误] 无法找到可行解: {pulp.LpStatus[result]}")
        
        # 检查是否因为约束条件过于严格
        print("\n[调试] 检查可能的约束冲突:")
        if max_days < n - 2:
            print(f"[警告] 最大天数 ({max_days}) 小于城市数量 ({n-2})")
        
        # 检查预算是否充足
        min_costs = {}
        for i in range(1, n-1):
            min_transport = min([distances[cities[j]][cities[i]] * 0.3 for j in range(n) if j != i] + [1000000])
            daily_cost = (250 if cities[i] in HIGH_COST_CITIES else 150) + (200 if cities[i] in HIGH_COST_CITIES else 100)
            min_costs[cities[i]] = min_transport + daily_cost
        
        total_min_cost = sum(min_costs.values())
        if total_min_cost > budget:
            print(f"[警告] 可能的最小成本 ({total_min_cost}) 超出预算 ({budget})")
            print(f"城市最小成本估计: {min_costs}")
            
    return None


if __name__ == '__main__':
    cities = ["太原", "西安", "重庆", "北京", "威海", "运城"]
    start_temps = {"西安": 28.0, "重庆": 30.0, "北京": 29.0, "威海": 27.0}
    distances = {
        "太原": {"西安": 500, "重庆": 1050, "北京": 600, "威海": 1000, "运城": 400},
        "西安": {"重庆": 750, "北京": 1100, "威海": 1300, "运城": 500},
        "重庆": {"北京": 1700, "威海": 1800, "运城": 950},
        "北京": {"威海": 750, "运城": 1200},
        "威海": {"运城": 1500}
    }
    for c1 in list(distances.keys()):
        for c2 in list(distances[c1].keys()):
            if c2 not in distances:
                distances[c2] = {}
            if c1 not in distances[c2]:
                distances[c2][c1] = distances[c1][c2]

    max_days = 15
    budget = 5000
    weights = get_ahp_weights()

    result = solve_fixed_all_visit(cities, distances, start_temps, max_days, budget, weights)
    if result:
        print("\n✅ 最优旅游路线: ", ' -> '.join(result['route']))
        print("\n📌 各地安排:")
        for i, city in enumerate(result['route'][1:-1]):
            print(f"{city}: {result['days_per_city'][i]}天, {result['attractions_per_city'][i]}个景点")
        print(f"\n💰 总花费: {result['total_cost']:.2f}元")
        print(f"💵 消费得分: {result['cost_score']:.2f}")
        print(f"🌡️ 舒适度得分: {result['comfort_score']:.2f}")
        print(f"🎉 娱乐得分: {result['entertainment_score']:.2f}")
        print(f"📈 综合得分: {result['total_score']:.2f}")
    else:
        print("❌ 无法找到可行解，请检查输入参数")

def get_city_type(city, cities, distances):
    HIGH_COST_CITIES = ["北京", "上海", "重庆", "天津", "深圳", "广州", "杭州"]
    if city in HIGH_COST_CITIES or distances[cities[0]][city] > 1000:
        return 3
    elif distances[cities[0]][city] > 600:
        return 2
    else:
        return 1

def get_attr_limits(city, days, cities, distances):
    city_type = get_city_type(city, cities, distances)
    min_density = {3: 1.0, 2: 0.8, 1: 0.5}[city_type]
    min_attr = int(np.ceil(days * min_density))
    max_attr = 2 * days
    return min_attr, max_attr

def ga_fitness(individual, cities, distances, start_temps, max_days, budget, weights):
    route, days_per_city, attractions_per_city = individual
    # 约束检查
    if sum(days_per_city) > max_days or any(d < 1 for d in days_per_city):
        return -1e6
    # 景点约束检查
    for i, city in enumerate(route[1:-1]):
        min_attr, max_attr = get_attr_limits(city, days_per_city[i], cities, distances)
        if not (min_attr <= attractions_per_city[i] <= max_attr):
            return -1e6
    total_cost = calculate_total_cost(route, days_per_city, attractions_per_city, distances)
    cost_score = calculate_cost_score(total_cost, budget)
    comfort_score = calculate_comfort_score(route, days_per_city, start_temps)
    entertainment_score = calculate_entertainment_score(attractions_per_city, max_days)
    total_score = weights[0]*cost_score + weights[1]*comfort_score + weights[2]*entertainment_score
    return total_score

def ga_crossover(parent1, parent2, cities, distances):
    route1, days1, attr1 = parent1
    route2, days2, attr2 = parent2
    # 路线部分：部分映射交叉
    cut = random.randint(1, len(route1)-2)
    child_route = route1[:cut] + [c for c in route2 if c not in route1[:cut]]
    # 天数均匀交叉
    child_days = [random.choice([d1, d2]) for d1, d2 in zip(days1, days2)]
    # 景点数交叉后修正
    child_attr = []
    for i, city in enumerate(child_route[1:-1]):
        min_attr, max_attr = get_attr_limits(city, child_days[i], cities, distances)
        val = random.choice([attr1[i], attr2[i]])
        val = max(min_attr, min(max_attr, val))
        child_attr.append(val)
    return (child_route, child_days, child_attr)

def ga_mutate(individual, cities, distances):
    route, days, attr = individual
    # 路线变异：交换两个城市（不动首尾）
    idxs = list(range(1, len(route)-1))
    i, j = random.sample(idxs, 2)
    route = route[:]
    route[i], route[j] = route[j], route[i]
    # 天数和景点微调
    days = days[:]
    attr = attr[:]
    idx = random.randint(0, len(days)-1)
    days[idx] = max(1, days[idx] + random.choice([-1, 1]))
    # 修正景点数约束
    min_attr, max_attr = get_attr_limits(route[idx+1], days[idx], cities, distances)
    attr[idx] = max(min_attr, min(max_attr, attr[idx] + random.choice([-1, 1])))
    return (route, days, attr)

def genetic_algorithm(cities, distances, start_temps, max_days, budget, weights, pop_size=80, generations=150):
    mid_cities = cities[1:-1]
    population = []
    for _ in range(pop_size):
        route = [cities[0]] + random.sample(mid_cities, len(mid_cities)) + [cities[-1]]
        days = [random.randint(1, max_days//len(mid_cities)) for _ in mid_cities]
        attr = []
        for i, city in enumerate(route[1:-1]):
            min_attr, max_attr = get_attr_limits(city, days[i], cities, distances)
            attr.append(random.randint(min_attr, max_attr))
        population.append((route, days, attr))

    for gen in range(generations):
        fitnesses = [ga_fitness(ind, cities, distances, start_temps, max_days, budget, weights) for ind in population]
        # 选择
        selected = random.choices(population, weights=[max(f, 0.01) for f in fitnesses], k=pop_size)
        # 交叉和变异
        next_gen = []
        for i in range(0, pop_size, 2):
            child1 = ga_crossover(selected[i], selected[i+1], cities, distances)
            child2 = ga_crossover(selected[i+1], selected[i], cities, distances)
            if random.random() < 0.2:
                child1 = ga_mutate(child1, cities, distances)
            if random.random() < 0.2:
                child2 = ga_mutate(child2, cities, distances)
            next_gen.extend([child1, child2])
        population = next_gen[:pop_size]
    # 返回最优个体
    best = max(population, key=lambda ind: ga_fitness(ind, cities, distances, start_temps, max_days, budget, weights))
    return best

# ========== 遗传算法求解并输出 ==========
print("\n====== 遗传算法求解大规模旅游优化问题 ======")
best_route, best_days, best_attr = genetic_algorithm(cities, distances, start_temps, max_days, budget, weights)
final_cost = calculate_total_cost(best_route, best_days, best_attr, distances)
cscore = calculate_cost_score(final_cost, budget)
comscore = calculate_comfort_score(best_route, best_days, start_temps)
escore = calculate_entertainment_score(best_attr, max_days)
tscore = weights[0]*cscore + weights[1]*comscore + weights[2]*escore

print("\n✅ 遗传算法最优旅游路线: ", ' -> '.join(best_route))
print("\n📌 各地安排:")
for i, city in enumerate(best_route[1:-1]):
    print(f"{city}: {best_days[i]}天, {best_attr[i]}个景点")
print(f"\n💰 总花费: {final_cost:.2f}元")
print(f"💵 消费得分: {cscore:.2f}")
print(f"🌡️ 舒适度得分: {comscore:.2f}")
print(f"🎉 娱乐得分: {escore:.2f}")
print(f"📈 综合得分: {tscore:.2f}")