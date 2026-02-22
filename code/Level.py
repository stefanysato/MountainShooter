#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import COLOR_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator


class Level:
    def __init__(self, window, name, game_mode):
        self.timeout = 20000  # 20 segundos
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # extend -> instancia os objetos da factory e coloca dentro da entity_list
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        # append -> apenas 1 entidade
        self.entity_list.append(EntityFactory.get_entity('Player1'))
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            self.entity_list.append(EntityFactory.get_entity('Player2'))
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)


    def run(self, ):
        pygame.mixer.music.load(f'./assets/{self.name}.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)  # taxa de fps
            for entity in self.entity_list:
                self.window.blit(source=entity.surf, dest=entity.rect)
                entity.move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # o mesmo que quit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            # print text
            self.level_text(text_size=14, text=f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s',
                            text_color=COLOR_WHITE, text_pos=(10, 5))
            self.level_text(text_size=14, text=f'fps: {clock.get_fps() :.0f}', text_color=COLOR_WHITE,
                            text_pos=(10, WIN_HEIGHT - 35))
            self.level_text(text_size=14, text=f'entidades: {len(self.entity_list)}', text_color=COLOR_WHITE,
                            text_pos=(10, WIN_HEIGHT - 20))
            pygame.display.flip()

            # Collisions
            EntityMediator.verify_collision(self.entity_list)
            EntityMediator.verify_health(self.entity_list)


    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Console", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)
