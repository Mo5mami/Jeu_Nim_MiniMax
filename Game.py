from MiniMaxTree import MiniMaxTreeAlphaBeta
#from MiniMaxTreeSafe import MiniMaxTree
from MiniMaxTree import MiniMaxTree
#from MiniMaxTreeAlphaBeta import MiniMaxTreeAlphaBeta


class Game:
    def __init__(self):
        self.number_of_sticks = None
        self.is_play_first = None
        self.tree = None
        self.current_player = None
        

    def __call__(self):
        self.show_title()
        self.show_insert_number_of_stick()
        self.show_turn_choice()
        self.creating_tree()
        current_node = self.tree.tree[0]
        while not current_node.is_leaf:
            if not self.available_moving_point(current_node):
                break
            if self.current_player:
                current_node = self.get_human_moving_choice(current_node)
            else:
                current_node = self.get_comp_moving_choice(current_node)
            self.current_player = not self.current_player
            print("---------------------------------------------------\n\n")
        print("\n---------------------------------------------------\n\n")
        self.show_winner()
        self.show_rendered_tree()

    def available_moving_point(self, current_node):
        print("---------------------------------------------------")
        print(("\t\t(^_^)/ Humain" if self.current_player else "\t     ['-']/ IA") + " Tour")
        print("---------------------------------------------------")
        print("Choix valable")
        count_child = 0
        for child in current_node.children:
            if child.is_leaf:
                print("\nPas de choix valable ", end="")
                return False
            else:
                print(str(count_child + 1) + ". [" + ("-".join(map(str, child.node_value)))+"]")
            count_child += 1
        print("")
        return True

    def get_comp_moving_choice(self, current_node):
        choice_child = self.check_comp_moving_choice(current_node)
        current_child = 0
        for child in current_node.children:
            if current_child == choice_child:
                print("Choix IA\t: [" + ("-".join(map(str, child.node_value)))+"]")
                return child
            current_child += 1
        print("---------------------------------------------------")

    def check_comp_moving_choice(self, current_node):
        child_choice = 0
        for child in current_node.children:
            if child.evaluator_value == 1:
                return child_choice
            child_choice += 1
        return child_choice / child_choice - 1

    def get_human_moving_choice(self, current_node):
        while True:
            count_child = 0
            moving_choice = int(input("Choisir\t: "))
            for child in current_node.children:
                if moving_choice - 1 == count_child:
                    print("Choix\t\t: [" + ("-".join(map(str, child.node_value))) + "]")
                    return child
                count_child += 1
            print("Invalide \n")

    def show_title(self):
        print("\t -------------------------------")
        print("\t|           Jeu de NIM         |")
        print("\t -------------------------------\n\n")

    def show_insert_number_of_stick(self):
        print("---------------------------------------------------")
        while True:
            self.number_of_sticks = int(input("Inserer le nombre de sticks\t: "))
            if self.number_of_sticks % 2 != 0 and self.number_of_sticks != 1:
                break
            print("doit etre impaire et pas 1.\n")
        print("---------------------------------------------------\n\n")

    def show_turn_choice(self):
        print("---------------------------------------------------")
        print("\t\t  Premier joueur")
        print("---------------------------------------------------")
        self.is_play_first = int(input("1. Humain\n2. IA\n\nDonner votre choix\t: "))
        self.is_play_first = True if self.is_play_first == 1 else False
        print("---------------------------------------------------\n\n")

    def creating_tree(self):
        print("---------------------------------------------------")
        print("Creation arbre minimax....")
        #self.tree = MiniMaxTree(self.number_of_sticks, self.is_play_first)
        self.tree_alpha_beta = MiniMaxTreeAlphaBeta(self.number_of_sticks, self.is_play_first)
        self.tree = MiniMaxTree(self.number_of_sticks, self.is_play_first)
        print("Arbre cree")
        self.current_player = self.tree.first_player
        print("---------------------------------------------------\n\n")

    def show_rendered_tree(self):
        print("---------------------------------------------------")
        print(f"AVEC alpha beta : {self.tree_alpha_beta}")
        print(f"Sans alpha beta : {self.tree}")
        print("---------------------------------------------------")
        is_show_tree = input("afficher les arbres MiniMax [o/n]? ")
        
        if is_show_tree == "o" or is_show_tree == "O":
            print("---------------------------------------------------")
            print("------------arbre avec alpha beta------------------")
            print("---------------------------------------------------")
            print(self.tree_alpha_beta.get_tree())
        print("---------------------------------------------------\n\n")
        if is_show_tree == "o" or is_show_tree == "O":
            print("---------------------------------------------------")
            print("------------arbre sans alpha beta------------------")
            print("---------------------------------------------------")
            print(self.tree.get_tree())
        print("---------------------------------------------------\n\n")

    def show_winner(self):
        print("---------------------------------------------------")
        print(("\t    Humain   " if not self.current_player else "\tIA   ") + "GAGNE !")
        self.current_player = not self.current_player
        print(("\t    Humain   " if not self.current_player else "\tIA   ") + "PERD !")
        print("---------------------------------------------------\n\n")

if __name__ == '__main__':
    game=Game()
    game()
