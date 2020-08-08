class Game():
    def __init__(self, game_id):
        self.p1_moved = False
        self.p2_moved = False
        self.game_rdy = False
        self.id = game_id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, player):
        '''
        :param player: [0, 1]
        :return: Move
        '''
        return self.moves[player]
        
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1_moved = True
        else:
            self.p2_moved = True

    def connected(self):
        return self.game_rdy

    def both_moved(self):
        return self.p1_moved and self.p2_moved

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        # check all options that are not a draw

        winner = -1
        if p1 == 'R' and p2 == 'P':
            winner = 1
        if p1 == 'R' and p2 == 'S':
            winner = 0
        if p1 == 'P' and p2 == 'R':
            winner = 0
        if p1 == 'P' and p2 == 'S':
            winner = 1
        if p1 == 'S' and p2 == 'R':
            winner = 1
        if p1 == 'S' and p2 == 'P':
            winner = 0

        return winner

    def reset(self):
        self.p1_moved = False
        self.p2_moved = False

        
            
