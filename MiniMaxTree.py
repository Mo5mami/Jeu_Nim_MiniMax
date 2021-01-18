from anytree import Node, RenderTree, findall,PreOrderIter
from anytree.dotexport import RenderTreeGraph

infinity=int(1e6)

class MiniMaxTree(object):
    def __init__(self, root_value, first_player):
        self.root_value = root_value
        self.first_player = first_player  # first_player: True = Human, False = Computer
        self.tree = [Node(0, node_value=[self.root_value], is_final=False, evaluator_value=None)]
        self.render_tree()
        self.len=1

    def render_tree(self):
        current_state, check_state = 0, True
        while check_state:
            count_final = 0
            for node in findall(self.tree[0], filter_=lambda n: n.depth == current_state):
                if not node.is_final:
                    for list_ in self.set_all_child(node):
                        self.tree.append(Node(len(self.tree), parent=self.tree[node.name],
                                              node_value=list_[0], is_final=True if list_[1] == 1 else False,
                                              evaluator_value=None))
                else:
                    count_final += 1
                if count_final == self.count_siblings(current_state):
                    check_state = False
            current_state += 1
        self.search( self.tree[0], self.first_player, 0)
        

    def set_all_child(self, node):
        result_list = []
        if max(node.node_value) == 2:
            result_list.append([self.set_child_value(node.node_value, 2, 1), 1])
            
        else:
            for value in node.node_value:
                number_of_children = self.count_children(value)
                if value > 2:
                    for i in range(number_of_children):
                        result=self.set_child_value(node.node_value, value, i + 1)
                        test=max(result)<=2
                        result_list.append([result, 0])
        return self.check_duplicate(result_list)

    def count_children(self, current_value):
        return (int(current_value / 2) - 1) if current_value % 2 == 0 else int(current_value / 2)

    def check_duplicate(self, list_):
        result_list = []
        for value in list_:
            if value not in result_list:
                result_list.append(value)
        return result_list

    def set_child_value(self, list_, current_value, deduction):
        result_list = []
        is_already_split = True
        for value in list_:
            if value == current_value and is_already_split:
                result_list.append(current_value - deduction)
                result_list.append(deduction)
                is_already_split = False
            else:
                result_list.append(value)
        
        return result_list

    
    def count_siblings(self, current_state):
        return len(findall(self.tree[0], filter_=lambda n: n.depth == current_state))

    def get_tree(self):
        return RenderTree(self.tree[0]).by_attr(lambda n: ("-".join(map(str, n.node_value)) +
                                                           "  [" + str(n.evaluator_value) + "]"))

    def get_tree_height(self):
        return self.tree[0].height


    def terminal_test(self,node):
        return node.is_leaf

    def utility(self, node, current_player, current_state):
        if node.is_final and current_state % 2 == 0:
            node.evaluator_value=-1 if current_player else 1
            
        elif node.is_final and current_state % 2 != 0:
            node.evaluator_value= 1 if not current_player else -1
        return node.evaluator_value

    def actions(self,node):
        return node.children

    def search(self, node, current_player, current_state):

        def max_value(node,player,state,):
            if self.terminal_test(node):
                return self.utility(node, player, state)
            v = -infinity
            for child in self.actions(node):
                v = max(v, min_value(child,not player,state+1))
                node.evaluator_value=v
            return v

        def min_value(node,player,state,):
            if self.terminal_test(node):
                return self.utility(node, player, state)
            v = infinity
            for child in self.actions(node):
                v = min(v, max_value(child,not player,state+1))
                node.evaluator_value=v
            return v

        #return max_value(node,current_player,current_state)
        if not current_player:
            return max_value(node,current_player,current_state,)
        else :
            return min_value(node,current_player,current_state,) 

    def filter_none(self,node):
        return findall(self.tree[0], filter_=lambda n: n.evaluator_value is not None)

    def __len__(self):
        return len(self.filter_none(self.tree[0]))

    def __str__(self):
        return f"nombre de noeuds total: " + str(self.__len__())






class MiniMaxTreeAlphaBeta(MiniMaxTree):

    def search(self, node, current_player, current_state):

        def max_value(node,player,state, alpha, beta):
            if self.terminal_test(node):
                return self.utility(node, player, state)
            v = -infinity
            for child in self.actions(node):
                v = max(v, min_value(child,not player,state+1, alpha, beta))
                node.evaluator_value=v
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(node,player,state, alpha, beta):
            if self.terminal_test(node):
                return self.utility(node, player, state)
                
            v = infinity
            for child in self.actions(node):
                v = min(v, max_value(child,not player,state+1, alpha, beta))
                node.evaluator_value=v
                if v <= alpha:
                    return v
                
                beta = min(beta, v)
            return v

        if not current_player:
            return max_value(node,current_player,current_state,-infinity,infinity)
        else :
            return min_value(node,current_player,current_state,-infinity,infinity) 