import random
import math



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



def chess(first_move, carlsen_strength, caruana_strength):
    carlsen_score = 0
    caruana_score = 0
    draws = 0
    
    for game in range(1, 5):
        if game % 2 == 1:
            if first_move == 0:
                max_player = "Magnus Carlsen"
                min_player = "Fabiano Caruana"
                maxV = carlsen_strength
                minV = caruana_strength
            else:
                max_player = "Fabiano Caruana"
                min_player = "Magnus Carlsen"
                maxV = caruana_strength
                minV = carlsen_strength
        else:
            if first_move == 0:
                max_player = "Fabiano Caruana"
                min_player = "Magnus Carlsen"
                maxV = caruana_strength
                minV = carlsen_strength
            else:
                max_player = "Magnus Carlsen"
                min_player = "Fabiano Caruana"
                maxV = carlsen_strength
                minV = caruana_strength
        
        leaf_nodes = leaf_node_generator(maxV, minV)
        tree = [None, None, None, 'max']
        create_tree(leaf_nodes, tree, leaf_depth = 5)
        
        result = alpha_beta_pruning(tree)
        
        if result > 0:
            winner = max_player
            winner_role = "Max"
            if winner == "Magnus Carlsen":
                carlsen_score += 1
            else:
                caruana_score += 1
        elif result < 0:
            winner = min_player
            winner_role = "Min"
            if winner == "Magnus Carlsen":
                carlsen_score += 1
            else:
                caruana_score += 1
        else:
            winner = "Draw"
            winner_role = ""
            draws += 1
        
        print(f"Game {game} Winner: {winner} ({winner_role}) (Utility value: {result})")
    
    print("\nOverall results:")
    print(f"Magnus Carlsen Wins: {carlsen_score}")
    print(f"Fabiano Caruana Wins: {caruana_score}")
    print(f"Draws: {draws}")
    
    if carlsen_score > caruana_score:
        overall_winner = "Magnus Carlsen"
    elif caruana_score > carlsen_score:
        overall_winner = "Fabiano Caruana"
    else:
        overall_winner = "Draw"
    print(f"Overall winner: {overall_winner}")






#Driver Code
first_move = int(input("Enter starting player for game 1 (0 for Carlsen, 1 for Caruana): "))
carlsen_strength = int(input("Enter base strength for Carlsen: "))
caruana_strength = int(input("Enter base strength for Caruana: "))

chess(first_move, carlsen_strength, caruana_strength)
