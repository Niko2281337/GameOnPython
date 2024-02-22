import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((700,400))
pygame.display.set_caption('OkhlopkovAndVolkov')


background = pygame.image.load('images/background.jpeg').convert_alpha()
player = pygame.image.load('images/hero.png').convert_alpha()
walk_right = [
    pygame.image.load('images/run1.png').convert_alpha(),
    pygame.image.load('images/run2.png').convert_alpha(),
    pygame.image.load('images/run3.png').convert_alpha(),
    pygame.image.load('images/run4.png').convert_alpha()
]

walk_left = [
    pygame.image.load('images/run-1.png').convert_alpha(),
    pygame.image.load('images/run-2.png').convert_alpha(),
    pygame.image.load('images/run-3.png').convert_alpha(),
    pygame.image.load('images/run-4.png').convert_alpha()
]
attack = pygame.image.load('images/attack.png').convert_alpha()




kills = 0
reaper_list = []

boss = pygame.image.load('images/boss.webp').convert_alpha()

skeleton = pygame.image.load('images/reaper.png').convert_alpha()
skeleton_x = 500

player_anim_count = 0
background_x = 0
player_speed_right = 5
player_speed_left = 10
player_x = 150
player_y = 300

is_jump = False
jump_count = 8


lightning = pygame.image.load('images/lightning.png').convert_alpha()
lightnings = []

dontwin = True
game = True
label = pygame.font.SysFont('arial', 40)
label_kills = pygame.font.SysFont('arial', 18)
kill_labes = label_kills.render(f'kills: {kills}', False, (255, 0 , 0))
lose_label = label.render('Поражение', False, (255, 0 ,0))
restart_label = label.render('Начать заново', False, (130,130 ,130))
win_label = label.render('ТЫ ВЫИГРАЛ!', False, (0,128,0) )
restart_label_rect = restart_label.get_rect(topleft=(230, 200))

reaper_timer = pygame.USEREVENT + 1
pygame.time.set_timer(reaper_timer, 2000)

running = True
while running:
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 700, 0))
    screen.blit(kill_labes, (500, 50) )
    

    if game and dontwin:
        

        if kills >= 11:
            dontwin = False

        


        player_rect = player.get_rect(topleft=(player_x, player_y))
        boss_rect = boss.get_rect(topleft=(skeleton_x, 100))
        
        if reaper_list:
            for (i,el) in enumerate(reaper_list):
                screen.blit(skeleton, el)
                el.x -= 10

                if el.x < -10:
                    reaper_list.pop(i)

                if player_rect.colliderect(el):
                    print('you lose')
                    game = False
            



        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_RIGHT]:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        elif keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        elif keys[pygame.K_b]:
            screen.blit(attack, (player_x, player_y))
        else:
            screen.blit(player, (player_x, player_y))

        
        if keys[pygame.K_RIGHT] and player_x < 1300:
        
            player_x += player_speed_right
            background_x -= 5
        elif keys[pygame.K_LEFT] and player_x > 80:
            player_x -= player_speed_left
            background_x += 5

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count**2) / 2
                else:
                    player_y += (jump_count**2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count +=1 

        
        if background_x == -690:
            background_x == 0

        if keys[pygame.K_b]:
            lightnings.append(lightning.get_rect(topleft=(player_x + 40, player_y + 10)))

        if lightnings:
            for (i,el) in enumerate(lightnings):
                screen.blit(lightning, (el.x, el.y))
                el.x += 15

                if el.x >1300:
                    lightnings.pop(i)
                
                if reaper_list:
                    for(index, reap) in enumerate(reaper_list):
                        if el.colliderect(reap):
                            reaper_list.pop(index)
                            lightnings.pop(i)
                            kill_labes = label_kills.render(f'kills: {kills}', False, (255, 0 , 0))
                            kills += 1
                            if kills == 10:
                                reaper_list.clear
                                
                

    elif dontwin == True and game ==False:
        screen.fill((90, 90, 90))
        screen.blit(lose_label, (250, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            kills = 0
            game = True
            dontwin = True
            player_x = 150
            background_x = 0
            reaper_list.clear()
            lightnings.clear()
    
    else:

        screen.fill((90,90,90))
        screen.blit(win_label, (230, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            kills = 0
            game = True
            dontwin = True
            player_x = 150
            background_x = 0
            reaper_list.clear()
            lightnings.clear()


    
    pygame.display.update()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
            pygame.quit()
        if i.type == reaper_timer and kills < 11:
            reaper_list.append(skeleton.get_rect(topleft=(720, 300)))

      
            

    clock.tick(12)