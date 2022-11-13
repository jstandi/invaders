import pygame
import time
import random as r
import json


def space_invaders():
    from pygame.locals import KEYDOWN, QUIT, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_ESCAPE, RLEACCEL, K_s, \
        K_BACKSPACE, K_RETURN, K_h
    pygame.init()
    screen_width = 1500
    screen_height = 1000
    screen = pygame.display.set_mode([screen_width, screen_height])
    clock = pygame.time.Clock()
    data = {}

    # To Do:
    # 1) fix high score list issue
    # 2) figure out sprite ghost when starting from high score page
    # 3) figure out spacing between names, scores in high score page
    # mechanics are officially done! 9/10/21

    def write(json_file, data):
        json.dump(data, open(json_file, 'w'))

    def retrieve(json_file):
        global data
        file = open(json_file, 'r')
        data = json.load(file)
        return data

    class Mechanics:
        def __init__(self):
            self.dead = False
            self.running = False
            self.paused = False
            self.home_page = True
            self.game_running = True
            self.score_input = False
            self.score_page = False
            self.score_text = ''
            self.player_name = ""
            self.lives = 3
            self.points = 0
            self.god_mode = False

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.dead = False
            self.surf = pygame.image.load('spaceship.PNG').convert()
            self.surf.set_colorkey((1, 1, 1), RLEACCEL)
            self.rect = self.surf.get_rect(center=((screen_width/2), screen_height-50))
            self.speed_y = 3
            self.speed_x = 7
            self.hp = 50
            self.ammo = 150
            self.lives = 3

        def update(self, key_dict):
            if self.dead:
                pass
            else:
                if key_dict[K_LEFT]:
                    self.rect.move_ip(-self.speed_x, 0)
                elif key_dict[K_RIGHT]:
                    self.rect.move_ip(self.speed_x, 0)
                if key_dict[K_SPACE]:
                    if self.ammo > 0:
                        x = self.rect.midtop
                        y = self.rect.top
                        new_laser = Laser(x, y)
                        new_laser.origin = 'player'
                        all_sprites.add(new_laser)
                        lasers.add(new_laser)
                        if not game.god_mode:
                            ammo_bar.total_ammo -= 1
                            ammo_bar.start_center -= 1/1.88
                            ammo_bar.decrease_ammo()
                            self.ammo -= 1
                elif key_dict[K_UP]:
                    self.rect.move_ip(0, -self.speed_y)
                elif key_dict[K_DOWN]:
                    self.rect.move_ip(0, self.speed_y)
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.right > screen_width:
                    self.rect.right = screen_width
                if self.rect.top < 0:
                    self.rect.top = 0
                if self.rect.bottom > screen_height:
                    self.rect.bottom = screen_height

    class TitlePlayer(pygame.sprite.Sprite):
        def __init__(self):
            super(TitlePlayer, self).__init__()
            self.surf = pygame.image.load('spaceship.PNG').convert()
            self.surf.set_colorkey((1, 1, 1), RLEACCEL)
            self.rect = self.surf.get_rect(center=((screen_width / 2), screen_height - 50))
            self.speed_x = 5

        def update(self):
            if self.rect.right > screen_width-200:
                self.speed_x *= -1
            if self.rect.left < 200:
                self.speed_x *= -1
            self.rect.move_ip(self.speed_x, 0)

        def full_kill(self):
            self.surf = pygame.Surface((1, 1))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect()
            self.kill()

    class DeathScreen(pygame.sprite.Sprite):
        def __init__(self):
            super(DeathScreen, self).__init__()
            self.surf = pygame.image.load('death_screen.png')
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(center=(screen_width/2, screen_height/2))

    class Laser(pygame.sprite.Sprite):
        def __init__(self, start_x, start_y):
            super(Laser, self).__init__()
            self.start_x = start_x[0]
            self.start_y = start_y + 10
            self.surf = pygame.Surface((4, 20))
            self.surf.fill((219, 23, 9))
            self.rect = self.surf.get_rect(center=(self.start_x, self.start_y))
            self.speed_y = 20
            self.speed_x = 0
            self.origin = None

        def update(self):
            if self.rect.bottom < 0:
                self.kill()
            else:
                self.rect.move_ip(0, -self.speed_y)

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load('alien.png').convert()
            self.surf.set_colorkey((1, 1, 1), RLEACCEL)
            self.rect = self.surf.get_rect(center=(x, y))
            self.speed_y = 1
            self.speed_x = r.randint(1, 3)
            self.max_left = x-40
            self.max_right = x+40
            self.start_time = time.time()
            self.current_time = 0

        def update(self):
            self.current_time = time.time()
            if self.rect.top > screen_height:
                game.lives -= 1
                self.kill()
                game.dead = True
            if self.rect.right > screen_width:
                self.rect.right = screen_width
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.max_right:
                self.speed_x *= -1
            if self.rect.left < self.max_left:
                self.speed_x *= -1
            if not player.dead:
                if self.current_time-self.start_time >= r.randint(1, 3):
                    x = self.rect.midbottom
                    y = self.rect.bottom
                    new_laser = Laser(x, y)
                    new_laser.origin = 'enemy'
                    new_laser.speed_y = -20
                    all_sprites.add(new_laser)
                    lasers.add(new_laser)
                    self.start_time = time.time()
                else:
                    self.rect.move_ip(self.speed_x, self.speed_y)

    class HealthBarOutline(pygame.sprite.Sprite):
        def __init__(self):
            super(HealthBarOutline, self).__init__()
            self.surf = pygame.Surface((160, 16))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(center=(85, screen_height-80))

    class HealthBar(pygame.sprite.Sprite):
        def __init__(self):
            super(HealthBar, self).__init__()
            self.total_health = 150
            self.start_center = 85
            self.surf = pygame.Surface((self.total_health, 14))
            self.surf.fill((189, 8, 8))
            self.rect = self.surf.get_rect(center=(self.start_center, screen_height-80))

        def decrease_health(self):
            if self.total_health < 0:
                self.total_health = 0
            self.surf = pygame.Surface((self.total_health, 14))
            self.surf.fill((198, 8, 8))
            self.rect = self.surf.get_rect(center=(self.start_center, screen_height-80))

    class AmmoBarOutline(pygame.sprite.Sprite):
        def __init__(self):
            super(AmmoBarOutline, self).__init__()
            self.surf = pygame.Surface((160, 16))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect(center=(85, screen_height-50))

    class AmmoBar(pygame.sprite.Sprite):
        def __init__(self):
            super(AmmoBar, self).__init__()
            self.total_ammo = 150
            self.start_center = 85
            self.surf = pygame.Surface((self.total_ammo, 14))
            self.surf.fill((77, 77, 77))
            self.rect = self.surf.get_rect(center=(self.start_center, screen_height-50))

        def decrease_ammo(self):
            self.surf = pygame.Surface((self.total_ammo, 14))
            self.surf.fill((77, 77, 77))
            self.rect = self.surf.get_rect(center=(self.start_center, screen_height-50))

    class Star(pygame.sprite.Sprite):
        def __init__(self, starting):
            super(Star, self).__init__()
            self.surf = pygame.Surface((r.randint(1, 10), r.randint(1, 10)))
            self.surf.fill((255, 255, 255))
            if starting:
                self.rect = self.surf.get_rect(center=(r.randint(30, screen_width-30), r.randint(30, screen_height-30)))
            else:
                self.rect = self.surf.get_rect(center=(r.randint(30, screen_width-30), screen_height))

        def update(self):
            self.rect.move_ip(0, -1)
            if self.rect.top < 0:
                self.kill()

    class PauseIcon(pygame.sprite.Sprite):
        def __init__(self, offset):
            super(PauseIcon, self).__init__()
            self.surf = pygame.Surface((10, 50))
            self.surf.fill((255, 255, 255))
            self.offset = offset
            self.rect = self.surf.get_rect(center=((screen_width/2)+offset, screen_height/2))

    class Pack(pygame.sprite.Sprite):
        def __init__(self, type_):
            super(Pack, self).__init__()
            self.type = type_
            if self.type == 'ammo':
                self.surf = pygame.image.load('ammo_box.png').convert()
                self.surf.set_colorkey((1, 1, 1), RLEACCEL)
            else:
                self.surf = pygame.image.load('health_pack.png').convert()
                self.surf.set_colorkey((1, 1, 1), RLEACCEL)
            self.rect = self.surf.get_rect(center=(r.randint(30, screen_width-30), 0))
            self.speed_y = 5

        def update(self):
            self.rect.move_ip(0, self.speed_y)
            if self.rect.top > screen_height:
                self.kill()

        def pick_up(self):
            if self.type == 'health':
                player.hp += 25
                health_bar.total_health += 25
                health_bar.start_center += 25/1.875
                health_bar.decrease_health()
                if player.hp > 50:
                    health_bar.total_health = 150
                    health_bar.start_center = 85
                    health_bar.decrease_health()
                    player.hp = 50
            if self.type == 'ammo':
                player.ammo += 50
                ammo_bar.total_ammo += 50
                ammo_bar.start_center += 50/1.88
                ammo_bar.decrease_ammo()
                if player.ammo > 150:
                    ammo_bar.total_ammo = 150
                    ammo_bar.start_center = 85
                    ammo_bar.decrease_ammo()
                    player.ammo = 150

    class Heart(pygame.sprite.Sprite):
        def __init__(self, offset):
            super(Heart, self).__init__()
            self.surf = pygame.image.load('heart.png').convert()
            self.surf.set_colorkey((1, 1, 1), RLEACCEL)
            self.offset = offset
            self.rect = self.surf.get_rect(center=(50+offset, 50))

    class TitleScreen(pygame.sprite.Sprite):
        def __init__(self):
            super(TitleScreen, self).__init__()
            self.surf = pygame.image.load('logo.png').convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(center=(screen_width/2, screen_height/2))

    class Score(pygame.font.Font):
        def __init__(self, score):
            if len(str(score)) == 1:
                score_str = '00'+str(score)
            elif len(str(score)) == 2:
                score_str = '0'+str(score)
            else:
                score_str = str(score)
            self.font = pygame.font.SysFont('Impact', 30)
            self.surf = self.font.render(score_str, True, (77, 77, 77))
            self.rect = self.surf.get_rect()

        def kill(self):
            self.surf = self.font.render('Impact', True, (0, 0, 0))
            self.rect = self.surf.get_rect()

    class InputPageTitle(pygame.sprite.Sprite):
        def __init__(self):
            super(InputPageTitle, self).__init__()
            self.surf = pygame.image.load('game_over.png').convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(center=(screen_width/2, screen_height/4))

    class ScoreInput(pygame.font.Font):
        def __init__(self):
            self.font = pygame.font.SysFont('Impact', 40)
            self.surf = self.font.render('___', True, (255, 255, 255))
            self.rect = self.surf.get_rect()

        def kill(self):
            self.surf = self.font.render('', True, (0, 0, 0))
            self.rect = self.surf.get_rect()

        def update(self, text):
            if len(text) == 1:
                render_text = text + '__'
            elif len(text) == 2:
                render_text = text + '_'
            elif len(text) > 3:
                render_text = text[0:3]
            elif len(text) == 0:
                render_text = '___'
            else:
                render_text = text
            self.surf = self.font.render(render_text, True, (255, 255, 255))
            self.rect = self.surf.get_rect()

    class ScorePageTitle(pygame.sprite.Sprite):
        def __init__(self):
            super(ScorePageTitle, self).__init__()
            self.surf = pygame.image.load('high_scores.png')
            self.surf.set_colorkey((1, 1, 1), RLEACCEL)
            self.rect = self.surf.get_rect(center=(screen_width/2, screen_height/4))

    class ScoreText(pygame.font.Font):
        def __init__(self, text):
            self.offset = 0
            self.text = str(text)
            self.font = pygame.font.SysFont('Impact', 40)
            self.surf = self.font.render(self.text, True, (255, 255, 255))
            self.rect = self.surf.get_rect()

        def kill(self):
            self.surf = self.font.render('', True, (0, 0, 0))
            self.rect = self.surf.get_rect()

    class Boss(pygame.sprite.Sprite):
        def __init__(self):
            super(Boss, self).__init__()
            self.surf = pygame.Surface((100, 100))
            self.surf.fill((126, 12, 240))
            self.rect = self.surf.get_rect(center=(screen_width / 2, 60))
            self.max_left = self.rect.midleft[0] + 80
            self.max_right = self.rect.midright[0] + 80
            self.speed_x = 3
            self.speed_y = 2
            self.health = 50

        def update(self):
            if self.rect.right > screen_width:
                self.rect.right = screen_width
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.max_right:
                self.speed_x *= -1
            if self.rect.left < self.max_left:
                self.speed_x *= -1

        def main_attack(self):
            # put into while loop inside gameplay loop - create multiple at once
            boss_laser = Laser(self.rect.midbottom[0], self.rect.midbottom[1])
            boss_laser.surf = pygame.Surface((125, 10))
            boss_lasers.add(boss_laser)


    game = Mechanics()
    title_player = TitlePlayer()
    stars = pygame.sprite.Group()
    for i in range(0, r.randint(15, 20)):
        star = Star(True)
        stars.add(star)
    star_num = len(stars)
    score_input = ScoreInput()
    input_page_title = InputPageTitle()
    score_group = pygame.sprite.Group()
    score_group.add(input_page_title)
    score_page_title = ScorePageTitle()
    score_page_group = pygame.sprite.Group()
    score_page_group.add(score_page_title)
    score_texts = []
    title_screen = TitleScreen()
    title_group = pygame.sprite.Group()
    title_group.add(title_player)
    title_group.add(title_screen)
    death_screen = DeathScreen()
    score = Score(0)
    hearts = pygame.sprite.Group()
    for i in range(0, 3):
        heart = Heart(40*i)
        hearts.add(heart)
    health_bar_outline = HealthBarOutline()
    health_bar = HealthBar()
    ammo_bar_outline = AmmoBarOutline()
    ammo_bar = AmmoBar()
    statuses = pygame.sprite.Group()
    statuses.add(health_bar_outline)
    statuses.add(health_bar)
    statuses.add(ammo_bar_outline)
    statuses.add(ammo_bar)
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(health_bar_outline)
    all_sprites.add(health_bar)
    all_sprites.add(ammo_bar_outline)
    all_sprites.add(ammo_bar)
    packs = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    boss_lasers = pygame.sprite.Group()
    enemy_x = 250
    game.god_mode = False

    def create_enemies(x):
        for num in range(0, 5):
            enemy = Enemy(x, 40)
            x += r.randint(245, 255)
            all_sprites.add(enemy)
            enemies.add(enemy)

    def game_over():
        game.running = False
        game.dead = False
        game.home_page = True

    def create_score_texts(score_data):
        score_data.sort(key=lambda x: x['score'], reverse=True)
        offset = 0
        for item in score_data:
            name = item['player']
            score = item['score']
            if len(name+str(score)) < 12:
                spaces = 12-len(name+str(score))
            text = name + ' '*spaces + str(score)
            new_text_class = ScoreText(text)
            new_text_class.offset = offset
            score_texts.append(new_text_class)
            offset += 40

    loop_counter = 0
    pack_types = ['ammo', 'health']
    homepage_text = ''
    title_sprite = True

    # this loop is the entire game - homepage and everything
    while game.game_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                game.running = False

        # homepage loop
        while game.home_page:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game.home_page = False
                    game.game_running = False
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        game.home_page = False
                        game.running = True
                        pygame.mouse.set_visible(False)
                        title_player.kill()
                        title_sprite = False
                        if title_player in title_group:
                            player.rect.union_ip(title_player.rect)
                        if hasattr(title_player, 'rect'):
                            title_player.rect.bottom = 1529436
                    if event.key == K_h:
                        game.score_page = True
                        game.home_page = False
                        title_player.kill()
                        title_sprite = False
                        create_score_texts(retrieve('scorekeeper.json'))
                    if event.key != K_s and event.key != K_h:
                        try:
                            homepage_text += str(chr(event.key))
                        except:
                            pass
                        if homepage_text == 'invade':
                            game.god_mode = True

            screen.fill((0, 0, 0))

            for entity in stars:
                screen.blit(entity.surf, entity.rect)
            for entity in stars:
                entity.update()

            if len(stars) < star_num:
                new_star = Star(False)
                stars.add(new_star)

            screen.blit(title_player.surf, title_player.rect)
            screen.blit(title_screen.surf, title_screen.rect)
            if title_sprite:
                title_player.update()
            pygame.display.flip()
            clock.tick(45)

        # high score page loop
        while game.score_page:
            if title_player in title_group:
                title_player.kill()
            if title_screen in title_group:
                title_screen.kill()
            for event in pygame.event.get():
                if event.type == QUIT:
                    game.score_page = False
                    game.game_running = False
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        game.score_page = False
                        game.home_page = True
                        title_sprite = True
                        for text in score_texts:
                            text.kill()

            screen.fill((0, 0, 0))

            for entity in stars:
                screen.blit(entity.surf, entity.rect)
            for entity in stars:
                entity.update()

            screen.blit(score_page_title.surf, score_page_title.rect)

            if len(stars) < star_num:
                new_star = Star(False)
                stars.add(new_star)

            # need to blit each text in list with offset
            for text in score_texts:
                if text.rect.bottom < screen_height:
                    screen.blit(text.surf, ((screen_width/2)-100, score_page_title.rect.midbottom[1]+25+text.offset))

            pygame.display.flip()
            clock.tick(45)

        # gameplay loop
        while game.running:
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    game.running = False
                    game.game_running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game.paused = True
                        pause_left = PauseIcon(-15)
                        pause_right = PauseIcon(15)
                        pause_group = pygame.sprite.Group()
                        pause_group.add(pause_left)
                        pause_group.add(pause_right)
                        for entity in pause_group:
                            screen.blit(entity.surf, entity.rect)
                            pygame.display.flip()

            # pause loop
            while game.paused:
                pressed_keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        game.running = False
                        game.paused = False
                        game.game_running = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            for entity in pause_group:
                                entity.kill()
                            game.paused = False

            # death and restart from death loop
            while game.dead:
                pressed_keys = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        game.running = False
                        game.dead = False
                        game.game_running = False
                    if event.type == KEYDOWN:
                        if event.key == K_s:
                            stars = pygame.sprite.Group()
                            for i in range(0, r.randint(15, 20)):
                                star = Star(True)
                                stars.add(star)
                            star_num = len(stars)
                            hearts = pygame.sprite.Group()
                            for i in range(0, game.lives):
                                heart = Heart(40 * i)
                                hearts.add(heart)
                            health_bar_outline = HealthBarOutline()
                            health_bar = HealthBar()
                            ammo_bar_outline = AmmoBarOutline()
                            ammo_bar = AmmoBar()
                            statuses = pygame.sprite.Group()
                            statuses.add(health_bar_outline)
                            statuses.add(health_bar)
                            statuses.add(ammo_bar_outline)
                            statuses.add(ammo_bar)
                            player = Player()
                            player_group = pygame.sprite.Group()
                            player_group.add(player)
                            all_sprites = pygame.sprite.Group()
                            all_sprites.add(player)
                            all_sprites.add(health_bar_outline)
                            all_sprites.add(health_bar)
                            all_sprites.add(ammo_bar_outline)
                            all_sprites.add(ammo_bar)
                            packs = pygame.sprite.Group()
                            lasers = pygame.sprite.Group()
                            enemies = pygame.sprite.Group()
                            create_enemies(enemy_x)
                            game.dead = False
                screen.blit(death_screen.surf, death_screen.rect)
                pygame.display.flip()

            # this and below is within the gameplay loop
            player.update(pressed_keys)
            screen.fill((0, 0, 0))

            if player.hp <= 0 or player.dead:
                game.lives -= 1
                if game.lives == 0:
                    game_over()
                for entity in packs:
                    entity.kill()
                for entity in enemies:
                    entity.kill()
                for entity in lasers:
                    entity.kill()
                for entity in hearts:
                    entity.kill()
                for i in range(0, game.lives):
                    heart = Heart(40*i)
                    hearts.add(heart)
                game.dead = True

            if not game.god_mode:
                if player.hp < 20 or player.ammo < 45:
                    if loop_counter % 45*10 == 0:
                        new_pack = Pack(r.choice(pack_types))
                        packs.add(new_pack)

            if loop_counter % (45*(r.randint(13, 15))) == 0:
                create_enemies(enemy_x)

            for entity in stars:
                screen.blit(entity.surf, entity.rect)

            screen.blit(score.surf, (screen_width-50, 10))

            for entity in hearts:
                screen.blit(entity.surf, entity.rect)

            for entity in packs:
                screen.blit(entity.surf, entity.rect)
                entity.update()

            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

            for entity in stars:
                entity.update()

            if len(stars) != star_num:
                new_star = Star(False)
                stars.add(new_star)

            for entity in lasers:
                entity.update()

            for entity in enemies:
                entity.update()

            for entity in lasers:
                if pygame.sprite.spritecollideany(entity, enemies):
                    if hasattr(entity, 'origin'):
                        if entity.origin == 'player':
                            for entity in enemies:
                                if pygame.sprite.spritecollideany(entity, lasers):
                                    entity.kill()
                                    game.points += 1
                                    score.kill()
                                    score = Score(game.points)
            if not game.god_mode:
                if pygame.sprite.spritecollideany(player, lasers):
                    player.hp -= 5
                    health_bar.total_health -= 15
                    health_bar.start_center -= 15/1.875
                    if player.hp < 15:
                        health_bar.total_health = player.hp*3
                        health_bar.start_center = (player.hp*3)/1.3
                    health_bar.decrease_health()
                    if player.hp == 0:
                        player.dead = True
                        player.kill()

            for entity in packs:
                if pygame.sprite.spritecollideany(entity, player_group):
                    entity.pick_up()
                    entity.kill()

            if game.god_mode:
                player.hp = 50
                player.ammo = 150
                player.speed_x = 15
                player.speed_y = 12
                ammo_bar.kill()
                ammo_bar_outline.kill()
                health_bar.kill()
                health_bar_outline.kill()

            pygame.display.flip()
            clock.tick(45)
            loop_counter += 1

        if game.dead:
            game.score_input = True
        while game.score_input:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game.score_input = False
                    game.game_running = False
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        if len(game.score_text) > 0:
                            game.score_text = game.score_text[:-1]
                    else:
                        if len(game.score_text) < 3:
                            try:
                                game.score_text += str(chr(event.key))
                            except:
                                pass
                    score_input.update(game.score_text)
                    if event.key == K_RETURN:
                        if game.score_text == '':
                            game.score_input = False
                        else:
                            game.player_name = game.score_text
                            score_input.kill()
                            input_page_title.kill()
                            score_list = retrieve('scorekeeper.json')
                            score_list.append({"player": game.player_name, "score": game.points})
                            write('scorekeeper.json', score_list)
                            game.score_input = False

            screen.fill((0, 0, 0))
            screen.blit(score_input.surf, (screen_width/2, screen_height-500))
            screen.blit(input_page_title.surf, input_page_title.rect)
            pygame.display.flip()

        # this block runs at the end of the main loop
        game.lives = 3
        player.lives = 3
        player.hp = 50
        player.ammo = 150
        game.home_page = True
        player.dead = False
        game.dead = False
        player = Player()
        player_group.add(player)
        all_sprites.add(player)
        game.points = 0
        score = Score(game.points)
        health_bar.total_health = 150
        for i in range(0, game.lives):
            new_heart = Heart(40*i)
            hearts.add(new_heart)
        health_bar.kill()
        health_bar = HealthBar()
        all_sprites.add(health_bar)


space_invaders()
