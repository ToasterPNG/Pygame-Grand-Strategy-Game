from pygame.locals import *
import pygame, time, sys, json, requests, threading, os, ast, random

pygame.init()

"""

NOTES :
  map.json can only give countrys provinces that border them (more than that now)

increase military power button : 1, 0.75, 0.5, 0.25, (0.25) <-- repeating ✔

before release : 
  military power                                      ✔
  forts,                                              ✔
  different ideologies,
  server menu,                                        ✔
  ability to pick flag and country name and color,
  capitals,                                           ✔
  more maps,                                          ✔
  can play game with more than 2 people               ✔
  othersssss................

"""

FPS = 144

WIDTH, HEIGHT = 1062, 625
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
clock = pygame.time.Clock()

screen_surf = pygame.Surface((WIDTH, HEIGHT))
country_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)

map_s = open("data\\map.txt", "r").read()

MAP = map_s
NAME = "noname"

server_id_file = open("data\\server_id.txt", "r")
server_link = open("data\\current_server.txt", "r").read()

NAME = open("data\\player.txt", "r").read().strip().replace("\n", "")

SERVER = int(server_id_file.read()) # 1-5

turn = 0

# INTERFACE #

Map = pygame.image.load(f"maps/{MAP}/{MAP}.png").convert_alpha()
Map = pygame.transform.scale(Map, (WIDTH - 200, 500))

MapColors = pygame.image.load(f"maps/{MAP}/{MAP}_c.png").convert_alpha()
MapColors = pygame.transform.scale(MapColors, (WIDTH - 200, 500))

MapOutline = pygame.image.load(f"maps/{MAP}/{MAP}_o.png").convert_alpha()
MapOutline = pygame.transform.scale(MapOutline, (WIDTH - 200, 500))

# could make this a for loop but i nono want to use exec command so much anymore

if os.path.exists("assets/interface/0.png"):
    flag_0 = pygame.image.load("assets/interface/0.png").convert()
    flag_0 = pygame.transform.scale(flag_0, (640 // 7, 384 // 7))

    flag_0.set_alpha(180)

if os.path.exists("assets/interface/1.png"):
    flag_1 = pygame.image.load("assets/interface/1.png").convert()
    flag_1 = pygame.transform.scale(flag_1, (640 // 7, 384 // 7))

    flag_1.set_alpha(180)

if os.path.exists("assets/interface/2.png"):
    flag_2 = pygame.image.load("assets/interface/2.png").convert()
    flag_2 = pygame.transform.scale(flag_2, (640 // 7, 384 // 7))

    flag_2.set_alpha(180)

if os.path.exists("assets/interface/3.png"):
    flag_3 = pygame.image.load("assets/interface/3.png").convert()
    flag_3 = pygame.transform.scale(flag_3, (640 // 7, 384 // 7))

    flag_3.set_alpha(180)

if os.path.exists("assets/interface/4.png"):
    flag_4 = pygame.image.load("assets/interface/4.png").convert()
    flag_4 = pygame.transform.scale(flag_4, (640 // 7, 384 // 7))

    flag_4.set_alpha(180)

Main_Cursor = pygame.image.load("assets/interface/cursor/cursor.png").convert_alpha()
Fort_Cursor = pygame.image.load("assets/interface/cursor/cursor_build_fort.png").convert_alpha()

current_cursor = Main_Cursor

Flag = pygame.image.load("assets/interface/flag.png").convert()
Flag = pygame.transform.scale(Flag, (640 // 4, 384 // 4))

Port = pygame.image.load("assets/interface/icons/port.png").convert_alpha()
Port = pygame.transform.scale(Port, (54 // 2, 54 // 2))

Star = pygame.image.load("assets/interface/icons/capital.png").convert_alpha()
Star = pygame.transform.scale(Star, (54 // 2, 54 // 2))

Fort = pygame.image.load("assets/interface/icons/fort.png").convert_alpha()
Fort = pygame.transform.scale(Fort, (54 // 2, 54 // 2))

Capture_Button = pygame.image.load("assets/interface/buttons/capture.png").convert_alpha()
Capture_Button = pygame.transform.scale(Capture_Button, (200, 60))

MP_Button = pygame.image.load("assets/interface/buttons/militarypower.png").convert_alpha()
MP_Button = pygame.transform.scale(MP_Button, (60, 60))

Fort_Button = pygame.image.load("assets/interface/buttons/buildfort.png").convert_alpha()
Fort_Button = pygame.transform.scale(Fort_Button, (60, 60))

debug_font = pygame.font.Font('assets/fonts/DebugFont.ttf', 16)
debug_font_sm = pygame.font.Font('assets/fonts/DebugFont.ttf', 12)

debug_text = debug_font.render(f'turn : {turn}', True, (0, 0, 0))
invasion_text = debug_font.render(f'No Invasion', True, (0, 0, 0))
invasion_text_two = debug_font.render(f'...', True, (0, 0, 0))

player_invasion_data = 0

mp_list = [1, 0.75, 0.5, 0.25]
mp_list_pos = 0

mp_stop = False

# OTHER VARS #

map_config_file = open(f'maps/{MAP}/config.json')
map_config_file = json.load(map_config_file)

for i in map_config_file['Provinces']:
    province_colors = i['province_colors']
    borders = i['borders']
    ports = i['ports']

    exec(borders)

country_keys = []
map_provinces = []

def load_map_json():
    global countrys, countrys_data, countrys_in_game, country_keys, invasion_text, invasion_text_two, full_country_data, forts, map_provinces, last_province_invaded, land_military_power, player_id, capitals, capitals_index, player_invasion_data

    country_keys = []

    info_config_file = open(f'data/info.json')
    info_config_file = json.load(info_config_file)

    for i in info_config_file['Countrys']:
        exec_string = f"global countrys_data; countrys_data = dict({i})"



        exec(exec_string)
        num = -1

        i = -1

        for key in countrys_data:
            i += 1
            if key == NAME:
                player_id = i
                break


        for key in countrys_data:
            num += 1
            exec_string = f"global country_{num}; country_{num} = {countrys_data[key]}; countrys_in_game.append(country_{num})"

            country_keys.append(key)

            exec(exec_string)
        
        

        for key in countrys_data:
        
            if key == NAME:

                player_invasion_data = ast.literal_eval(countrys_data[NAME])[3]
            else:
                enemy_invaion_data = ast.literal_eval(countrys_data[key])[3]
                player_invasion_data = 0
                enemy_key = key

        if player_invasion_data != 0 and enemy_invaion_data != 0:
            if player_invasion_data >= enemy_invaion_data:
                invasion_text = debug_font.render(f'{NAME} : {round(player_invasion_data, 2)}, {enemy_key} : {round(enemy_invaion_data, 2)}', True, (10, 180, 10))
                invasion_text_two = debug_font.render('Defended Successfully', True, (10, 180, 10))
            else:
                invasion_text = debug_font.render(f'{NAME} : {round(player_invasion_data, 2)}, {enemy_key} : {round(enemy_invaion_data, 2)}', True, (180, 10, 10))
                invasion_text_two = debug_font.render('Defended Unsuccessfully', True, (180, 10, 10))
        else:
            invasion_text = debug_font.render(f'No Invasions', True, (0, 0, 0))

    print(country_keys)

    full_country_data = eval(str(dict(info_config_file)["Countrys"]).replace("[", "").replace("]", ""))
    land_military_power = float(dict(full_country_data)[NAME].replace(',', '').split(" ")[7])


    for i in info_config_file['Map']:
        exec_string = f"global countrys; countrys = {i}"

        exec(exec_string)

        for country in countrys:
            for prov in countrys[country]:
                map_provinces.append(prov)

    capitals = []
    capitals_index = {}

    for country in countrys:
        capitals.append(int(full_country_data[country].replace(',', '').split(" ")[6]))

    for country in countrys:
        capitals_index[country] = int(full_country_data[country].replace(',', '').split(" ")[6])
        
    forts = info_config_file['Forts'][0]

    last_province_invaded = info_config_file['Data'][0]['mri']

def download_server_json():
    
    url = f'{server_link}/return_data'

    print("Downloading Server Data")
    
    os.system('del data\\server_data.json')

    with requests.get(url, stream=True) as r: # for downloading server data ONCE
        r.raise_for_status()
        with open('data\\server_data.json', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def download_map_json():

    global flagged
    
    url = f'{server_link}{SERVER}/map'

    print("Downloading Map")
    
    os.system('del data\\info.json')

    with requests.get(url, stream=True) as r: # for downloading map on startup of game
        r.raise_for_status()
        with open('data/info.json', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    flagged = False
    file_not_downloaded = True

    while file_not_downloaded: # not for initial download
        if os.path.isfile("data\\info.json"):
            if os.path.getsize("data\\info.json") > 0:
                load_map_json()
                file_not_downloaded = False


def add_outline_to_image(image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (255, 0, 255)) -> pygame.Surface:
    mask = pygame.mask.from_surface(image)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))

    new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
    new_img.fill(color_key)
    new_img.set_colorkey(color_key)

    for i in -thickness, thickness:
        new_img.blit(mask_surf, (i + thickness, thickness))
        new_img.blit(mask_surf, (thickness, i + thickness))
    new_img.blit(image, (thickness, thickness))

    return new_img

descriptive_text_mp = debug_font_sm.render("MP", False, (0, 0, 0)).convert()
descriptive_text_mp = add_outline_to_image(descriptive_text_mp, 2, (255, 255, 255))

descriptive_text_invade = debug_font_sm.render("Invade", False, (0, 0, 0)).convert()
descriptive_text_invade = add_outline_to_image(descriptive_text_invade, 2, (255, 255, 255))

descriptive_text_forts = debug_font_sm.render("Forts", False, (0, 0, 0)).convert()
descriptive_text_forts = add_outline_to_image(descriptive_text_forts, 2, (255, 255, 255))

last_province_invaded = 1

country_color = (145, 23, 23)
open_capital = False

countrys_in_game = []



info_config_file = open(f'data/info.json')
info_config_file = json.load(info_config_file)

for i in info_config_file['Countrys']:
    exec_string = f"countrys_data = dict({i})"

    exec(exec_string)

    num = -1

    for key in countrys_data:
        num += 1
        exec_string = f"country_{num} = {countrys_data[key]}; countrys_in_game.append(country_{num})"

        country_keys.append(key)

        exec(exec_string)

    for list_ in countrys_in_game:
        if countrys_data[NAME] == str(list_):
            country_data = list_
  
    ideology = country_data[0]
    country_color = country_data[1]
    military_power = country_data[2]
    capital = country_data[4]


countrys = {}

for i in info_config_file['Map']:
    exec_string = f"countrys = {i}"

    exec(exec_string)

full_country_data = eval(str(dict(info_config_file)["Countrys"]).replace("[", "").replace("]", ""))

capitals = []
capitals_index = {} # isnt used yet

# for country in countrys:
#     capitals.append(int(full_country_data[country].replace(',', '').split(" ")[6]))

# for country in countrys:
#     capitals_index[country] = int(full_country_data[country].replace(',', '').split(" ")[6])

download_server_json()
download_map_json()

prev_time = time.time()
draw_province = False
grab = False


# MULTIPLAYER VARS

players_in_server = 2

server_config_file = open(f'data/server_data.json')
server_config_file = json.load(server_config_file)

players_in_server = len(list(server_config_file['Server Data']["players"]))

#player_id = 0
turn = 0

turn_pls = int(turn) + 1
new_turn = False

land_military_power = float(dict(full_country_data)[NAME].replace(',', '').split(" ")[7])

# MULTIPLAYER VARS


map_pos = (WIDTH // 2 - Map.get_width() // 2, HEIGHT // 2 - Map.get_height() // 2)
hover_province_color = (245, 200, 66)

Map_Rect = pygame.Rect(map_pos[0], map_pos[1], Map.get_width(), Map.get_height())
Capture_Button_Rect = pygame.Rect(WIDTH - Capture_Button.get_width() - 100, HEIGHT - Capture_Button.get_height(), Capture_Button.get_width(), Capture_Button.get_height())
MP_Button_Rect = pygame.Rect(WIDTH - MP_Button.get_width() * 6, HEIGHT - MP_Button.get_height(), MP_Button.get_width(), MP_Button.get_height())
Fort_Button_Rect = pygame.Rect(WIDTH - Fort_Button.get_width() * 16.07, HEIGHT - MP_Button.get_height(), Fort_Button.get_width(), Fort_Button.get_height())

cc_r, cc_g, cc_b = country_color[0] - 75, country_color[1] - 75, country_color[2] - 75

if cc_r < 0: cc_r = 0
if cc_g < 0: cc_g = 0
if cc_b < 0: cc_b = 0

flagged_province_color = (cc_r, cc_g, cc_b)


border_province_color = (70, 190, 15)

owned_provinces = [5]
forts = {"1": [], "2": [], "3": []} # forts can be 3 levels 1/3, 2/3, 3/3

provinces = {
    # 1: (255, 0, 0), map_provinces_mask, map_province, rect, border_rect
}

annexed_provinces = [5, 6, 7]
province_to_draw = None
prov_to_annex = None
placing_forts = False

debugging = False
flagged = False

# FUNCTIONS #

def ColorMask(image, mask_color):
    mask_image = image.convert_alpha()
    mask_image.set_colorkey(mask_color)
    #mask_image.set_colorkey((0, 0, 0))
    mask = pygame.mask.from_surface(mask_image)
    mask.invert()
    return mask

def LoadMap():
    global annexed_provinces, country_provinces_centroids

    for key in countrys:
        if key == NAME:
            annexed_provinces = countrys[key]
        else:
            
            for list_ in countrys_in_game:
                if countrys_data[key] == str(list_):
                    temp_country_color = list_[1]

            for prov in countrys[key]: # Draw Country
                bordering_province_hover = provinces[prov + 1][2].copy().convert_alpha()
                #bordering_province_hover.set_alpha(120)
            
                pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), temp_country_color, 1, None, True)
            
                country_surf.blit(bordering_province_hover, map_pos)
                # for province_id in borders[prov]:
                #     if province_id in countrys[key]:
def LoadProvinces():
    global provinces, map_pos

    num = 0

    #border_scale = 1.05

    for color in province_colors:
        num += 1

        map_provinces_mask = ColorMask(MapColors, color)

        map_province = map_provinces_mask.to_surface().convert_alpha()
        map_province.set_colorkey((0, 0, 0))

        rect = map_province.get_rect(topleft = (0, 0))

        #border_mask = ColorMask(pygame.transform.scale(map_province, (map_province.get_width() * border_scale, map_province.get_height() * border_scale)), (255, 255, 255))
        #border_offset = (border_scale * 32, border_scale * 22)

        # automatic border detection stuff ^^^^^

        provinces[num] = color, map_provinces_mask,map_province, rect

    

LoadProvinces()
LoadMap()

#print(provinces)

for province in provinces:
    map_province_rect = provinces[province][2].get_rect(topleft = (map_pos[0], map_pos[1]))

def CalculateCentroids(list, make_dict=False):
    if not make_dict:

        centroids = []

        for province in list:
            surf = provinces[province + 1][1].to_surface()
            surf.set_colorkey((0,0,0))

            centroids.append(pygame.mask.from_surface(surf).centroid())

        return centroids
    else:
        centroids = {}

        for province in list:
            surf = provinces[province + 1][1].to_surface()
            surf.set_colorkey((0,0,0))

            centroids[province] = pygame.mask.from_surface(surf).centroid()

        return centroids

def CalculateProbabilityOfTile(mp_1, mp_2, fort_level):
    return 50 * mp_1 - 50 * mp_2 * fort_level


def update_map_json(prov, Turn, invasion=False, numbers=[0, 0]):
    global full_country_data, json_data, military_power, land_military_power, country_color

    info_config_file = open(f'data/info.json')
    info_config_file = json.load(info_config_file)

    if open_capital:
        prov -= 1
    
    if not invasion:
        if prov not in info_config_file['Map'][0][NAME]:
            if prov != None:
                info_config_file['Map'][0][NAME].append(prov)
            info_config_file['Data'][0]['turn'] = int(Turn)
            info_config_file['Data'][0]['mri'] = int(last_province_invaded)
            info_config_file['Forts'][0] = forts

            mp_data_one = ast.literal_eval(info_config_file['Countrys'][0][NAME])

            mp_data_one[1] = country_color
            mp_data_one[2] = military_power
            mp_data_one[4] = capital
            mp_data_one[5] = float(land_military_power)
            
            
            info_config_file['Countrys'][0][NAME] = str(mp_data_one)
            full_country_data = eval(str(dict(info_config_file)["Countrys"]).replace("[", "").replace("]", ""))

    else:
        if prov not in info_config_file['Map'][0][NAME]:
            info_config_file['Data'][0]['turn'] = int(Turn)
            info_config_file['Data'][0]['mri'] = int(last_province_invaded)
            info_config_file['Forts'][0] = forts

            invasion_data_one = ast.literal_eval(info_config_file['Countrys'][0][NAME])
            invasion_data_two = ast.literal_eval(info_config_file['Countrys'][0][invasion])

            
            #del invasion_data_one[3]; del invasion_data_two[3]

            invasion_data_one[3] = numbers[0]; invasion_data_two[3] = numbers[1]

            invasion_data_one[4] = capitals_index[NAME]; invasion_data_two[4] = capitals_index[invasion]

            if numbers[0] >= numbers[1]:
                info_config_file['Map'][0][invasion].remove(prov)
                info_config_file['Map'][0][NAME].append(prov)

                invasion_data_two[5] = float(ast.literal_eval(info_config_file['Countrys'][0][invasion])[5]) - 0.25
                land_military_power += 0.25
            else:
                invasion_data_two[5] = float(ast.literal_eval(info_config_file['Countrys'][0][invasion])[5])

            invasion_data_one[5] = float(land_military_power)
    
            info_config_file['Countrys'][0][NAME] = str(invasion_data_one)
            info_config_file['Countrys'][0][invasion] = str(invasion_data_two)
            
    json_data = info_config_file

    with open('data/info.json', 'w', encoding='utf-8') as json_file:
        json.dump(info_config_file, json_file)

        print('JSON file updated successfully')

def upload_map_json():
    global country_provinces_centroids
    url = f'{server_link}{SERVER}/upload_redirect'
    nm = 'data/info.json'

    country_provinces_centroids = CalculateCentroids(map_provinces, make_dict=True)


    nmrb = open(nm, 'rb')

    files = [('file', nmrb)]

    r = requests.post(url, files=files)

    if r.ok:
        print("Uploaded JSON Succesfully")
    else:
        print("Error when trying to upload JSON to server !!!")

    nmrb.close()

def draw_country(Turn):
    global invasion_text, invasion_text_two, last_province_invaded, land_military_power, capital_centroids, capitals, open_capital, capital

    for prov in annexed_provinces: # Draw Country
        for province_id in borders[prov]:
            if province_id in annexed_provinces or open_capital:

                for key in countrys:
                    if key != NAME:
                        if province_id in countrys[key]:
                            in_another_country = True
                            print(province_id, countrys[key])
                            break
                        else:
                            in_another_country = False
                    

                if not open_capital:
                    if in_another_country:

                        last_province_invaded = province_id
                        
                        # countrys_data[key] -> ['f', [207, 174, 43], 4]

                        rand1 = random.randint(10, 50) / 100
                        rand2 = random.randint(10, 50) / 100
                        
                        fort_multiplier = 1

                        for fort_level in forts:
                            for prov in forts[fort_level]:
                                if prov == province_id:
                                    fort_multiplier = int(fort_level) // 2 + 1.5

                        invaded_land_multiplier = float(dict(full_country_data)[key].replace(',', '').split(" ")[7])

                        print(rand1, rand2, "--", rand1 * military_power * land_military_power, rand2 * ast.literal_eval(countrys_data[key])[2] * fort_multiplier * invaded_land_multiplier)

                        print(fort_multiplier)

                        invasion_text = debug_font.render(f'{NAME} : {round(rand1 * military_power * land_military_power, 2)}, {key} : {round(rand2 * ast.literal_eval(countrys_data[key])[2] * fort_multiplier * invaded_land_multiplier, 2)}', True, (180, 10, 10))
                        invasion_text_two = debug_font.render('Invaded Unsuccessfully', True, (180, 10, 10))

                        if rand1 * military_power * land_military_power >= rand2 * ast.literal_eval(countrys_data[key])[2] * fort_multiplier * invaded_land_multiplier:

                            if province_id != capitals_index[key]:

                                invasion_text = debug_font.render(f'{NAME} : {round(rand1 * military_power * land_military_power, 2)}, {key} : {round(rand2 * ast.literal_eval(countrys_data[key])[2] * fort_multiplier * invaded_land_multiplier, 2)}', True, (10, 180, 10))
                                invasion_text_two = debug_font.render('Invaded Successfully', True, (10, 180, 10))

                                bordering_province_hover = provinces[province_id + 1][2].copy().convert_alpha()
                            
                                pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), country_color, 1, None, True)
                            
                                country_surf.blit(bordering_province_hover, map_pos)
                                countrys[key].remove(province_id)





                                update_map_json(province_id, Turn, invasion=key, numbers=[rand1 * military_power * land_military_power, rand2 * ast.literal_eval(countrys_data[key])[2] * fort_multiplier * invaded_land_multiplier])

                                break
                            else:
                                invasion_text = debug_font.render(f'{NAME} : {round(rand1 * military_power, 2)}, {key} : {round(rand2 * ast.literal_eval(countrys_data[key])[2], 2)}', True, (10, 180, 10))
                                invasion_text_two = debug_font.render('Annexed Successfully', True, (10, 180, 10))

                                bordering_province_hover = provinces[province_id + 1][2].copy().convert_alpha()
                            
                                pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), country_color, 1, None, True)
                            
                                country_surf.blit(bordering_province_hover, map_pos)


                            
                                for element in json_data:
                                    
                                    if element == "Map":

                                        country_provinces = json.loads(str(json_data[element])[1:-1].replace("'", '"'))

                                for province in country_provinces[key]:

                                    countrys[key].remove(province)
                                    annexed_provinces.append(province)

                                    update_map_json(province, Turn, invasion=key, numbers=[rand1 * military_power * land_military_power, rand2 * ast.literal_eval(countrys_data[key])[2] * fort_multiplier * invaded_land_multiplier])
                                break
                        else:
                            annexed_provinces.remove(province_id)

                            update_map_json(None, Turn, invasion=key, numbers=[rand1 * military_power * land_military_power, rand2 * ast.literal_eval(countrys_data[key])[2] * fort_multiplier * invaded_land_multiplier])
                    else:
                        bordering_province_hover = provinces[province_id + 1][2].copy().convert_alpha()
                        #bordering_province_hover.set_alpha(120)
                    
                        pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), country_color, 1, None, True)
                    
                        country_surf.blit(bordering_province_hover, map_pos)

                        #land_military_power += 0.25
                        


                        update_map_json(province_id, Turn)
                else:
                    bordering_province_hover = provinces[prov_to_annex][2].copy().convert_alpha()
                    #bordering_province_hover.set_alpha(120)
                
                    pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), country_color, 1, None, True)
                
                    country_surf.blit(bordering_province_hover, map_pos)

                    #land_military_power += 0.25

                    capital = prov_to_annex - 1

                    capitals = []
                    

                    capitals.append(prov_to_annex - 1)

                    capitals.append(int(full_country_data[NAME].replace(',', '').split(" ")[6]))
                    
                    capital_centroids = CalculateCentroids(capitals)

                    update_map_json(prov_to_annex, Turn)

def get_turn(): # whos turn?
    global turn, turn_pls, new_turn, mp_stop, capitals, capital_centroids
    url = f'{server_link}{SERVER}'

    turn = requests.get(url).text
    turn_pls = int(turn) + 1

    if int(turn) == player_id and not new_turn:
        new_turn = True
        download_map_json()

        mp_stop = False

        #Traceback (most recent call last):
        #File "C:\Users\user\Desktop\hm!\3 - online version\client 1\main.py", line 413, in <module>
        #    debug_text = debug_font.render(f'turn : {country_keys[int(turn)]}', True, (0, 0, 0))
        #IndexError: list index out of range

        load_map_json()
        capital_centroids = CalculateCentroids(capitals)
        LoadMap()

        draw_country(turn)
    elif int(turn) != player_id and new_turn:
        new_turn = False

original_screen_size = (1062, 625)

centroids = CalculateCentroids(ports)
capital_centroids = CalculateCentroids(capitals)
country_provinces_centroids = CalculateCentroids(map_provinces, make_dict=True)
download_map_json()
draw_country(turn)

LoadMap()

if military_power > 1: # [1, 0.75, 0.5, 0.25]
    if military_power == 2:
        mp_list_pos = 1
    elif military_power == 2.75:
        mp_list_pos = 2
    else:
        mp_list_pos = 3

tick = 0
tick_rate = 3

while True:

    mx, my = pygame.mouse.get_pos()

    if screen.get_size() != original_screen_size: # adjust sensetivity to resizing screen
        mx *= original_screen_size[0] / screen.get_size()[0]
        my *= original_screen_size[1] / screen.get_size()[1]

    pygame.mouse.set_visible(False)
    
    dt = time.time() - prev_time
    prev_time = time.time()

    tick += tick_rate * dt

    if tick >= 1:

        print('fixed update')

        last_turn = turn

        t1 = threading.Thread(target=get_turn)
        t1.start()

        tick = 0

    

    if len(country_keys) == players_in_server:

        debug_text = debug_font.render(f'turn : {country_keys[int(turn)]}', True, (0, 0, 0))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SLASH:
                if debugging:
                    debugging = False
                else:
                    debugging = True
            elif event.key == pygame.K_RETURN and int(turn) == player_id:

                if flagged:
                    
                    

                    if turn_pls == players_in_server:
                        turn = '0'
                    else:
                        turn = str(int(turn) + 1)

                    annexed_provinces.append(prov_to_annex - 1)

                    for key in countrys:
                        if key != NAME:
                            if prov_to_annex - 1 in countrys[key]:
                                in_another_country = True
                                break
                            else:
                                in_another_country = False

                    if not in_another_country:
                        land_military_power += 0.25
                    
                    draw_country(turn)
                    upload_map_json()


                    open_capital = False

                    prov_to_annex = None
                    flagged = False

        elif event.type == MOUSEBUTTONDOWN and event.button == 1:    # last elif so when interacting with ui it dont move map around
            current_image = 0

            province_mask_x, province_mask_y = mx - map_province_rect.x, my - map_province_rect.y

        elif event.type == MOUSEBUTTONUP and event.button == 1:
            
            if Capture_Button_Rect.collidepoint((mx, my)) and int(turn) == player_id:
                if flagged:
                    

                    if turn_pls == players_in_server:
                        turn = '0'
                    else:
                        turn = str(int(turn) + 1)

                    annexed_provinces.append(prov_to_annex - 1)

                    for key in countrys:
                        if key != NAME:
                            if prov_to_annex - 1 in countrys[key]:
                                in_another_country = True
                                break
                            else:
                                in_another_country = False

                    if not in_another_country:
                        land_military_power += 0.25
                        
                    draw_country(turn)
                    upload_map_json()

                    open_capital = False

                    prov_to_annex = None
                    flagged = False
            elif MP_Button_Rect.collidepoint((mx, my)) and int(turn) == player_id:
                if not mp_stop:

                    mp_stop = True

                    if mp_list_pos < len(mp_list):
                        military_power += mp_list[mp_list_pos]
                        mp_list_pos += 1
                    else:
                        military_power += 0.25
                            
                    if turn_pls == players_in_server:
                        turn = '0'
                    else:
                        turn = str(int(turn) + 1)

                    update_map_json(None, turn)
                    upload_map_json()
            elif Fort_Button_Rect.collidepoint((mx, my)) and int(turn) == player_id:
                if not placing_forts:
                    placing_forts = True
                    current_cursor = Fort_Cursor
                else:
                    placing_forts = False
                    current_cursor = Main_Cursor

            elif Map_Rect.collidepoint((mx, my)):
                if not placing_forts:
                    flag = False
                    
                    if annexed_provinces != []:
                        for prov in annexed_provinces:
                            for province_id in borders[prov]:
                                if province_id not in annexed_provinces and province_to_draw != None:

                                    print(province_to_draw - 1, province_id)

                                    if province_to_draw - 1 == province_id:
                                        prov_to_annex = province_to_draw
                                        flagged = True
                                    
                                                
                            if flag == True:
                                break
                    else:
                        if province_to_draw != None and province_to_draw - 1 not in capitals:
                            prov_to_annex = province_to_draw
                            open_capital = True
                                
                            flagged = True
                elif int(turn) == player_id:
                    
                    flagged_prov = province_to_draw - 1
                    no_fort_flag = False
                    search = False

                    skip = False

                    if flagged_prov in annexed_provinces:

                        for fort_level in forts:
                            if flagged_prov not in forts[fort_level]:
                                search = True
                        
                        if search:
                            for fort_level in forts:
                                if flagged_prov in forts[fort_level]:
                                    no_fort_flag = False
                                    if fort_level != "3":

                                        forts[str(int(fort_level) + 1)].append(flagged_prov)
                                        forts[fort_level].remove(flagged_prov)
                                        break
                                    else:
                                        skip = True
                                else:
                                    no_fort_flag = True
                            
                            if no_fort_flag:
                                forts["1"].append(flagged_prov)

                        if not skip:

                            if turn_pls == players_in_server:
                                turn = '0'
                            else:
                                turn = str(int(turn) + 1)

                            placing_forts = False
                            current_cursor = Main_Cursor

                            update_map_json(None, turn)
                            upload_map_json()

    province_mask_x, province_mask_y = mx - map_province_rect.x, my - map_province_rect.y

    screen_surf.fill((255, 255, 255))

    screen_surf.blit(Map, map_pos) # 250 is half of the height for the map images

    

    #MapColors.set_alpha(50)
    #screen_surf.blit(MapColors, map_pos)

    draw_province = False

    if int(turn) == player_id:
            

        for province in provinces:
            if map_province_rect.collidepoint((mx, my)) and provinces[province][1].get_at((province_mask_x, province_mask_y)):
                if provinces[province][0] in province_colors:
                    draw_province = True
                    province_to_draw = province
                    province_borders_to_draw = borders[province - 1]


        if debugging: # aiaiai only for the debuggeringers
            for prov in annexed_provinces:
                for province_id in borders[prov]:
                    if province_id not in annexed_provinces:
                        
                        #province_id += 1
                        bordering_province_hover = provinces[province_id + 1][2].copy().convert_alpha()
                        bordering_province_hover.set_alpha(120)
                    
                        pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), border_province_color, 1, None, True)
                    
                        screen_surf.blit(bordering_province_hover, map_pos)



    screen_surf.blit(country_surf, (0, 0))

    if flagged and int(turn) == player_id and not placing_forts: # Hovering Over A Province
            
            #print(province_borders_to_draw)

            province_hover = provinces[prov_to_annex][2].copy().convert_alpha()
            province_hover.set_alpha(190)

        

            #province_hover = hover_cache[province_to_draw - 1]

            #province_to_draw_brd = province_to_draw

            prov_to_annex -= 1

            #print(province_to_draw)

                
            #print(borders[province_to_draw])

            if debugging:
                for province_id in borders[prov_to_annex]:
                    #province_id += 1
                    bordering_province_hover = provinces[province_id + 1][2].copy().convert_alpha()
                    bordering_province_hover.set_alpha(120)
                
                    pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), flagged_province_color, 1, None, True)
                
                    screen_surf.blit(bordering_province_hover, map_pos)
            
            prov_to_annex += 1

            pygame.transform.threshold(province_hover, province_hover,(255, 255, 255), (0,0,0,0), flagged_province_color, 1, None, True)
            
            screen_surf.blit(province_hover, map_pos)

    thistoexec = ""
    
    if draw_province and int(turn) == player_id: # Hovering Over A Province
            
            #print(province_borders_to_draw)

            province_hover = provinces[province_to_draw][2].copy().convert_alpha()
            province_hover.set_alpha(190)

        

            #province_hover = hover_cache[province_to_draw - 1]

            #province_to_draw_brd = province_to_draw

            province_to_draw -= 1

            #print(province_to_draw)

                
            #print(borders[province_to_draw])

            if debugging:
                for province_id in borders[province_to_draw]:
                    #province_id += 1
                    bordering_province_hover = provinces[province_id + 1][2].copy().convert_alpha()
                    bordering_province_hover.set_alpha(120)
                
                    pygame.transform.threshold(bordering_province_hover, bordering_province_hover,(255, 255, 255), (0,0,0,0), border_province_color, 1, None, True)
                
                    screen_surf.blit(bordering_province_hover, map_pos)
            
            province_to_draw += 1

            if not placing_forts:
                pygame.transform.threshold(province_hover, province_hover,(255, 255, 255), (0,0,0,0), hover_province_color, 1, None, True)
                screen_surf.blit(province_hover, map_pos)

                countrys_list = list(countrys)

                print(countrys_list, province_to_draw)

                for country in countrys_list:
                    if province_to_draw - 1 in countrys[country]:
                        if countrys_list.index(country) != player_id:
                            thistoexec = f"screen_surf.blit(flag_{countrys_list.index(country)}, (mx + 20, my + 20))"
            else:
                
                if province_to_draw - 1 in annexed_provinces:
                    pygame.transform.threshold(province_hover, province_hover,(255, 255, 255), (0,0,0,0), (84, 110, 39), 1, None, True)

                    screen_surf.blit(province_hover, map_pos)

                    centers = CalculateCentroids([province_to_draw - 1])

                    Fort_Opacity = Fort.copy()
                    Fort_Opacity.set_alpha(160)

                    for center in centers: # this is stupid there is only one center but CalculateCentroids function takes in list and i cant be bothered to make an option to only take one element
                        if province_to_draw - 1 in ports:
                            offset = (10, -10)
                            screen_surf.blit(Fort_Opacity, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))
                        elif province_to_draw - 1 == capital:
                            offset = (10, -10)
                            screen_surf.blit(Fort_Opacity, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))
                        else:
                            offset = (-20, -10)
                            screen_surf.blit(Fort_Opacity, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))

    screen_surf.blit(MapOutline, map_pos)

    for center in centroids: # Draw Icons
        offset = (-20, -10)
        screen_surf.blit(Port, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))

    for center in capital_centroids: # Draw Icons
        offset = (-20, -10)
        screen_surf.blit(Star, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))

    print(land_military_power)
    for fort_level in forts:
        for fort in forts[fort_level]:

            for prov in country_provinces_centroids:

                if fort == prov:
                    center = country_provinces_centroids[prov]

                    descriptive_text_fort = debug_font_sm.render(f"{fort_level}/3", False, (0, 0, 0)).convert()
                    descriptive_text_fort = add_outline_to_image(descriptive_text_fort, 2, (255, 255, 255))

                    if prov in ports:
                        offset = (10, -10)
                        screen_surf.blit(Fort, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))
                        screen_surf.blit(descriptive_text_fort, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] - offset[1]))

                        
                    elif prov in capitals:
                        offset = (10, -10)
                        screen_surf.blit(Fort, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))
                        screen_surf.blit(descriptive_text_fort, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] - offset[1]))
                    else:
                        offset = (-20, -10)
                        screen_surf.blit(Fort, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))
                        screen_surf.blit(descriptive_text_fort, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] - offset[1]))
        
    # UI

    print(province_to_draw, capitals)

    
    screen_surf.blit(Capture_Button, (WIDTH - Capture_Button.get_width() - 100, HEIGHT - Capture_Button.get_height()))
    screen_surf.blit(MP_Button, (MP_Button_Rect.x, MP_Button_Rect.y))
    screen_surf.blit(Fort_Button, (Fort_Button_Rect.x, Fort_Button_Rect.y))

    screen_surf.blit(descriptive_text_invade, (WIDTH - Capture_Button.get_width() - 100, HEIGHT - descriptive_text_invade.get_height()))
    screen_surf.blit(descriptive_text_mp, (MP_Button_Rect.x, HEIGHT - descriptive_text_mp.get_height()))
    screen_surf.blit(descriptive_text_forts, (Fort_Button_Rect.x, HEIGHT - descriptive_text_forts.get_height()))

    i = 1
    province_invaded_highlight = provinces[last_province_invaded + 1][2].copy().convert_alpha()
    province_invaded_highlight.set_alpha(90)

    pygame.transform.threshold(province_invaded_highlight, province_invaded_highlight,(255, 255, 255), (0,0,0,0), (89, 17, 5), 1, None, True)

    screen_surf.blit(province_invaded_highlight, map_pos)
        
    for country_name in country_keys:
        i += 1
        y_temp = debug_text.get_height() * i



        current_country_data = ast.literal_eval("[" + full_country_data[country_name] + "]")

        temp_debug_text = debug_font_sm.render(f'MP - {country_name} : {current_country_data[4]}', True, (0, 0, 0))
        temp_debug_text = add_outline_to_image(temp_debug_text, 2, (255, 255, 255))
        screen_surf.blit(temp_debug_text, (WIDTH - temp_debug_text.get_width(), y_temp))

    i += 1

    for country_name in country_keys:
        i += 1
        y_temp = debug_text.get_height() * i



        current_country_data = ast.literal_eval("[" + full_country_data[country_name] + "]")

        temp_debug_text = debug_font_sm.render(f'LAND MP - {country_name} : {current_country_data[7]}', True, (0, 0, 0))
        temp_debug_text = add_outline_to_image(temp_debug_text, 2, (255, 255, 255))
        screen_surf.blit(temp_debug_text, (WIDTH - temp_debug_text.get_width(), y_temp))

    screen_surf.blit(debug_text, (WIDTH - debug_text.get_width(), 0))
    screen_surf.blit(invasion_text, (debug_text.get_width(), 0))
    screen_surf.blit(invasion_text_two, (debug_text.get_width(), HEIGHT // 20))


    screen_surf.blit(Flag, (0, 0))
    exec(thistoexec)

    screen_surf.blit(current_cursor, (mx, my))
    
    
    screen.blit(pygame.transform.scale(screen_surf, screen.get_rect().size), (0, 0))

    pygame.display.set_caption(f'Inimi de fier 5 | FPS : {str(round(clock.get_fps(), 2))}')
    

    pygame.display.flip()

    clock.tick(FPS)
