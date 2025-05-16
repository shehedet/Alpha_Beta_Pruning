import math
import random

def utility_function(maxV, minV):
    strength_maxV = math.log2(maxV + 1) + (maxV / 10)
    strength_minV = math.log2(minV + 1) + (minV / 10)
    i = random.randint(0, 1)
    utility = strength_maxV - strength_minV + ((-1) ** i) * (random.randint(1, 10) / 10)

    return round(utility, 3)



def leaf_node_generator(maxV, minV):
    leaf_nodes = []
    for i in range(32):
        leaf_nodes.append(utility_function(maxV, minV))
        
    return leaf_nodes



def create_tree(leaf_nodes, tree, leaf_depth, current_depth = 1):
    if current_depth % 2 == 0:
        position = 'min'
    else:
        position = 'max'
    
    if current_depth == leaf_depth:
        tree[1] = [leaf_nodes[0], None, None, position]
        tree[2] = [leaf_nodes[1], None, None, position]
        leaf_nodes.pop(0)
        leaf_nodes.pop(0)
    else:
        tree[1] = [None, None, None, position]
        tree[2] = [None, None, None, position]
        create_tree(leaf_nodes, tree[1], leaf_depth, current_depth + 1)
        create_tree(leaf_nodes, tree[2], leaf_depth, current_depth + 1)
    
    return tree



def create_tree_for_mind_control(leaf_nodes, tree, leaf_depth, current_depth = 1):
    position = 'max'
    
    if current_depth == leaf_depth:
        tree[1] = [leaf_nodes[0], None, None, position]
        tree[2] = [leaf_nodes[1], None, None, position]
        leaf_nodes.pop(0)
        leaf_nodes.pop(0)
    else:
        tree[1] = [None, None, None, position]
        tree[2] = [None, None, None, position]
        create_tree_for_mind_control(leaf_nodes, tree[1], leaf_depth, current_depth + 1)
        create_tree_for_mind_control(leaf_nodes, tree[2], leaf_depth, current_depth + 1)
    
    return tree



def alpha_beta_pruning(tree, alpha = -math.inf, beta = math.inf):
    if tree[0] != None:
        return tree[0]
    
    position = tree[3]

    if position == 'max':
        value = -math.inf
        left_value = alpha_beta_pruning(tree[1], alpha, beta)
        value = max(value, left_value)
        alpha = max(alpha, value)
        if alpha >= beta:
            return value
        right_value = alpha_beta_pruning(tree[2], alpha, beta)
        value = max(value, right_value)
        alpha = max(alpha, value)

        return value
    else:
        value = math.inf
        left_value = alpha_beta_pruning(tree[1], alpha, beta)
        value = min(value, left_value)
        beta = min(beta, value)
        if alpha >= beta:
            return value
        right_value = alpha_beta_pruning(tree[2], alpha, beta)
        value = min(value, right_value)
        beta = min(beta, value)

        return value
    


def chess(first_move, mind_control_cost, light_strength, l_strength):
    if first_move == 0:
        max_player = 'Light'
        maxV = light_strength
        minV = l_strength
    else:
        max_player = 'L'
        maxV = l_strength
        minV = light_strength
    
    leaf_nodes1 = leaf_node_generator(maxV, minV)
    leaf_nodes2 = leaf_nodes1.copy()
    tree = [None, None, None, 'max']
    tree_for_mind_control = [None, None, None, 'max']
    create_tree(leaf_nodes1, tree, leaf_depth = 5)
    create_tree_for_mind_control(leaf_nodes2, tree_for_mind_control, leaf_depth = 5)
    
    minimax_without_mind_control = alpha_beta_pruning(tree)
    minimax_with_mind_control = alpha_beta_pruning(tree_for_mind_control)
    after_cost = round(minimax_with_mind_control - mind_control_cost, 3)

    print(f'Minimax value without Mind Control: {minimax_without_mind_control}')
    print(f'Minimax Value with Mind Control: {minimax_with_mind_control}')
    print(f'Minimax value with Mind Control after incurring the cost: {after_cost}\n')

    if minimax_without_mind_control > 0 and after_cost > 0:
        print(f"{max_player} should NOT use Mind Control as the position is already winning.")
    elif minimax_without_mind_control > 0 and after_cost < 0:
        print(f"{max_player} should NOT use Mind Control as it backfires.")
    elif minimax_without_mind_control < 0 and after_cost > 0:
        print(f"{max_player} should use Mind Control.")
    elif minimax_without_mind_control < 0 and after_cost < 0:
        print(f"{max_player} should NOT use Mind Control as the position is losing either way.")



first_move = int(input("Enter who goes first (0 for Light, 1 for L): "))
mind_control_cost = float(input("Enter the cost of using Mind Control: "))
light_strength = int(input("Enter base strength for Light: "))
l_strength = int(input("Enter base strength for L: "))

chess(first_move, mind_control_cost, light_strength, l_strength)
