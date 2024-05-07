import pygame
import math
import sys
pygame.init()
WIDTH, HEIGHT = 900, 900
FPS = 60
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
keys_pressed = [0, 0]
rect = [600, -30, 30, 30]
pressed_down = False
enemy = pygame.image.load('data/images/enemy.png').convert_alpha()
pygame.mixer.music.load('data/images/no-copyright-music-181373.mp3')
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1)
font = pygame.font.SysFont('Cambria', 110)
small = pygame.font.SysFont('Cambria', 50)
smaller = pygame.font.SysFont('Cambria', 20)


def quit():
    sys.exit()
    
class Ballons:
    def __init__(self, strength):
        self.strength = strength
        self.rect = [560, 0]
        self.rects = pygame.Rect(self.rect[0], self.rect[1], 30, 30)
        self.keys_pressed = [1, 0]
        self.adder = 1
        self.num_waypoints = 3
        self.waypoint = [
            [560, 800]
        ]
        self.color = [0, 0, 255]
        self.time = 1
        self.i = 0
    def ballpos(self):
        return self.rect[:2]
    def move_checker(self):
        if self.rect[1] + self.keys_pressed[0]*self.adder == self.waypoint[0][1]:
            self.keys_pressed[0] = 0
            self.keys_pressed[1] = -1


    def remove_layer(self, pierce):
        self.strength -= pierce

    def move(self):
        self.move_checker()
        self.rect[1] += self.keys_pressed[0] * self.adder
        self.rect[0] += self.keys_pressed[1] * self.adder
        self.rects.y += self.keys_pressed[0] * self.adder
        self.rects.x += self.keys_pressed[1] * self.adder
        self.time += 1
    def draw(self):
        if self.time % 15 == 0:
            self.i += 1
            if self.i >= 4:
                self.i = 0
        window.blit(enemy, self.rect, ((self.i*96)+29, 103, 50, 57))

class Mechas:
    player = pygame.image.load('data/images/player1.png').convert_alpha()
    player_light = pygame.image.load('data/images/playerlight.png').convert_alpha()
    player_med = pygame.image.load('data/images/player.png').convert_alpha()
    bullet = pygame.image.load('data/images/bullet.png').convert_alpha()
    def __init__(self, name, pos, ball_pos, slow):
        self.name = name
        self.pos = pos
        self.ball_pos = ball_pos
        self.bullet_rect = pygame.Rect(pos[0]+15, pos[1]+40, 10, 10)
        self.storer = [pos[0], pos[1]]
        self.storrect = pygame.Rect(pos[0], pos[1], 60, 60)
        self.own_rect = [pos[0]+15, pos[1]+40]
        self.color = (255, 255, 255)
        self.hit = False
        self.can_shoot = False
        self.slow = slow
        self.carry = slow
        self.pierce = 1
        if self.name == "Light":
            self.color = (0, 255, 0)
            self.shooting_radius = 200
            self.player1 = self.player_light
        elif self.name == "Medium":
            self.color = (255, 0, 0)
            self.shooting_radius = 300
            self.player1 = self.player_med
        elif self.name == "Heavy":
            self.color = (0, 0, 255)
            self.shooting_radius = 400
            self.player1 = self.player
        self.time = 1
        self.i = 0

    def hitter(self):
        self.bullet_rect.x, self.bullet_rect.y = self.own_rect[0], self.own_rect[1]


    def shoot(self, ball_pos):
        self.y2_y1 = (ball_pos[1] - self.bullet_rect.y)
        self.x2_x1 = -(ball_pos[0] - self.bullet_rect.x)
        if self.slow == 0:
            self.can_shoot = True
        distance = math.sqrt((self.x2_x1)**2+(self.y2_y1)**2)
        if ball_pos[1] >= 40 and self.can_shoot and distance <= self.shooting_radius:
            if self.x2_x1 == 0:
                self.slope = 0
            else:
                self.slope = self.y2_y1/self.x2_x1
                self.carrier = self.slope
            if self.slope > 0:
                if self.x2_x1 <= 0:
                    self.bullet_rect.x += 5
                elif self.x2_x1 >= 0:
                    self.bullet_rect.x -= 5
                if self.y2_y1 <= 0:
                    self.bullet_rect.y -= self.slope * 5
                elif self.y2_y1 >= 0:
                    self.bullet_rect.y += self.slope * 5
            elif self.slope <= 0:
                if self.x2_x1 < 0:
                    self.bullet_rect.x += 5
                elif self.x2_x1 >= 0:
                    self.bullet_rect.x -= 5
                if self.y2_y1 <= 0:
                    self.bullet_rect.y += self.slope * 5
                elif self.y2_y1 >= 0:
                    self.bullet_rect.y -= self.slope * 5
            self.slow = self.carry
        self.slow -= 1

    def frames(self):
        self.time += 1
        if self.time % 15 == 0:
            self.i += 1
            if self.i >= 4:
                self.i = 0
    def draw(self):
        self.frames()
        pygame.draw.rect(window, (0, 255, 255), self.bullet_rect)
        window.blit(self.player1, self.storer, ((self.i*96)+26, 416, 64, 63))

def placing_units(name, heavy, medium, light, pos):
    if name == "Light":
        window.blit(light, pos, (32, 50, 32, 45))
        pygame.draw.circle(window, (255, 255, 255), pos, 200, 1)
    elif name == "Medium":
        window.blit(medium, pos, (32, 50, 32, 45))
        pygame.draw.circle(window, (255, 255, 255), pos, 300, 1)
    elif name == "Heavy":
        window.blit(heavy, pos, (32, 50, 32, 45))
        pygame.draw.circle(window, (255, 255, 255), pos, 400, 1)

def checkers(leveler, lives):
    if leveler > 10 or lives <= 0:
        run = True
        text = font.render('Thanks for Playing!', True, (255, 255, 255))
        while run:
            window.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            window.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2))
            pygame.display.update()

def upgrade(mecha, money):
    running = True
    Factor = 3
    reload_image = pygame.image.load('data/images/player1.png').convert_alpha()
    reload_image = pygame.transform.scale_by(reload_image, Factor)
    reload = smaller.render("Increase reload speed", True, (255, 255, 255))
    bullet = pygame.image.load('data/images/bullet.png').convert_alpha()
    bullet = pygame.transform.scale_by(bullet, 0.30)
    test = small.render(mecha.name + " upgrades", True, (255, 255, 255))
    bullet_text = smaller.render("Pierce +1", True, (255, 255, 255))
    cost1 = small.render("$300", True, (255, 255, 255))
    cost2 = small.render("$600", True, (255, 255, 255))
    exit_button = pygame.Rect(670, 200, 30, 30)
    reloadrect = (230, 400, 200, 200)
    piercerect = (470, 400, 200, 200)
    while running:
        mouse = pygame.mouse.get_pos()
        mouserect = pygame.Rect(mouse[0], mouse[1], 10, 10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouserect.colliderect(reloadrect):
                    if money >= 300:
                        mecha.slow -= 10
                        return 300
                    return 0
                elif mouserect.colliderect(piercerect):
                    if money >= 600:
                        mecha.pierce += 1
                        return 600
                    return 0
                elif mouserect.colliderect(exit_button):
                    return 0
        pygame.draw.rect(window, (0, 0, 0), (200, 200, 500, 500))
        pygame.draw.rect(window, (0, 255, 0), (200, 200, 500, 500), 1)
        pygame.draw.rect(window, (0, 0, 255), reloadrect, 1)
        pygame.draw.rect(window, (255, 0, 0), piercerect, 1)
        window.blit(test, (WIDTH//2-test.get_width()//2, 210))
        window.blit(bullet_text, (510, 400))
        window.blit(bullet, (520, 450))
        window.blit(reload, (240, 400))
        window.blit(cost1, (260, 330))
        window.blit(cost2, (500, 330))
        pygame.draw.line(window, (255, 255, 255), (670, 230), (700, 200))
        pygame.draw.line(window, (255, 255, 255), (670, 200), (700, 230))
        pygame.draw.rect(window, (255, 255, 255), exit_button, 1)
        if pygame.time.get_ticks()%1000 <= 200:
            window.blit(reload_image, (270, 460), (32*Factor, 242*Factor, 32*Factor, 53*Factor))
        elif pygame.time.get_ticks()%1000 <= 400:
            window.blit(reload_image, (270, 460), (128*Factor, 242*Factor, 32*Factor, 53*Factor))
        elif pygame.time.get_ticks()%1000 <= 600:
            window.blit(reload_image, (270, 460), (224*Factor, 242*Factor, 32*Factor, 53*Factor))
        elif pygame.time.get_ticks() % 1000 <= 800:
            window.blit(reload_image, (270, 460), (320*Factor, 242*Factor, 32*Factor, 53*Factor))
        else:
            window.blit(reload_image, (270, 460), (416*Factor, 242*Factor, 32*Factor, 53*Factor))

        pygame.display.update()

def game():
    balloon_list = [[] for _ in range(7)]
    for _ in range(5):
        balloon_list[0].append(Ballons(4))
        balloon_list[0].append(Ballons(5))
    for _ in range(7):
        balloon_list[1].append(Ballons(5))
        balloon_list[1].append(Ballons(6))
    for _ in range(9):
        balloon_list[2].append(Ballons(8))
        balloon_list[2].append(Ballons(9))
    for _ in range(12):
        balloon_list[3].append(Ballons(10))
        balloon_list[3].append(Ballons(12))
    for _ in range(14):
        balloon_list[4].append(Ballons(15))
        balloon_list[4].append(Ballons(16))
    for _ in range(16):
        balloon_list[5].append(Ballons(18))
        balloon_list[5].append(Ballons(19))
    for _ in range(20):
        balloon_list[6].append(Ballons(20))
        balloon_list[6].append(Ballons(25))
    mecha_list = []
    cheap_button = pygame.Rect(690, 690, 100, 100)
    medium_button = pygame.Rect(590, 690, 100, 100)
    heavy_button = pygame.Rect(490, 690, 100, 100)
    button_list = [cheap_button, medium_button, heavy_button]
    did = True
    name = ""
    checker = False
    it = 0
    time = 299
    slow = 0
    levels = {"level1": [Ballons(1) for _ in range(3)], "level2": [Ballons(2), Ballons(2), Ballons(2)], "level3": [Ballons(5), Ballons(5), Ballons(5)], "level4":balloon_list[0],
              "level5": balloon_list[1], "level6": balloon_list[2], "level7":balloon_list[3], "level8":balloon_list[4], "level9":balloon_list[5], "level10":balloon_list[6]}
    level = "level1"
    leveler = 1
    font = pygame.font.Font(None, 200)
    smaller_font = pygame.font.Font(None, 100)
    small_font = pygame.font.SysFont("Cambria", 75)
    money_font = pygame.font.SysFont('Cambria', 15)
    orig_surf = font.render('Level 1', True, (255, 255, 255))
    txt_surf = orig_surf.copy()
    never = smaller_font.render('NEVER SURRENDER!', True, (255, 255, 255))
    never1 = never.copy()
    alpha_surf1 = pygame.Surface(never1.get_size(), pygame.SRCALPHA)
    alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
    alpha = 255
    starting_money = 1000
    cost = {"Light": 150, "Medium": 350, "Heavy": 1000}
    lives = 5
    alpha1 = 255
    background = pygame.image.load('data/images/back.png')
    background = pygame.transform.scale(background, (900, 900))
    revive_complete = False
    life_bolt = pygame.image.load('data/images/nut.png').convert_alpha()
    life_bolt = pygame.transform.scale_by(life_bolt, 0.5)
    heavy_text = pygame.image.load('data/images/heavy.png').convert()
    heavy = pygame.image.load('data/images/player1.png').convert_alpha()
    medium = pygame.image.load('data/images/player.png').convert_alpha()
    medium_text = pygame.image.load('data/images/Med.png').convert()
    light = pygame.image.load('data/images/playerlight.png').convert_alpha()
    light_text = pygame.image.load('data/images/light.png').convert()
    button_clicked = False
    can_place = True
    can_click = False
    var = math.inf
    while run:
        mouse_pos = pygame.mouse.get_pos()
        time += 1
        clock.tick(FPS)
        window.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 10, 10)
                if len(mecha_list) >= 1:
                    for mecha in mecha_list:
                        if mecha.storrect.colliderect(mouse_rect) and var <= pygame.time.get_ticks() and name == "":
                            starting_money -= upgrade(mecha, starting_money)
                if cheap_button.colliderect(mouse_rect):
                    name = "Light"
                    checker = False
                    slow = 180
                    button_clicked = True
                elif medium_button.colliderect(mouse_rect):
                    name = "Medium"
                    checker = False
                    slow = 150
                    button_clicked = True
                elif heavy_button.colliderect(mouse_rect):
                    name = "Heavy"
                    checker = False
                    slow = 100
                    button_clicked = True
                if checker:
                    if name != "":
                        if starting_money - cost[name] >= 0:
                            mouse = pygame.mouse.get_pos()
                            mouse_rect = pygame.Rect(mouse[0], mouse[1], 50, 50)
                            for mecha in mecha_list:
                                if mecha.storrect.colliderect(mouse_rect):
                                    can_place = False
                            if can_place:
                                mecha_list.append(Mechas(name, mouse, balloon_pos, slow))
                                var = pygame.time.get_ticks() + 1
                                starting_money -= cost[name]
                                button_clicked = False
                    name = ""
                    did = False
                checker = True
                can_place = True

        if button_clicked:
            placing_units(name, heavy, medium, light, mouse_pos)
        if alpha > 0:
            alpha = max(alpha-1.2, 0)
            txt_surf = orig_surf.copy()
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        window.blit(heavy_text, (490, 690))
        window.blit(medium_text, (590, 690))
        window.blit(light_text, (690, 690))
        window.blit(money_font.render('$1000', False, (255, 255, 255)), (540, 743))
        window.blit(money_font.render('$350', False, (255, 255, 255)), (640, 743))
        window.blit(money_font.render('$150', False, (255, 255, 255)), (740, 743))
        for rect in button_list:
            pygame.draw.rect(window, (255, 0, 0), rect, 1)
        window.blit(heavy, (500, 743), (32, 50, 32, 45))
        window.blit(medium, (600, 743), (32, 50, 32, 45))
        window.blit(light, (700, 743), (32, 50, 32, 45))
        window.blit(life_bolt, (700, 0))
        window.blit((small_font.render(f":{lives}", False, (0, 255, 255))), (820, 10))
        window.blit((small_font.render(f"Money: ${starting_money}", False, (0, 0, 255))), (200, 0))
        window.blit(txt_surf, (WIDTH//2-txt_surf.get_width()//2, (HEIGHT//2-txt_surf.get_height()//2)))
        for i in range(it):
            levels[level][i].move()
            levels[level][i].draw()
        if levels[level][0].rect[0] <= -60:
            lives -= 1
            checkers(leveler, lives)
            del levels[level][0]
            if len(levels[level]) <= 0:
                leveler += 1
                checkers(leveler, lives)
                level = level[:5] + str(leveler)
                orig_surf = font.render(f"Level {leveler}", True, (255, 255, 255))
                alpha = 255
        balloon_pos = levels[level][0].ballpos()
        if not did:
            for mecha in mecha_list:
                if levels[level][0].rects.colliderect(mecha.bullet_rect):
                    levels[level][0].remove_layer(mecha.pierce)
                    starting_money += 15
                    mecha.can_shoot = False
                    if levels[level][0].strength <= 0:
                        del levels[level][0]
                        if len(levels[level]) <= 0:
                            leveler += 1
                            checkers(leveler, lives)
                            level = level[:5] + str(leveler)
                            orig_surf = font.render(f"Level {leveler}", True, (255, 255, 255))
                            alpha = 255
                    mecha.hitter()
                mecha.shoot(balloon_pos)
                mecha.draw()
        if time % 300 == 0:
            time = 1
            it += 1
        if it >= len(levels[level]):
            it = len(levels[level])
        if lives == 0:
            if alpha1 >= 255:
                value = pygame.time.get_ticks() + 5000
            if alpha1 > 0:
                alpha1 = max(alpha1 - 1, 0)
                never1 = never.copy()
                alpha_surf1.fill((255, 255, 255, alpha1))
                never1.blit(alpha_surf1, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            window.blit(never1, (WIDTH//2-never1.get_width()//2, (HEIGHT//2-never1.get_height()//2)))
            if value <= pygame.time.get_ticks():
                if not revive_complete:
                    for i in range(len(levels[level])):
                        del levels[level][0]
                    leveler += 1
                    checkers(leveler, lives)
                    level = level[:5] + str(leveler)
                    orig_surf = font.render(f"Level {leveler}", True, (255, 255, 255))
                    alpha = 255
                    revive_complete = True
                    lives = 3
        pygame.display.update()

if __name__ == "__main__":
    game()
    pygame.quit()
    quit()