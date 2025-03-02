import numpy as np

num_to_res = {
        0: "sheep",
        1: "wheat",
        2: "wood",
        3: "brick",
        4: "ore",
        5: "desert"
}

num_to_port = {
    0: "sheep",
    1: "wheat",
    2: "wood",
    3: "brick",
    4: "ore",
    5: "3-1"
}

num_to_dev = {
        0: "knight",
        1: "mono",
        2: "road_build",
        3: "double_res",
        4: "vp"
}


class Player:
    def __init__(self, id):
        self.id = id
        self.res = [0 for i in range(5)]
        self.res_count = 0
        self.dev_cards = [0 for i in range(5)]
        self.vps = 0
        self.long_road = 0
        self.army = 0


class Spot:
    def __init__(self, tiles=set(), edges=set(), port=set()):
        self.tiles = tiles
        self.edges = edges
        self.port = port


class Edge:
    def __init__(self, spots=set()):
        self.spots = spots


class Tile:
    def __init__(self, res=5, dots=set()):
        self.res = res
        self.dots = dots
        self.spots = set()


class CatanBoard:
    def __init__(self):
        # Store resource order for state
        resources = [
            0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5
        ]
        np.random.shuffle(resources)

        # Store points order for state
        dots = [
            2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12
        ]
        np.random.shuffle(dots)

        # Store ports order for state
        ports = [
            0, 1, 2, 3, 4, 5, 5, 5, 5
        ]
        np.random.shuffle(ports)

        # Tiles activated during a roll number
        self.roll_res = {}

        # Create Catan Resource Tiles
        self.tiles = [Tile()] * len(resources)
        j = 0
        i = 0
        for res in resources:
            if res != 5:
                self.tiles[i] = (Tile(dots[j], res))
                j += 1
            else:
                self.tiles[i] = (Tile(0, res))
            i += 1

        # Add spots to tiles
        self.tiles[0].spots = {0, 1, 2, 12, 13, 14}
        self.tiles[1].spots = {2, 3, 4, 10, 11, 12}
        self.tiles[2].spots = {4, 5, 6, 7, 9, 10}
        self.tiles[3].spots = {13, 14, 15, 16, 18, 19}
        self.tiles[4].spots = {11, 12, 13, 19, 20, 21}
        self.tiles[5].spots = {9, 10, 11, 21, 22, 23}
        self.tiles[6].spots = {7, 8, 9, 23, 24, 25}
        self.tiles[7].spots = {16, 17, 18, 35, 36, 37}
        self.tiles[8].spots = {18, 19, 20, 33, 34, 35}
        self.tiles[9].spots = {20, 21, 22, 31, 32, 33}
        self.tiles[10].spots = {22, 23, 24, 29, 30, 31}
        self.tiles[11].spots = {24, 25, 26, 27, 28, 29}
        self.tiles[12].spots = {34, 35, 36, 38, 39, 40}
        self.tiles[13].spots = {32, 33, 34, 40, 41, 42}
        self.tiles[14].spots = {30, 31, 32, 42, 43, 44}
        self.tiles[15].spots = {28, 29, 30, 44, 45, 46}
        self.tiles[16].spots = {39, 40, 41, 51, 52, 53}
        self.tiles[17].spots = {41, 42, 43, 49, 50, 52}
        self.tiles[18].spots = {43, 44, 45, 47, 48, 49}

        # Player with settle on each spot
        self.spot_owners = [0] * 54

        # Assign all spots tiles, ports, and edges
        self.spots = [Spot()] * len(self.spot_owners)
        self.spots[0] = Spot({0}, {0, 1})
        self.spots[1] = Spot({0}, {1, 2})
        self.spots[2] = Spot({0, 1}, {2, 3, 4}, {0})
        self.spots[3] = Spot({1}, {4, 5}, {0})
        self.spots[4] = Spot({1, 2}, {5, 6, 7})
        self.spots[5] = Spot({2}, {7, 8}, {1})
        self.spots[6] = Spot({2}, {8, 9}, {1})
        self.spots[7] = Spot({2, 6}, {9, 20, 21})
        self.spots[8] = Spot({6}, {21, 22}, {2})
        self.spots[9] = Spot({2, 5, 6}, {18, 19, 20})

        self.spots[10] = Spot({1, 2, 5}, {6, 17, 18})
        self.spots[11] = Spot({1, 4, 5}, {15, 16, 17})
        self.spots[12] = Spot({0, 1, 4}, {3, 14, 15})
        self.spots[13] = Spot({0, 3, 4}, {12, 13, 14})
        self.spots[14] = Spot({0, 3}, {0, 11, 12}, {8})
        self.spots[15] = Spot({3}, {10, 11}, {8})
        self.spots[16] = Spot({3, 7}, {10, 24, 25})
        self.spots[17] = Spot({7}, {23, 24}, {7})
        self.spots[18] = Spot({3, 7, 8}, {25, 26, 27})
        self.spots[19] = Spot({3, 4, 8}, {13, 27, 28})

        self.spots[20] = Spot({4, 8, 9}, {28, 29, 30})
        self.spots[21] = Spot({4, 5, 9}, {16, 30, 31})
        self.spots[22] = Spot({5, 9, 10}, {31, 32, 33})
        self.spots[23] = Spot({5, 6, 10}, {19, 33, 34})
        self.spots[24] = Spot({6, 10, 11}, {34, 35, 36})
        self.spots[25] = Spot({6, 11}, {22, 37}, {2})
        self.spots[26] = Spot({11}, {37, 38})
        self.spots[27] = Spot({11}, {38, 53})
        self.spots[28] = Spot({11, 15}, {51, 52, 53}, {3})
        self.spots[29] = Spot({10, 11, 15}, {35, 50, 51})

        self.spots[30] = Spot({10, 14, 15}, {48, 49, 50})
        self.spots[31] = Spot({9, 10, 14}, {32, 47, 48})
        self.spots[32] = Spot({9, 13, 14}, {45, 46, 47})
        self.spots[33] = Spot({8, 9, 13}, {29, 44, 45})
        self.spots[34] = Spot({8, 12, 13}, {42, 43, 44})
        self.spots[35] = Spot({7, 8, 12}, {26, 41, 42})
        self.spots[36] = Spot({7, 12}, {39, 40, 41})
        self.spots[37] = Spot({7}, {23, 39}, {7})
        self.spots[38] = Spot({12}, {40, 54}, {6})
        self.spots[39] = Spot({12, 16}, {54, 55, 56}, {6})

        self.spots[40] = Spot({12, 13, 16}, {43, 56, 57})
        self.spots[41] = Spot({13, 16, 17}, {57, 58, 59})
        self.spots[42] = Spot({13, 14, 17}, {46, 59, 60})
        self.spots[43] = Spot({14, 17, 18}, {60, 61, 62})
        self.spots[44] = Spot({14, 15, 18}, {49, 62, 63})
        self.spots[45] = Spot({15, 18}, {63, 64, 65})
        self.spots[46] = Spot({15}, {52, 65}, {3})
        self.spots[47] = Spot({18}, {64, 71}, {4})
        self.spots[48] = Spot({18}, {70, 71}, {4})
        self.spots[49] = Spot({17, 18}, {61, 69, 70})

        self.spots[50] = Spot({17}, {68, 69}, {5})
        self.spots[51] = Spot({16, 17}, {58, 67, 68}, {5})
        self.spots[52] = Spot({16}, {66, 67})
        self.spots[53] = Spot({16}, {55, 66})

        # Player with roads on each spot
        self.edge_owners = [0] * 72

        # Assign all edges spots
        self.edges = [Edge()] * len(self.edge_owners)
        self.edges[0] = Edge({0, 14})
        self.edges[1] = Edge({0, 1})
        self.edges[2] = Edge({1, 2})
        self.edges[3] = Edge({2, 12})
        self.edges[4] = Edge({2, 3})
        self.edges[5] = Edge({3, 4})
        self.edges[6] = Edge({4, 10})
        self.edges[7] = Edge({4, 5})
        self.edges[8] = Edge({5, 6})
        self.edges[9] = Edge({6, 7})

        self.edges[10] = Edge({15, 16})
        self.edges[11] = Edge({14, 15})
        self.edges[12] = Edge({13, 14})
        self.edges[13] = Edge({13, 19})
        self.edges[14] = Edge({12, 13})
        self.edges[15] = Edge({11, 12})
        self.edges[16] = Edge({11, 21})
        self.edges[17] = Edge({10, 11})
        self.edges[18] = Edge({9, 10})
        self.edges[19] = Edge({9, 23})

        self.edges[20] = Edge({7, 9})
        self.edges[21] = Edge({7, 8})
        self.edges[22] = Edge({8, 25})
        self.edges[23] = Edge({17, 37})
        self.edges[24] = Edge({16, 17})
        self.edges[25] = Edge({16, 18})
        self.edges[26] = Edge({18, 35})
        self.edges[27] = Edge({18, 19})
        self.edges[28] = Edge({19, 20})
        self.edges[29] = Edge({20, 33})

        self.edges[30] = Edge({20, 21})
        self.edges[31] = Edge({21, 22})
        self.edges[32] = Edge({22, 31})
        self.edges[33] = Edge({22, 23})
        self.edges[34] = Edge({23, 24})
        self.edges[35] = Edge({24, 29})
        self.edges[36] = Edge({24, 25})
        self.edges[37] = Edge({25, 26})
        self.edges[38] = Edge({26, 27})
        self.edges[39] = Edge({36, 37})

        self.edges[40] = Edge({36, 38})
        self.edges[41] = Edge({35, 36})
        self.edges[42] = Edge({34, 35})
        self.edges[43] = Edge({34, 40})
        self.edges[44] = Edge({33, 34})
        self.edges[45] = Edge({32, 33})
        self.edges[46] = Edge({32, 42})
        self.edges[47] = Edge({31, 32})
        self.edges[48] = Edge({30, 31})
        self.edges[49] = Edge({30, 44})

        self.edges[50] = Edge({29, 30})
        self.edges[51] = Edge({28, 29})
        self.edges[52] = Edge({28, 46})
        self.edges[53] = Edge({27, 28})
        self.edges[54] = Edge({38, 39})
        self.edges[55] = Edge({39, 53})
        self.edges[56] = Edge({39, 40})
        self.edges[57] = Edge({40, 41})
        self.edges[58] = Edge({41, 51})
        self.edges[59] = Edge({41, 42})

        self.edges[60] = Edge({42, 43})
        self.edges[61] = Edge({43, 49})
        self.edges[62] = Edge({43, 44})
        self.edges[63] = Edge({44, 45})
        self.edges[64] = Edge({45, 47})
        self.edges[65] = Edge({45, 46})
        self.edges[66] = Edge({52, 53})
        self.edges[67] = Edge({51, 52})
        self.edges[68] = Edge({50, 51})
        self.edges[69] = Edge({49, 50})

        self.edges[70] = Edge({48, 49})
        self.edges[71] = Edge({47, 48})

    def adj_spots(self, spot):
        adj = set()
        for edge in self.spots[spot].edges:
            for spot in self.edges[edge].spots:
                adj.add(spot)
        return adj

    def adj_empty(self, spot):
        adj_spots = self.adj_spots(spot)
        for spot in adj_spots:
            if self.spot_owners[spot] != 0:
                return False
        return True


class CatanGame:
    def __init__(self, num_players=4, rand=True):
        self.board = CatanBoard()

        # Initialize players and player stats
        self.player = 0
        self.num_players = num_players
        self.players = [Player(i) for i in range(self.num_players)]

        # Initialize tiles activated for rolls and spots associated with tiles
        self.dots_to_tile = {}
        self.tile_to_spot = {}

        # Reset flags before turn starts
        self.reset_flags()

        # Initialize robber position
        self.robber_pos = 0

        # Initialize tiles
        for i, tile in enumerate(self.board.tiles):
            # Set robber position to desert tile
            if tile.res == 5:
                self.robber_pos = i
                continue

            # Add tiles to their respective dots
            if tile.dots in self.dots_to_tile:
                self.dots_to_tile[tile.dots].add(i)
            else:
                self.dots_to_tile[tile.dots] = {i}

        # Initialize longest road, player needs at least 5 to have
        self.longest_road = 4
        self.longest_road_player = None

        # Initialize most knights, player needs at least 3 to have
        self.most_knights = 2
        self.most_knights_player = None

        # Create place order for placing settles
        place_order = np.concatenate((
            np.arange(self.num_players),
            np.arange(self.num_players)[::-1]
        ))

        # Assign spots on board randomly if random game
        if rand:
            num_placed = 0
            while num_placed < self.num_players * 2:
                self.player = place_order[num_placed]
                spot = np.random.randint(0, len(self.board.spot_owners))

                # Find a spot that is not adjacent or on an existing settle
                while (
                    self.board.spot_owners[spot] != 0 or
                    not self.board.adj_empty(spot)
                ):
                    spot = np.random.randint(0, len(self.board.spot_owners))
                self.settling = True
                self.place_settle_city(spot)

                # Place road on random edge of settle
                edges = self.board.spots[spot].edges
                edge = np.random.randint(0, len(edges))
                self.rbing = True
                self.place_road(list(edges)[edge])

                num_placed += 1
        # TODO need to add choosing settles

    def place_settle_city(self, spot):
        """
        Place settlement or city at selected location. Does not check if valid.
        Does not take resources.

        Params:
        spot (int): index of spot to place the settle
        """

        if self.settling:
            # Add settle to board and add in tile dict
            self.board.spot_owners[spot] = self.player + 1
            for tile in self.board.spots[spot].tiles:
                if tile in self.tile_to_spot:
                    self.tile_to_spot[tile].add(spot)
                else:
                    self.tile_to_spot[tile] = {spot}
            self.settling = False
        elif self.citying:
            self.board.spot_owners[spot] = self.player + 1 + self.num_players
            self.citying = False

        # Add VP for placing settle or city
        self.players[self.player].vps += 1

    def place_road(self, edge):
        """
        Place road at selected location. Does not check if valid.
        Does not take resources. Determines longest road.

        Params:
        edge (int): index of edge to place the road
        """
        self.board.edge_owners[edge] = self.player + 1

        def longest_road(cur_edge, vis_edge, vis_spot, length):
            """
            Determines longest road from specific edge.

            Params:
            cur_edge (int): index of current edge
            vis_edge (set): set of visited edges
            vis_spot (set): set of visited spots
            length (int): current total of length from root

            Returns:
            length (int): maximum length from current spot
            """
            if (
                cur_edge in vis_edge or
                self.board.edge_owners[cur_edge] != self.player + 1
            ):
                return length
            vis_edge.add(cur_edge)
            for spot in self.board.edges[cur_edge].spots:
                if (
                    spot not in vis_spot and
                    (
                        self.board.spots[spot] == 0 or
                        self.board.spots[spot] == self.player + 1
                    )
                ):
                    vis_spot.add(spot)
                    for e in self.board.spots[spot].edges:
                        length = max(
                            length,
                            longest_road(e, vis_edge, vis_spot, length + 1)
                        )
            return length

        # Update the longest road for player
        self.players[self.player].long_road = max(
            self.players[self.player].long_road,
            longest_road(edge, set(), set(), 0)
        )

        # Update VPs of player
        if self.players[self.player].long_road > self.longest_road:
            if self.longest_road_player is not None:
                self.players[self.longest_road_player - 1].vps -= 2
            self.players[self.player].vps += 2
            self.longest_road_player = self.player + 1

        self.rbing_roads -= 1
        self.rbing = False

    def move_robber(self, tile):
        """
        Moves the robber to a specific tile. Does not rob.

        Params:
        tile (int): index of tile to place robber

        Returns:
        players (set): set of players that can be robbed
        """
        # Update robber position
        self.robber_pos = tile

        # Find players to rob
        players = set()
        for spot in self.tile_to_spot[tile]:
            if (
                self.board.spot_owners[spot] != 0 and
                self.board.spot_owners[spot] != self.player + 1
            ):
                players.add(self.board.spot_owners[spot])
        return players

    def rob_player(self, player, robbee):
        """
        Player robs robbee.

        Params:
        player (int): player doing the robbing (1 to num_players)
        robbee (int): player getting robbed (1 to num_players)
        """
        # Rob from robbee and give to player (randomly)
        res_probs = np.array(
            self.players[robbee - 1].res
        ) / np.sum(self.players[robbee - 1])
        res_stolen = np.random.choice(range(5), p=res_probs)
        self.players[robbee - 1].res[res_stolen] -= 1
        self.players[player - 1].res[res_stolen] += 1

    def play_dev(self, card):
        """
        Plays a dev card at current game state.

        Params:
        card (int): index of card to play
        player (int): player to play card (1 to num_players)
        """
        # Remove card from player hand
        self.players[self.player].dev_cards[card] -= 1

        # Play card
        if card == 0:
            # Knight card
            self.robbing = True

            # Update number of knights for player
            self.players[self.player].knights += 1

            # Update VPs of player
            if self.players[self.player].knights > self.most_knights:
                if self.most_knights_player is not None:
                    self.players[self.most_knights_player - 1].vps -= 2
                self.players[self.player].vps += 2
        elif card == 1:
            # Road building
            self.rbing = True
            self.rbing_roads = 2
        elif card == 2:
            # Monopoly
            self.monoing = True
        elif card == 3:
            # Double Resource
            self.d_resing = True
            self.d_resing_res = 2
        self.played_dev = True

    def roll(self):
        """
        Roll the dice. Perform dice roll action
        """
        rolled_num = np.random.randint(1, 7) + np.random.randint(1, 7)
        if rolled_num == 7:
            self.robbing = True
        else:
            # For each spot adjacent to a tile
            for tile in self.dots_to_tile[rolled_num]:
                for spot in self.tile_to_spot[tile]:
                    owner = self.board.spot_owners[spot]
                    if owner != 0:
                        res = self.board.tiles[tile].res
                        num_res = ((owner - 1) // self.num_players) + 1
                        self.players[
                            (owner - 1) % self.num_players
                        ].res[res] += num_res
        self.rolled = True

    def buy(self, item):
        """
        Buy an item.

        Params:
        item (int): type of item to buy
        """
        if item == 0:
            # Buy a dev card
            self.players[self.player].res[0] -= 1
            self.players[self.player].res[1] -= 1
            self.players[self.player].res[4] -= 1
        elif item == 2:
            # Buy a road
            self.players[self.player].res[2] -= 1
            self.players[self.player].res[3] -= 1

            self.rbing = True
            self.rbing_roads = 1
        elif item == 3:
            # Buy a settle
            self.players[self.player].res[0] -= 1
            self.players[self.player].res[1] -= 1
            self.players[self.player].res[2] -= 1
            self.players[self.player].res[3] -= 1

            self.settling = True
        elif item == 3:
            # Buy a city
            self.players[self.player].res[1] -= 2
            self.players[self.player].res[4] -= 3

            self.citying = True

    def choose_res(self, res):
        """
        Choose a resource to mono, get from dev, or keep from rob.

        Params:
        choice (int): the resource to choose
        """
        if self.monoing:
            # Mono a resource
            for i in range(self.num_players):
                if i == self.player:
                    pass
                self.players[self.player].res[res] += self.players[i].res[res]
                self.players[i].res[res] = 0
                self.monoing = False
        elif self.d_resing_res > 0:
            # Get one of the double resources
            self.players[self.player].res[res] += 1
            self.d_resing_res -= 1
            self.d_resing = False
        elif self.num_card_rob > 0 or self.trading:
            # Choose resource to keep
            self.res = res

    def place_obj(self, place):
        """
        Place on tile, spot, or edge.

        Params:
        place (int): index of place to place object
        """
        if place in range(19):
            # Place robber
            self.move_robber(place)
            self.placed_robber = True
        elif place in range(19, 73):
            # Place settle or city
            spot = place - 19
            self.place_settle_city(spot)
        elif place in range(73, 145):
            # Place road
            edge = place - 73
            self.place_road(edge)

    def card_num(self, num_cards):
        """
        Performs action with number of cards.

        num_cards (int): number of cards to perform action with
        """
        if self.num_rob > 0:
            num_to_rob = min(
                min(self.num_rob, num_cards),
                self.players[self.player].res[self.res]
            )
            self.players[self.player].res[self.res] -= num_to_rob
            self.num_rob -= num_to_rob
        elif self.trading:
            print("ack trading")

    def reset_flags(self):
        """
        Reset all flags for new turn.
        """
        # Flag for rolling
        self.rolled = False

        # Flags for dev cards
        self.robbing = False
        self.placed_robber = False

        # Roads, settles, cities
        self.rbing = False
        self.settling = False
        self.citying = False

        # Number of roads that need to be built
        self.rbing_roads = 0

        # Mono and double resource
        self.monoing = False
        self.d_resing = False
        self.d_resing_res = 0

        # Played dev card
        self.played_dev = False

        # 7-roll keep
        self.num_rob = 0

        # Trading
        self.trading = False
        self.trader = 0

        # Selected Resource for trading and robbery
        self.res = 0

    def valid_actions(self):
        """
        Determine valid actions at current game state.

        Returns:
        actions (list): indicator list of possible actions
        """
        actions = [0] * (170 + self.num_players + 1)

        # Robbing or road building take precedence
        if self.robbing:
            actions.add("robbing")
        if self.rbing:
            actions.add("rbing")

        # Add ability to play dev card
        if not self.dev_played:
            actions.add("dev")

        # Add rolling
        if not self.rolled:
            actions[0] = 1
            return actions

    def take_action(self, action):
        """
        Take an action on current game state.

        Params:
        action (int): index of action to take
        """
        if action == 0:
            # Roll die
            self.roll()
        elif action == 1:
            # Trade
            self.trading = True
        elif action in range(2, 6):
            # Buy dev card, road, settle, or city
            item = action - 2
            self.buy(item)
        elif action in range(6, 10):
            # Play dev card
            card = action - 6
            self.play_dev(card)
        elif action in range(10, 15):
            # Choose resource (mono, double resource, 7-roll, trading)
            res = action - 10
            self.choose_res(res)
        elif action in range(15, 160):
            # Place object
            place = action - 15
            self.place_obj(place)
        elif action in range(160, 170):
            # Choose number of cards to trade, keep
            num_cards = action - 159
            self.card_num(num_cards)
        elif action == 170:
            # End turn
            self.player = (self.player + 1) % 4
            self.reset_flags()
        elif action in (170, 170 + self.num_players + 1):
            # Choose person for robbing or trading
            person = action - 170
            if self.robbing:
                self.rob_player(person)
                self.robbing = False
            elif self.trading:
                self.trader = person


if __name__ == "__main__":
    game = CatanGame()
    print("made")
