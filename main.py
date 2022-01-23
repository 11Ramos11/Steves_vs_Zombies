import pygame
from pygame import mixer
import random

pygame.init()

screen_x = 720
screen_y = 560
sqr_size_x = 90
sqr_size_y = 70
col_n = int(screen_x / sqr_size_x)
row_n = int(screen_y / sqr_size_y)

screen = pygame.display.set_mode((screen_x, screen_y))

gameoverscreen = pygame.image.load("gameover.jpg")
gameover = False
clock = pygame.time.Clock()
dt = clock.tick()

mixer.music.load("Minecraft.wav")
mixer.music.play(-1)

class Shield:

    pos = (0, 0)
    x, y = pos
    size_x = 66
    size_y = 66
    hp = 300
    img = pygame.image.load("shield.png")
    placed = False
    dead = False

    def health_bar(self):
        if not self.dead:
            pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(self.x + 7, self.y + 70, 75 * self.hp / 300, 10))
            pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(self.x + 7, self.y + 70, 75, 10), 3)

    def appear(self):
        if not self.dead:
            screen.blit(self.img, (self.x + 25, self.y + 23))


Shields = []


class Miner:

    pos = (0,0)
    x, y = pos
    size_x = 46
    size_y = 85
    hp = 100
    img = pygame.image.load("miner.png")
    placed = False
    dead = False
    interval = 0
    time_set = False
    gold_cooldown = 13
    alpha = 0

    def health_bar(self):
        if not self.dead:
            pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(self.x + 6, self.y + 70, 75 * self.hp / 100, 10))
            pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(self.x + 6, self.y + 70, 75, 10), 3)

    def appear(self):
        if not self.dead:
            screen.blit(self.img, (self.x + 28, self.y - 19))

    def timer(self, time):

        if not self.time_set:
            self.interval = time
            self.time_set = True

        myfontnotif = pygame.font.Font("myfont.otf", 30)
        miner_notif = myfontnotif.render("+25", 1, (203, 146, 49))
        miner_notif.set_alpha(self.alpha)
        notif_x = self.x + self.size_x + 20
        notif_y = self.y - 10
        if time - self.interval <= 1:
            screen.blit(miner_notif, (notif_x, notif_y))
        else:
            screen.blit(miner_notif, (notif_x, notif_y))
            self.alpha -= 0.5

        if (time - self.interval) / 1000 >= self.gold_cooldown:
            self.interval = time
            xp = mixer.Sound("xp.wav")
            xp.play()
            self.alpha = 200
            return True
        return False


Miners = []
miner_notif = False
alpha_elapsed = 0


class Soldier:
    img = pygame.image.load("soldier_placed.png")
    pos = (0,0)
    x, y = pos
    size_x = 85
    size_y = 85
    placed = False
    hp = 100
    dead = False
    timer = 0
    bullet_img = pygame.image.load("bullet.png")
    bullet_x = 0
    temp_bool = True
    wait = False
    bullet_x = x + size_x - 19
    bullet_y = y - 2
    one_shot = False
    bullet_speed = 0.4
    bullet_cooldown = 2.5
    time_set = False

    def zombie_shot(self, zombie_x, dt, time):
        if not self.time_set:
            self.timer = time
            self.time_set = True
        if self.bullet_x >= zombie_x and self.one_shot:
            self.one_shot = False
            arrow_hit = mixer.Sound("arrow_hit.wav")
            arrow_hit.play()
            return True
        else:
            if self.one_shot:
                self.bullet_x += self.bullet_speed * dt
                screen.blit(self.bullet_img, (self.bullet_x, self.bullet_y))
            elif (time - self.timer)/1000 >= self.bullet_cooldown:
                self.timer = time
                self.one_shot = True
                bow = mixer.Sound("bow.wav")
                bow.play()
            return False

    def health_bar(self):
        if not self.dead:
            pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(self.x + 8, self.y + 70, 75 * self.hp/ 100, 10))
            pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(self.x + 8, self.y + 70, 75, 10), 3)

    def appear(self):
        if not self.dead:
            screen.blit(self.img, (self.x + 31, self.y - 5))


Soldiers = []
bullet_unset = False


class Zombie:
    speed = -0.025
    img = pygame.image.load("zombie_sprite_hd.png")
    size_x = 60
    size_y = 82
    x = screen_x
    interval = 0
    interval2 = 0
    frame_x = -10
    hp = 100
    placed = False
    dead = False
    timer = 0
    fst_time_hp = True

    def ate(self, time):
        if (time - self.timer) / 1000 >= 0.5:
            self.timer = time
            return True
        else:
            return False

    def health_bar(self):
        if self.fst_time_hp:
            self.maxhp = self.hp
            self.fst_time_hp = False
        pygame.draw.rect(screen, pygame.Color("red"),pygame.Rect(self.x + (self.size_x - 32) / 2, self.y - 20 + self.size_y, ((self.size_x - 10) * self.hp)/self.maxhp, 10))
        pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(self.x + (self.size_x - 32)/2, self.y - 20 + self.size_y, self.size_x - 10, 10), 3)

    def appear(self, time, dt):

        if self.hp > 0:

            if time - self.interval >= 0.35:
                self.frame_x += 90
                self.interval = time
                if self.frame_x >= 529:
                    self.frame_x = -10

            if time - self.interval2 >= 12.5:
                self.interval2 = time

            frame = (self.frame_x, 98, 65, 90)

            self.x += self.speed * dt
            screen.blit(self.img, (self.x, self.y - 20), frame)

            self.health_bar()
            self.placed = True

        if self.hp <= 0:
            self.placed = False
            self.dead = True
            self.x = screen_x

zombie_times = [random.uniform(20,25)]
zombie_interval = (20, 25)
index = 0
Level_1 = []

def add_zombies(limits, x):

    a, b = limits
    if x <= 15:
        a += 30/x
    else:
        a += 150/(61 + x)
    b = a + 5/x
    x += 1
    timing = random.uniform(a, b)
    return [timing, (a,b)]


miner_card = pygame.image.load("miner_card.png")
minercard_pos = (5, 4)
minercard_x = 80
minercard_y = 63
miner_selected = False

soldier_card = pygame.image.load("soldier_sel.png")
sol_card_pos = (minercard_pos[0] + minercard_x + 10, 6)
sol_card_x = 80
sol_card_y = 62
sol_selected = False

shield_card = pygame.image.load("shield_card.png")
shieldcard_pos = (sol_card_pos[0] + sol_card_x + 18, 0)
shieldcard_x = 67
shieldcard_y = 75
shield_selected = False

occupied_squares = []

shooting_timer = 0
eating_timer = 0

gold_bar = pygame.image.load("gold.png")
start_gold_timer = 0
gold_bars = 0
gold_cooldown = 5
gold_elapsed = 0
gold_bar_spawned = pygame.image.load("gold_spawned.png")
gold_spawn_sizex = 45
gold_spawn_sizey = 45
gold_spawned = False
gold_pos = (0,0)
gold_spawn_cooldown = 4

new_time = 0

running = True

grid = [[0]]

click = False

clock = pygame.time.Clock()

for temp in range(1, row_n):
    if grid[0][temp - 1] == 1:
        grid[0].append(0)
    else:
        grid[0].append(1)

for i in range(1, col_n):
    if grid[i - 1][0] == 1:
        column = [0]
    else:
        column = [1]
    for j in range(1, row_n):
        if column[j - 1] == 1:
            column.append(0)
        else:
            column.append(1)
    grid.append(column)

while running:
    timer = pygame.time.get_ticks()
    while not gameover:
        timer = pygame.time.get_ticks()
        screen.fill(pygame.Color((225, 198, 153, 255)))
        screen.blit(soldier_card, sol_card_pos)
        screen.blit(miner_card, minercard_pos)
        screen.blit(shield_card, shieldcard_pos)
        for col in range(col_n):
            for row in range(1,row_n - 1):
                if grid[col][row] == 1:
                    sqr1_color = pygame.Color((127, 255, 148, 255))
                    pygame.draw.rect(screen, sqr1_color, pygame.Rect(col * sqr_size_x, row * sqr_size_y, sqr_size_x, sqr_size_y))
                else:
                    sqr2_color = pygame.Color((100, 233, 112, 255))
                    pygame.draw.rect(screen, sqr2_color, pygame.Rect(col * sqr_size_x, row * sqr_size_y, sqr_size_x, sqr_size_y))

        time = pygame.time.get_ticks() / 1000 - new_time
        dt = clock.tick()

        if zombie_times[index] < time:

            temp_zomb = Zombie()
            temp_zomb.y = (random.randint(1, row_n - 2) * sqr_size_y)
            if random.randint(1,9) == 2 and index > 3:
                temp_zomb.img = pygame.image.load("zombie_helmet_sprite_hd.png")
                temp_zomb.hp = 175
            Level_1.append(temp_zomb)
            new_timing, zombie_interval = add_zombies(zombie_interval, index + 1)
            zombie_times += [new_timing]
            index += 1

        if miner_selected:
            pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(0, 0, sqr_size_x, sqr_size_y), 3)

        if sol_selected:
            pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(sqr_size_x, 0, sqr_size_x, sqr_size_y), 3)

        if shield_selected:
            pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(sqr_size_x * 2, 0, sqr_size_x, sqr_size_y), 3)

        if click:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            gold_bar_requirements = gold_pos[0] + gold_spawn_sizex >= mouse_x >= gold_pos[0] and gold_spawned and gold_pos[1] + gold_spawn_sizey >= mouse_y >= gold_pos[1]

            shield_requirements = shield_selected and sqr_size_y <= mouse_y <= (row_n - 1) * sqr_size_y and gold_bars >= 75 and not gold_bar_requirements

            if shield_requirements:
                temp_square = (mouse_x // sqr_size_x, mouse_y // sqr_size_y)
                if not temp_square in occupied_squares:
                    occupied_squares += [temp_square]
                    temp_placed_shield = Shield()
                    temp_placed_shield.temp_square = temp_square
                    Shields.append(temp_placed_shield)
                    shield_selected = False
                    gold_bars -= 75
                    block = mixer.Sound("block.wav")
                    block.play()

            shieldcard_requirements = shieldcard_pos[0] < mouse_x < shieldcard_pos[0] + shieldcard_x and shieldcard_pos[1] < mouse_y < shieldcard_pos[1] + shieldcard_y

            if shieldcard_requirements:
                select = mixer.Sound("select.wav")
                select.play()
                if shield_selected:
                    shield_selected = False
                else:
                    shield_selected = True
                    miner_selected = False
                    sol_selected = False

            miner_requirements = miner_selected and sqr_size_y <= mouse_y <= (row_n - 1) * sqr_size_y and gold_bars >= 50 and not gold_bar_requirements

            if miner_requirements:
                temp_square = (mouse_x // sqr_size_x, mouse_y // sqr_size_y)
                if not temp_square in occupied_squares:
                    occupied_squares += [temp_square]
                    temp_placed_miner = Miner()
                    temp_placed_miner.temp_square = temp_square
                    Miners.append(temp_placed_miner)
                    miner_selected = False
                    gold_bars -= 50
                    placing = mixer.Sound("placing.wav")
                    placing.play()

            miner_card_requirements = minercard_pos[0] < mouse_x < minercard_pos[0] + minercard_x and minercard_pos[1] < mouse_y < minercard_pos[1] + minercard_y
            if miner_card_requirements:
                select = mixer.Sound("select.wav")
                select.play()
                if miner_selected:
                    miner_selected = False
                else:
                    shield_selected = False
                    miner_selected = True
                    sol_selected = False

            soldier_requirements = sol_selected and sqr_size_y <= mouse_y <= (row_n-1)*sqr_size_y and gold_bars >= 100 and not gold_bar_requirements
            if soldier_requirements:
                temp_square = (mouse_x // sqr_size_x, mouse_y // sqr_size_y)
                if not temp_square in occupied_squares:
                    occupied_squares += [temp_square]
                    temp_placed_soldier = Soldier()
                    temp_placed_soldier.temp_square = temp_square
                    Soldiers.append(temp_placed_soldier)
                    sol_selected = False
                    gold_bars -= 100
                    placing = mixer.Sound("placing.wav")
                    placing.play()

            soldier_card_requirements = sol_card_pos[0] < mouse_x < sol_card_pos[0] + sol_card_x and sol_card_pos[1] < mouse_y < sol_card_pos[1] + sol_card_y
            if soldier_card_requirements:
                select = mixer.Sound("select.wav")
                select.play()
                if sol_selected:
                    sol_selected = False
                else:
                    shield_selected = False
                    miner_selected = False
                    sol_selected = True

            if gold_bar_requirements:
                gold_spawned = False
                gold_bar_requirements = False
                gold_bars += 25
                xp = mixer.Sound("xp.wav")
                xp.play()


            click = False


        for shield in Shields:
            shield.health_bar()

        for miner in Miners:
            miner.health_bar()

        for soldier in Soldiers:
            soldier.health_bar()


        def collision(eater, eaten):
            if eater.y // sqr_size_y == eaten.y // sqr_size_y and (eaten.x + eaten.size_x / 2) <= eater.x + 25 <= (eaten.x + eaten.size_x):
                eater.speed = -0.03 * eaten.dead

                if eater.ate(timer):
                    eaten.hp -= 4

                if eaten.hp <= 0:
                    eaten.dead = True

        for shield in Shields:

            if shield.dead and shield.temp_square in occupied_squares:
                occupied_squares.remove(shield.temp_square)
                Shields.remove(shield)
                block = mixer.Sound("block.wav")
                block.play()

            if not shield.placed:
                shield.placed = True
                shield.pos = ((mouse_x // sqr_size_x) * sqr_size_x, (mouse_y // sqr_size_y) * sqr_size_y)
                shield.x, shield.y = shield.pos
            shield.appear()

            for zomb in Level_1:
                collision(zomb, shield)

        for miner in Miners:

            if miner.dead and miner.temp_square in occupied_squares:
                occupied_squares.remove(miner.temp_square)
                Miners.remove(miner)
                oof = mixer.Sound("oof.wav")
                oof.play()

            if not miner.placed:
                miner.placed = True
                miner.pos = ((mouse_x // sqr_size_x) * sqr_size_x, (mouse_y // sqr_size_y) * sqr_size_y)
                miner.x, miner.y = miner.pos
            miner.appear()

            gold_bars += 25 * int(miner.timer(timer))

            for zomb in Level_1:
                collision(zomb, miner)


        for soldier in Soldiers:

            if soldier.dead and soldier.temp_square in occupied_squares:
                occupied_squares.remove(soldier.temp_square)
                Soldiers.remove(soldier)
                oof = mixer.Sound("oof.wav")
                oof.play()

            if not soldier.placed:
                soldier.placed = True
                soldier.pos = ((mouse_x // sqr_size_x) * sqr_size_x, (mouse_y // sqr_size_y) * sqr_size_y)
                soldier.x, soldier.y = soldier.pos
                soldier.bullet_y = soldier.y - 2
            soldier.appear()

            for zomb in Level_1:
                temp_zombs = [zomba.x for zomba in Level_1 if zomba.placed and zomba.y // sqr_size_y == zomb.y // sqr_size_y and zomba.x > soldier.x]
                try:
                    if zomb.x == min(temp_zombs):
                        if zomb.y // sqr_size_y == soldier.y // sqr_size_y:
                            if soldier.x < zomb.x:
                                if not bullet_unset:
                                    soldier.bullet_x = soldier.x + soldier.size_x - 19
                                    bullet_unset = True
                                if soldier.zombie_shot(zomb.x, dt, timer):
                                    zomb.hp -= 100/6
                                    bullet_unset = False

                    collision(zomb,soldier)

                except:
                    pass

        for zomb in Level_1:
            zomb.appear(time, dt)
            if zomb.x + zomb.size_x <= 0:
                gameover = True

        if (timer - gold_elapsed) / 1000 >= gold_spawn_cooldown and not gold_spawned:
            gold_elapsed = timer
            gold_pos = (random.randint(0, screen_x-gold_spawn_sizex), random.randint(sqr_size_y, screen_y - sqr_size_y * 2))
            gold_spawned = True

        if gold_spawned:
            gold_elapsed = timer
            screen.blit(gold_bar_spawned, gold_pos)

        myFontGold = pygame.font.Font("myfont.otf", 65)
        gold_label = myFontGold.render(str(gold_bars), 1, pygame.Color("Black"))
        screen.blit(gold_label, (sqr_size_x, ((row_n - 1) * sqr_size_y) + 10))
        screen.blit(gold_bar, (10, (row_n - 1) * sqr_size_y))

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                running = False
                gameover = True

            if ev.type == pygame.MOUSEBUTTONDOWN:
                click = True

        pygame.display.flip()

    if running:
        myFontScore = pygame.font.Font("myfont.otf", 30)
        score_label = myFontScore.render("Your Score: " + str(time), 1, pygame.Color("Red"))
        score_x, score_y = (score_label.get_size())
        screen.blit(gameoverscreen, (0, 0))
        screen.blit(score_label, ((screen_x/2 - (score_x/2)), screen_y - score_y - 5))
        pygame.display.flip()

    for ev in pygame.event.get():

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                Level_1 = []
                Soldiers = []
                Miners = []
                Shields = []

                shield_selected = False
                miner_selected = False
                sol_selected = False
                new_time = pygame.time.get_ticks() / 1000
                gold_bars = 0
                gold_spawned = False
                gold_elapsed = timer
                start_gold_timer = timer
                shooting_timer = timer
                alpha = 0

                if not gameover:
                    for zomb in Level_1:
                        zomb.speed *= 1.5
                    for soldier in Soldiers:
                        soldier.bullet_cooldown *= 0.5
                        soldier.bullet_speed *= 1.5
                    for miner in Miners:
                        miner.gold_cooldown *= 0.5
                    gold_cooldown *= 0.5

                gameover = False

        if ev.type == pygame.QUIT:
            running = False

pygame.quit()
