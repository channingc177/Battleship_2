import pygame as pg
from sys import exit
from random import randint

# INTERPRETING SHIP IDs
# 1 = Patrol boat
# 2 = Cruiser
# 3 = Submarine
# 4 = Battleship
# 5 = Aircraft Carrier

class Ship:
    def __init__(self, ship_fleet = 0, ship_id = 1, active_game = None, ship_sunk = False):
        self.fleet = ship_fleet
        self.id = ship_id
        self.tags = []
        self.sunk = ship_sunk
        # setup tags
        if ship_id == 1:
            self.tags = [(0, 0), (0, 0)]
        elif ship_id == 2 or ship_id == 3:
            self.tags = [(0, 0), (0, 0), (0, 0)]
        elif ship_id == 4 or ship_id == 5:
            self.tags = []
            for i in range (1, ship_id + 1):
                self.tags.append((0, 0))
        # add ship to fleet data
        self.place_ship(active_game, ship_fleet)

    def place_ship(self, game_to_analyze, fleet_to_analyze):
        attempts = 100
        for i in range(0, attempts):
            target = (randint(1, 10), randint(1, 10))
            dir = randint(0, 1)
            execute = True
            self.set_tags(target, dir)
            for ship in game_to_analyze.fleets[fleet_to_analyze].ships:
                for other_tag in ship.tags:
                    for tag in self.tags:
                        if tag == other_tag:
                            execute = False
            if execute:
                break
        else:
            print(f"No suitable place was found in {attempts} tries. Be on guard for data errors!")
        

    def set_tags(self, ship_target = (1, 1), ship_direction = 0):
        self.tags[0] = ship_target
        if ship_direction == 0:
            for i in range(1, len(self.tags)):
                self.tags[i] = (ship_target[0], ship_target[1] + i)
        elif ship_direction == 1:
            for i in range(1, len(self.tags)):
                self.tags[i] = (ship_target[0] + i, ship_target[1])

class Fleet:
    def __init__(self, fleet_index = 0, fleet_defeated = False):
        self.ships = []
        self.defeated = fleet_defeated
        self.id = fleet_index
        self.bank = []
        
    def add_ships(self, num_ships = 5, running_game = None):
        for i in range(0, num_ships):
            self.ships.append(Ship(self.id, i + 1, running_game))

    def check_defeated(self):
        for ship in self.ships:
            if not ship.sunk:
                return False
        else:
            self.defeated = True
            return True

class Battleship:
    def __init__(self, fleet_num = 2):
        self.fleets = []
        for i in range(0, fleet_num):
            self.fleets.append(Fleet(i))
        for fleet in self.fleets:
            fleet.add_ships(5, self)
    
    def start_game(self):
        print("\n", "-" * 50, "Welcome to Bit Boats!", "-" * 50, "\nTake your turn to begin the game.\n")
        self.take_turn(0)
    
    def choose_target_fleet(self):
        user_in = int(input("Input index of fleet to target:"))
        if user_in + 1 > len(self.fleets):
            print("That fleet doesn't exist.")
            self.choose_target_fleet()
        else:
            print(f"Targeting fleet {user_in}.")
            return user_in

    def in_to_pair(self):
        user_in = input("--> ")
        if user_in == "":
            return ""
        # print(f"Accepted {user_in}.")
        let = user_in[0]
        num = int(user_in[1:])
        # print(f"converted to string {let} and int {num}.")
        return (ord(let) - 96, num)


    def take_turn(self, fleet_up_index = 0):
        active_fleet = self.fleets[fleet_up_index]
        shots = 0
        for ship in active_fleet.ships:
            if not ship.sunk:
                shots += 1
        targeted_fleet_index = self.choose_target_fleet()
        print("Input tag or [enter] to go back.")
        while shots > 0:
            target = self.in_to_pair()
            if target != "":
                result = self.check_shot(target, active_fleet, self.fleets[targeted_fleet_index])
                if result != 4 and result != 5:
                    shots -= 1
                self.interpret(result)
            else:
                targeted_fleet_index = self.choose_target_fleet()

    def interpret(self, num = 0):
        responses = ["Miss.", "Hit!", "Sunk!", "Ship sunk! Enemy fleet defeated!", "You already shot there, silly goose.", "This fleet is already defeated."]
        print(responses[num])

    def check_shot(self, shot = (1, 1), shooting_fleet = None, targeted_fleet = None):
        if targeted_fleet.defeated:
            return 5
        if shot in shooting_fleet.bank:
            return 4
        else:
            shooting_fleet.bank.append(shot)
            for ship in targeted_fleet.ships:
                for tag in ship.tags:
                    if tag == shot:
                        for tag2 in ship.tags:
                            if tag2 not in shooting_fleet.bank:
                                return 1
                        else:
                            ship.sunk = True
                            return 3 if targeted_fleet.check_defeated() else 2
            else:
                return 0

game = Battleship()
print(game.fleets[1].ships[0].tags)
game.start_game()
        

    # THIS METHOD NEEDS WORK. Currently, it is in R&D phase. 
    # def start_pg(self):
    #     print("Starting Pygame graphics window.")
    #     w, h, x, y = 800, 400, 100, 100
    #     pg.init()
    #     screen = pg.display.set_mode((w, h))
    #     pg.display.set_caption("Bit Boats")
    #     running = True

    #     while running:
    #         for event in pg.event.get():
    #             if event.type == pg.QUIT:
    #                 running = False
    #             if event.type == pg.KEYDOWN:
    #                 if event.key == pg.K_a:
    #                     x -= 20
    #                 elif event.key == pg.K_d:
    #                     x += 20
    #                 elif event.key == pg.K_w:
    #                     y -= 20
    #                 elif event.key == pg.K_s:
    #                     y += 20
            
    #         screen.fill((0, 75, 255))
    #         pg.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    #         pg.display.update()
    #     pg.quit()