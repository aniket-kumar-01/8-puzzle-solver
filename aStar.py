# aStar.py
import json
import hashlib
import sys

PUZZLE_SIZE = 3

sys.setrecursionlimit(10000)  # Set a higher recursion limit (adjust as needed)


class Node:
    def __init__(self, parent, mat, empty_tile_pos, cost, level):
        self.parent = parent
        self.mat = mat
        self.empty_tile_pos = empty_tile_pos
        self.cost = cost
        self.level = level
        self.id = self.calculate_id()
    
    def calculate_id_hash(self):
        # Create a hash object using BLAKE2
        hash_object = hashlib.sha1()

        # Update the hash with the matrix, cost, and level
        hash_object.update(str(self.mat).encode('utf-8'))
        hash_object.update(str(self.cost).encode('utf-8'))
        hash_object.update(str(self.level).encode('utf-8'))

        # Get the hexadecimal digest of the hash and return it as the id
        sha256_hash = hash_object.hexdigest()

        # Convert the hexadecimal hash to a numeric value
        numeric_value = int(sha256_hash, 16)

        return sha256_hash
    
    def calculate_id(self):
        matrix = self.mat 
        id = "".join(str(col) for row in matrix for col in row)
        id = str(self.level) + id
        return id

    def __lt__(self, nxt):
        return self.cost < nxt.cost


def node_dict_generator(node_obj):
    label = ""
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            label+= str(node_obj.mat[i][j])

    label = label[:3]+"\n"+label[3:6] +"\n"+label[6:9]

    node_dict = {
        "id": node_obj.id,
        "parent_id": ((lambda: node_obj.parent.id, lambda: None)[node_obj.parent == None]()),
        "empty_tile_pos": node_obj.empty_tile_pos,
        "cost": node_obj.cost,
        "level": node_obj.level,
        # "mat": node_obj.mat,
        "label": label
    }
    return node_dict


def nodes_dict_list_generator(node_list: list):
    '''
    node_list: list of nodes,
    '''
    node_dicts_list = []
    for node_obj in node_list:
        node_dict = node_dict_generator(node_obj)
        node_dicts_list.append(node_dict)
    return node_dicts_list


def nodes_dicts_to_json(node_dicts: list, name):
    # nodes_json = json.dumps({"nodes": node_dicts}, indent=4)
    # print(nodes_json)
    name_split = name.split(".")
    if len(name_split) > 1:
        if name_split[-1] != 'json':
            name = name + ".json"

    with open(name, "w") as json_file:
        json.dump(node_dicts, json_file, indent=4)

    return node_dicts


def node_list_adder(old_node_list: list, node_list_to_add: list):
    for n in node_list_to_add:
        old_node_list.append(n)
    return old_node_list


def edge_gen_fx(all_nodes: list):
    return [{
        "from": node.parent.id,
        "to": node.id
    } for node in all_nodes if node.parent is not None]


def sol_node_gen_fx(sol_node: Node):
    node_lst = []
    while sol_node:
        node_lst.append(sol_node.id)
        sol_node = sol_node.parent
    return list(reversed(node_lst))


def color_adder(all_nodes:list,sol_node_ids:list):
    for n in all_nodes:
        if n["id"] in sol_node_ids:
            n["color"] = "#ccff33"

    return all_nodes

def generate_possible_moves(matrix, final_matrix, parent_node: Node, all_nodes: list):
    '''
    matrix - 3x3 matrix,
    parent_node - Node,
    node_json - dict type
    '''
    outcomes = []
    zero_row, zero_col = parent_node.empty_tile_pos

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        new_row, new_col = zero_row + dr, zero_col + dc

        if 0 <= new_row < PUZZLE_SIZE and 0 <= new_col < PUZZLE_SIZE:
            new_matrix = [row[:] for row in matrix]
            new_matrix[zero_row][zero_col], new_matrix[new_row][new_col] = new_matrix[new_row][new_col], new_matrix[zero_row][zero_col]
            empty_tile_pos = (new_row, new_col)

            # Check if the generated matrix is different from the parent matrix
            try:
                if new_matrix != parent_node.parent.mat:
                    cost = calculateCost(new_matrix, final_matrix)
                    new_node = Node(parent_node, new_matrix,
                                    empty_tile_pos, cost, parent_node.level + 1)
                    outcomes.append(new_node)
                    # all_nodes = nodes_dict_list_generator([new_node],all_nodes)
                    all_nodes = node_list_adder(all_nodes, [new_node])
            except:
                if new_matrix != parent_node.mat:
                    cost = calculateCost(new_matrix, final_matrix)
                    new_node = Node(parent_node, new_matrix,
                                    empty_tile_pos, cost, parent_node.level + 1)
                    outcomes.append(new_node)
                    # all_nodes = nodes_dict_list_generator([new_node],all_nodes)
                    all_nodes = node_list_adder(all_nodes, [new_node])

    return {"new_nodes": outcomes, "all_nodes": all_nodes}


def calculate_empty_tile_pos(matrix):
    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            if matrix[i][j] == 0:
                return (i, j)


def calculateCost(mat, final):
    n = len(mat)
    count = 0
    for i in range(n):
        for j in range(n):
            if mat[i][j] and mat[i][j] != final[i][j]:
                count += 1
    return count


def print_matrix(matrix):
    for row in matrix:
        print(row)
    print()


def min_cost_nodes_fx(base_nodes: list, final_matrix, all_nodes: list):

    # print("\n\n", '-'*40, "\n\n")

    # Find the minimum cost path from the final position to all other positions

    # for n in base_nodes:
    #     print(n, "Cost :", n.cost, "id :", n.id)
    #     print_matrix(n.mat)
    # print()

    min_cost = min(n.cost for n in base_nodes)

    # print("Min cost :", min_cost)
    # print()

    if (min_cost == 0):
        for n in base_nodes:
            if n.cost == 0:
                print("Solution found :",n)
                print("Cost:", n.cost)
                print("Number of moves:", n.level)
                return {"solution_node": n, "all_nodes": all_nodes}
        pass

    else:
        min_cost_nodes = (n for n in base_nodes if n.cost == min_cost)

        temp = []
        for n in min_cost_nodes:

            # print(n, n.cost)
            # print_matrix(n.mat)

            output_dict = generate_possible_moves(
                n.mat, final_matrix, n, all_nodes)
            temp_children = output_dict["new_nodes"]
            all_nodes = output_dict["all_nodes"]

            for child_node in temp_children:
                temp.append(child_node)

        # for min_n in temp:
        #     print(min_n, min_n.cost)

        return min_cost_nodes_fx(temp, final_matrix, all_nodes)


def solve(initial_matrix, final_matrix):
    cost = calculateCost(initial_matrix, final_matrix)
    initial_empty_tile_pos = calculate_empty_tile_pos(initial_matrix)
    initial_node = Node(None, initial_matrix,
                        initial_empty_tile_pos, cost, 0)

    return min_cost_nodes_fx([initial_node], final_matrix, [initial_node])


if __name__ == "__main__":
    # Example usage:
    initial_matrix = [
        [1, 2, 3],
        [0, 4, 6],
        [7, 5, 8]
    ]

    final_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    result = solve(initial_matrix, final_matrix)
    # print(result)
    solution_node = result["solution_node"]
    all_nodes = result["all_nodes"]
    print(solution_node)
    print(all_nodes)

    all_edges = edge_gen_fx(all_nodes)

    # Implement adding node_json dict in the solve function or min_cost_nodes_fx or generate all possible outcomes.
    nodes_dicts_to_json(nodes_dict_list_generator(all_nodes), "nodes.json")

    nodes_dicts_to_json(all_edges, "edges.json")
