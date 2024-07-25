from pygame.locals import *
import os

def load_map(MAP):
    import pygame, time, sys, json

    pygame.init()


    FPS = 144

    WIDTH, HEIGHT = 1062, 625
    screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
    clock = pygame.time.Clock()

    screen_surf = pygame.Surface((WIDTH, HEIGHT))
    country_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)

    map_s = open("data\\map.txt", "r").read()


    # INTERFACE #

    Map = pygame.image.load(f"maps/{MAP}/{MAP}.png").convert_alpha()
    Map = pygame.transform.scale(Map, (WIDTH - 200, 500))

    MapColors = pygame.image.load(f"maps/{MAP}/{MAP}_c.png").convert_alpha()
    MapColors = pygame.transform.scale(MapColors, (WIDTH - 200, 500))

    MapOutline = pygame.image.load(f"maps/{MAP}/{MAP}_o.png").convert_alpha()
    MapOutline = pygame.transform.scale(MapOutline, (WIDTH - 200, 500))

    Main_Cursor = pygame.image.load("assets/interface/cursor/cursor.png").convert_alpha()


    Port = pygame.image.load("assets/interface/icons/port.png").convert_alpha()
    Port = pygame.transform.scale(Port, (54 // 2, 54 // 2))

    Star = pygame.image.load("assets/interface/icons/capital.png").convert_alpha()
    Star = pygame.transform.scale(Star, (54 // 2, 54 // 2))



    map_config_file = open(f'maps/{MAP}/config.json')
    map_config_file = json.load(map_config_file)

    for i in map_config_file['Provinces']:
        province_colors = i['province_colors']
        borders = i['borders']
        ports = i['ports']

        exec(borders)

    map_provinces = []

    country_color = (145, 23, 23)

    countrys_in_game = []



    capitals = []
    capitals_index = {} # isnt used yet

    # for country in countrys:
    #     capitals.append(int(full_country_data[country].replace(',', '').split(" ")[6]))

    # for country in countrys:
    #     capitals_index[country] = int(full_country_data[country].replace(',', '').split(" ")[6])


    prev_time = time.time()
    draw_province = False
    grab = False


    map_pos = (WIDTH // 2 - Map.get_width() // 2, HEIGHT // 2 - Map.get_height() // 2)
    hover_province_color = (245, 200, 66)

    Map_Rect = pygame.Rect(map_pos[0], map_pos[1], Map.get_width(), Map.get_height())

    cc_r, cc_g, cc_b = country_color[0] - 75, country_color[1] - 75, country_color[2] - 75

    if cc_r < 0: cc_r = 0
    if cc_g < 0: cc_g = 0
    if cc_b < 0: cc_b = 0

    flagged_province_color = (cc_r, cc_g, cc_b)


    border_province_color = (70, 190, 15)

    provinces = {
        # 1: (255, 0, 0), map_provinces_mask, map_province, rect, border_rect
    }

    province_to_draw = None

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


    original_screen_size = (1062, 625)

    centroids = CalculateCentroids(ports)
    capital_centroids = CalculateCentroids(capitals)
    country_provinces_centroids = CalculateCentroids(map_provinces, make_dict=True)

    LoadMap()


    while True:

        mx, my = pygame.mouse.get_pos()

        if screen.get_size() != original_screen_size: # adjust sensetivity to resizing screen
            mx *= original_screen_size[0] / screen.get_size()[0]
            my *= original_screen_size[1] / screen.get_size()[1]

        pygame.mouse.set_visible(False)
        

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:    # last elif so when interacting with ui it dont move map around
                current_image = 0

                province_mask_x, province_mask_y = mx - map_province_rect.x, my - map_province_rect.y

        province_mask_x, province_mask_y = mx - map_province_rect.x, my - map_province_rect.y

        screen_surf.fill((255, 255, 255))

        screen_surf.blit(Map, map_pos) # 250 is half of the height for the map images

        

        #MapColors.set_alpha(50)
        #screen_surf.blit(MapColors, map_pos)

        draw_province = False

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

        if flagged : # Hovering Over A Province
                
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

        
        if draw_province: # Hovering Over A Province
                
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

        screen_surf.blit(MapOutline, map_pos)

        for center in centroids: # Draw Icons
            offset = (-20, -10)
            screen_surf.blit(Port, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))

        for center in capital_centroids: # Draw Icons
            offset = (-20, -10)
            screen_surf.blit(Star, (center[0] + map_pos[0] + offset[0], center[1] + map_pos[1] + offset[1]))


        screen_surf.blit(Main_Cursor, (mx, my))
        
        
        screen.blit(pygame.transform.scale(screen_surf, screen.get_rect().size), (0, 0))

        pygame.display.set_caption(f'Inimi de fier 5 | FPS : {str(round(clock.get_fps(), 2))}')
        

        pygame.display.flip()

        clock.tick(FPS)

print("\nMap Name")

x = input(" --> ")

os.chdir("..")
if x in os.listdir("maps"):
    load_map(x)