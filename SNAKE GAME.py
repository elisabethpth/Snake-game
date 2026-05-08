# --- SNAKE GAME ---

# --- MOODULITE IMPORTIMINE ---
import pygame # Impordib PyGame'i mooduli
import random # Impordib random mooduli

pygame.init() # Käivitab PyGame'i mooduli

# --- SEADED ---
# EKRAANI SEADED
screenx, screeny = 800, 600 # Mänguakna laius ja kõrgus
screen = pygame.display.set_mode((screenx, screeny)) # Akna loomine
pygame.display.set_caption("Snake Game - IS25 :)") # Pealkiri aknale

# MÄNGU SEADED
fps = 30 # Ekraani FPS
clock = pygame.time.Clock() # Kell  FPS-i kontrollimiseks
grid_size = 30 # Jagab ekraani ruudustikuks, ühe ruudu suurus 30x30
snake_start_speed = 10 # Mao algne liikumiskiirus

# OBJEKTIDE SUURUSED
food_size = 30 # Toidu suurus
head_size = 40 # Mao pea suurus
body_size = 30 # Ühe kehaosa suurus

# NIHKED
head_offset = (head_size - grid_size) // 2 # Pea nihe ruudustikus, et keha algaks siis kui pea lõpeb
body_offset = (body_size - grid_size) // 2 # Keha nihe ruudustikus, et pildid üksteist ei kataks

# SUUNAD KRAADIDES | PILTIDE PÖÖRAMISEKS
DIRECTIONS = {"UP": 0, "RIGHT": -90, "DOWN": 180, "LEFT": 90}

# TEKSTI FONT
title_font = pygame.font.SysFont("None", 33) # Pealkirja font ja suurus
score_font = pygame.font.SysFont("None", 30) # Skoori font ja suurus
white = (255, 255, 255) # Valge RGB value, teksti värv

# --- MÄNGU TAUSTAHELID ---
# sounds = [] # List muusikafailidest
# pygame.mixer.music.load(random.choice(sounds)) # Valib juhuslikult helifaili
# pygame.mixer.music.play() # Alustab taustamuusika esitamist


# --- PILTIDE ÜLESLAADIMINE ---

# MÄNGU TAUSTAPILDID
background_paths = ["dirt.png", "muld.png", "muru.png"] # Failiteed erinevatest taustapiltidest
background_images = [] # List taustapiltide jaoks

for path in background_paths: # Käib läbi kõik failiteed
    bg = pygame.image.load(path).convert_alpha() # Laeb pildi failist mällu
    bg = pygame.transform.smoothscale(bg, (800, 600))  # Taustapildi suurus
    background_images.append(bg)  # Lisab pildi listi

current_background = random.choice(background_images)

# MAO PEA
snake_head_images = {} # Sõnastik peapiltide jaoks

head_paths = ["kennet.png", "rico.png", "lisett.png", "mariliis.png",
              "raven.png", "kevin.png", "sander.png", "alina.png",
              "caspar.png", "gert.png", "mikk.png", "jonatan.png",
              "steven.png", "karl.png"] # Failiteed peapiltidest

head = pygame.image.load(random.choice(head_paths)).convert_alpha()
head = pygame.transform.smoothscale(head, (head_size, head_size))

for dir_name in ["UP", "RIGHT", "DOWN", "LEFT"]:
    snake_head_images[dir_name] = pygame.transform.rotate(head, DIRECTIONS[dir_name])

# MAO KEHA
snake_body_images = list(snake_head_images.values()) # Kopeerib peapildid ka kehapiltideks

# MAO TOIT
food_images = [] # List toidupiltide jaoks

food_paths = ["apple.png", "fries.png", "cookie.png", "corn.png",
         "icecream.png", "sandwich.png", "noodles.png",
         "steak.png", "sushi.png", "salad.png"] # Toidupiltide failiteed

for path in food_paths: # Käib läbi kõik failiteed
    food = pygame.image.load(path).convert_alpha() # Laeb pildi failist mällu
    food = pygame.transform.smoothscale(food, (food_size, food_size)) # Toidu pildi suurus
    food_images.append(food) # Lisab pildi listi

# MÄNG LÄBI | EKRAANI TAUST
theend = pygame.image.load("theend.jpg") # Pilt kaotuse korral
theend = pygame.transform.scale(theend, (800, 600)) # Pildi suurus


# --- FUNKTSIOONID / MEETODID ----

# FUNKTSIOON | NIME SISESTAMINE MÄNGUAKNAS
def ask_name():  # Funktsioon, mis küsib kasutajalt nime ja tagastab selle
    name = ""  # Tühja stringina alustatakse nime salvestamist

    while True:  # Tsükkel töötab seni, kuni nimi on sisestatud või mäng suletakse

        # KÄIB LÄBI KÕIK SÜNDMUSED
        for event in pygame.event.get():

            # KUI MÄNGIJA VAJUTAB (X)
            if event.type == pygame.QUIT:
                pygame.quit()  # Sulgeb PyGame'i
                quit()

            # KUI MÄNGIJA VAJUTAB KLAHVI
            if event.type == pygame.KEYDOWN:

                # ESC = Sulgeb mängu
                if event.key == pygame.K_ESCAPE:  # Kui mängija vajutab ESC klahvi
                    pygame.quit()  # Sulgeb PyGame'i
                    quit()

                # ENTER = Alustab mängu
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: # Kui mängija vajutab ENTER
                    if name.strip():
                        return name.strip()
                    return "Player"  # Tagastab sisestatud nime ja alustab mängu

                # BACKSPACE = Kustutab tähe
                elif event.key == pygame.K_BACKSPACE:  # Kui mängija vajutab BACKSPACE
                    name = name[:-1]  # Kustutab viimase kirjutatud tähe

                # TÄHTEDE KIRJUTAMINE
                else: # Kui nimi pole liiga pikk ja sümbol on trükitav
                    if (len(name)) < 15:
                        name += event.unicode  # Lisab tähe nime lõppu

        screen.blit(current_background, (0, 0))  # Joonistab taustapildi ekraanile

        # MÄNGIJA NIME KÜSIMINE
        text1 = title_font.render("Enter your name:", True, white)  # Loob teksti "Enter your name"
        screen.blit(text1, (screenx // 2 - 150, screeny // 2 - 50))  # Kuvab selle teksti ekraani keskele (veidi üles)

        # NIMEKAST
        box = pygame.Rect(screenx // 2 - 150, screeny // 2, 300, 40)
        pygame.draw.rect(screen, (60, 60, 60), box, border_radius=8)

        # NIME KIRJUTAMINE
        text2 = title_font.render(name, True, white)  # Renderdab praegu sisestatud nime tekstiks
        screen.blit(text2, (screenx // 2 - 140, screeny // 2))  # Kuvab nime ekraani keskele

        # HINT | "VAJUTA ENTER, ET ALUSTADA MÄNGU"
        hint = score_font.render("Press ENTER to start", True, (180, 180, 180))
        screen.blit(hint, (screenx // 2 - 110, screeny // 2 + 60)) # Kuvab teksti

        pygame.display.flip()  # Ekraani uuendamine
        pygame.event.pump()
        clock.tick(30)  # Piirab tsükli kiiruse 30 kaadrini sekundis

# FUNKTSIOON | KAOTUSE TEKST
def message(msg, color): # Funktsioon, mis kuvab kaotuse teksti
    text = title_font.render(msg, True, color) # Teeb kaotuse tekstist pildi
    screen.blit(text, (260, 500)) # Kuvab kaotuse teksti ekraanile

# FUNKTSIOON | SKOORI LUGEMINE
def show_score(score): # Kuvab jooksvalt mängija skoori
    value = score_font.render("Score: " + str(score), True, white) # Skoori joonistamine ekraanile
    screen.blit(value, (340, 30)) # Kuvab skoori üleval vasakus nurgas

# FUNKTSIOON | SKOORI SALVESTAMINE
def save_score(name, score): # Skoori salvestamine
    with open("leaderboard.txt", "a", encoding="utf-8") as file: # Avab faili skoori juurdelisamiseks
        file.write(f"{name} - {score}\n") # Kirjutab faili mängija nime ja skoori

# FUNKTSIOON | LEADERBOARD
def draw_leaderboard(): # Edetabel 5 parima mängija skoori kuvamiseks
    try: # Proovib faili avada ja lugeda
        with open("leaderboard.txt", "r", encoding="utf-8") as f: # Avab faili lugemiseks
            lines = f.readlines() # Loeb faili sisu
    except FileNotFoundError: # Kui faili pole -
        lines = [] # - Annab tühja skoori listi

    scores = [] # List skooridest
    for line in lines: # Käib kõik read läbi
        if " - " in line: # Kontrollib formaati
            name, score = line.strip().split(" - ") # Võtab nime ja skoori
            scores.append((name, int(score))) # Lisab listi mängija nime ja skoori

    scores.sort(key=lambda x: x[1], reverse=True) # Sorteerib kõik tulemused
    scores = scores[:5]  # Võtab ainult TOP 5 tulemust

    y = 70  # y-koordinaadi algpositsioon
    title = title_font.render("LEADERBOARD:", True, white) # Pealkiri edetabelile
    screen.blit(title, (30, 30)) # Kuvab pealkirja ekraanile

    for name, score in scores: # Käib läbi kõik TOP 5 tulemust
        line = score_font.render(f"{name}: {score}", True, white) # Loob tekstirea (nimi + skoor)
        screen.blit(line, (30, y)) # Kuvab selle tekstirea ekraanile
        y += 25 # Liigutab järgmise tekstirea 25 pikslit allapoole


# ROTATSIOONI CACHE
rotation_cache = {}

# FUNKTSIOON | ÜHINE ROTATSIOON PILTIDEL
def get_rotated_image(image, direction):
    cache_key = (id(image), direction)

    if cache_key in rotation_cache:
        return rotation_cache[cache_key]

    rotated_img = pygame.transform.rotate(image, DIRECTIONS[direction])
    rotation_cache[cache_key] = rotated_img
    return rotated_img

# FUNKTSIOON | MAO JOONISTAMINE
def draw_snake(snake_list, snake_direction):

    for i, block in enumerate(snake_list):

        # PEA JOONISTAMINE
        if i == len(snake_list) - 1:
            snakehead = snake_head_images[snake_direction]
            screen.blit(snakehead, (block[0] - head_offset, block[1] - head_offset))

        # KEHA JOONISTAMINE
        else:
            body_dir = block[2]          # segmendi suund
            segment_image = block[3]     # segmendi PÜSIV pilt
            rotated_body = get_rotated_image(segment_image, body_dir)

            screen.blit(rotated_body, (block[0] - body_offset, block[1] - body_offset))

# --- FUNKTSIOON | MÄNGUTSÜKKEL ---
def gameloop(): # Mängu põhitsükkel
    gameover = False # Kontrollib, kas mäng on lõppenud (exit)
    gameclose = False # Kontrollib, kas mängija on kaotanud (game over ekraan)

# --- MÄNGU ALGUS | MAO ALGSEADED ---
    x1, y1 = (screenx // 2), (screeny // 2) # Mao algpositsioon
    x_change, y_change = 0, 0  # Mängu alguses madu seisab
    snake_direction = "UP" # Algne pea suund - üles
    snake_list = [] # Keha list - kehaosade koordinaadid
    length_of_snake = 1 # Mao pikkus mängu alguses
    new_snake_speed = 8 # Liikumiskiirus mängu alustades

# --- TOIT ---
    foodx = random.randrange(0, screenx // grid_size) * grid_size # Juhuslik x- koordinaat toidupildile
    foody = random.randrange(0, screeny // grid_size) * grid_size # Juhuslik y- koordinaat toidupildile
    current_food = random.choice(food_images) # Valib listist juhusliku toidupildi

# --- MÄNGU PEAMINE TSÜKKEL ---
    while not gameover: # Töötab, kuni gameover = True

    # MÄNG PEATATUD | KAOTUSE OLEK
        while gameclose: # Kaotuse olek
            screen.blit(theend, (0, 0)) # Kuvab kaotuse tausta
            draw_leaderboard() # Kuvab TOP 5 mängijate edetabeli
            message("Press Q-Quit | C-Play Again", white) # Kuvab juhised - ootab mängija sisendit
            show_score(length_of_snake - 1) # Kuvab mängija lõppskoori
            pygame.display.flip() # Uuendab ekraani

            for event in pygame.event.get(): # Käib läbi kõik mängu sündmused

                if event.type == pygame.KEYDOWN: # Kui mängija vajutab klahvi

                    if event.key == pygame.K_q: # Kui kasutaja vajutab "Q" = quit game
                        save_score(player_name, length_of_snake- 1) # Salvestab skoori
                        return False # Lõpetab mängu

                    if event.key == pygame.K_c: # Kui kasutaja vajutab "C" = restart game
                        save_score(player_name, length_of_snake -1) # Salvestab skoori
                        return True # Alustab uut mängu

# --- EVENTID | SÜNDMUSED --- MÄNGU SULGEMINE
                    if event.type == pygame.QUIT: # Kui kasutaja vajutab "X"
                        return False # Lõpetab mängu

                # NOOLEKLAHVIDELE VAJUTAMINE | MAO LIIKUMINE
                if event.type == pygame.KEYDOWN: # Kui mängija vajutab nooleklahvi

                    # MAO LIIKUMISSUUND - VASAK
                    if event.key == pygame.K_LEFT and x_change == 0: # Kui vajutatakse vasakut nooleklahvi
                        x_change = -snake_start_speed # Alustab liikumist vasakule
                        y_change = 0 # y-teljel liikumist ei toimu
                        snake_direction = "LEFT" # Liikumissuund - VASAKULE

                    # PAREM
                    elif event.key == pygame.K_RIGHT and x_change == 0: # Kui vajutatakse paremat nooleklahvi
                        x_change = snake_start_speed # Alustab liikumist paremale
                        y_change = 0 # y-teljel liikumist ei toimu
                        snake_direction = "RIGHT" # Liikumissuund - PAREMALE

                    # ÜLES
                    elif event.key == pygame.K_UP and y_change == 0:  # Kui vajutatakse ülemist nooleklahvi
                        y_change = -snake_start_speed # Alustab liikumist üles
                        x_change = 0 # x-teljel liikumist ei toimu
                        snake_direction = "UP" # Liikumissuund - ÜLES
                    # ALLA
                    elif event.key == pygame.K_DOWN and y_change == 0: # Kui vajutatakse alumist nooleklahvi
                        y_change = snake_start_speed # Alustab liikumist alla
                        x_change = 0 # x-teljel liikumist ei toimu
                        snake_direction = "DOWN" # Liikumissuund - ALLA

            # MAO LIIKUMINE
            x1 += x_change  # Mao liikumine x-teljel
            y1 += y_change  # Mao liikumine y-teljel
            # uuenda eelmiste segmentide suunda (liiguvad ettepoole)
            for i in range(len(snake_list) - 1):
                snake_list[i][2] = snake_list[i + 1][2]

# MAO LIIKUMINE LÄBI SEINTE - PAREM ÄÄR
        if x1 >= screenx: # Kui madu liigub paremalt äärest välja
            x1 = 0 # Liigub vasakult äärest tagasi
    # VASAK ÄÄR
        elif x1 < 0: # Kui madu liigub vasakult äärest välja
            x1 = screenx - grid_size # Liigub paremalt äärest tagasi
    # ALUMINE ÄÄR
        if y1 >= screeny: # Kui madu liigub alt äärest välja
            y1 = 0 # Liigub ülevalt äärest tagasi
    # ÜLEMINE ÄÄR
        elif y1 < 0: # Kui madu liigub ülevalt äärest välja
            y1 = screeny - grid_size # Liigub alt äärest tagasi

    # MAO POSITSIOON EKRAANIL
    snake_head = [x1, y1]  # Mao pea uus asukoht

    # Lisab uue asukoha mao keha listi + PÜSIV keha pilt
    snake_list.append([x1, y1, snake_direction, random.choice(snake_body_images)])

    # Kui list on liiga pikk (madu ei kasva)
    if len(snake_list) > length_of_snake:
        snake_list.pop(0)

        # HITBOXID
        head_rect = pygame.Rect(x1, y1, grid_size, grid_size)  # Pea hitbox, et tuvastada kokkupõrget
        food_rect = pygame.Rect(foodx, foody, food_size, food_size)  # Toidu hitbox, et tuvastada kokkupõrget

        # KOKKUPÕRGE TOIDUGA
        if head_rect.colliderect(food_rect):  # Kui mao pea põrkub kokku toiduga
            length_of_snake += 1  # Mao keha pikkus kasvab ühe pildi võrra

    # UUE TOIDUPILDI KUVAMINE
            foodx = random.randrange(0, screenx // grid_size) * grid_size  # Uus random x-koordinaat toidule
            foody = random.randrange(0, screeny // grid_size) * grid_size  # Uus random y-koordinaat toidule
            current_food = random.choice(food_images)  # Uus juhuslik toidupilt listist ja lisab selle ekraanile

    # KIIRUS KASVAB, KUI MADU SÖÖB TOITU
            new_snake_speed = min(new_snake_speed + 1, 60)
        # Mao uus kiirus on vana kiirus + 1, seab FPS kiirusele piirangu

    # KOKKUPÕRGE ISEENDAGA
        for segment in snake_list[:-1]: # Käib läbi kõik mao kehaosad
            if segment[:2] == snake_head: # Kokkupõrkel iseeendaga -
                return False # Lõpetab mängutsükli - kuvab kaotuse oleku

    # OBJEKTIDE JA SKOORI KUVAMINE
        screen.blit(current_background, (0, 0)) # Kuvab mängu tausta
        screen.blit(current_food, (foodx, foody)) # Kuvab toidupildi
        draw_snake(snake_list, snake_direction) # Kuvab mao õigesti ekraanile
        show_score(length_of_snake - 1) # Kuvab mängija skoori

        pygame.display.flip() # Uuendab ekraani
        clock.tick(int(new_snake_speed)) # Kasutab uut mao kiirust

    return False # Tagastab False - mäng lõpeb

# --- MÄNGIJA NIME SISESTUS MÄNGUAKNAS ---
player_name = ask_name() # Küsib mängija nime

# --- MÄNGU PÕHITSÜKKEL ---
running = True # Kontrollib, kas mäng töötab
while running: # Töötab, kuni "running" on True
    running = gameloop() # Käivitab mängutsükli

pygame.quit() # Sulgeb PyGame'i
quit() # Lõpetab programmi