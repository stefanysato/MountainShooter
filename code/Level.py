#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_GREEN, C_CYAN, EVENT_TIMEOUT, \
    TIMEOUT_STEP, TIMEOUT_LEVEL
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # extend -> instancia os objetos da factory e coloca dentro da entity_list
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))

        # append -> apenas 1 entidade
        # self.entity_list.append(EntityFactory.get_entity('Player1'))
        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            # self.entity_list.append(EntityFactory.get_entity('Player2'))
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)  # a cada 100ms verifica condição de vitória

    def run(self, player_score: list[int]):
        pygame.mixer.music.load(f'./assets/{self.name}.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)  # taxa de fps
            for entity in self.entity_list:
                self.window.blit(source=entity.surf, dest=entity.rect)
                entity.move()
                if isinstance(entity, (Player, Enemy)):
                    shoot = entity.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)
                if entity.name == 'Player1':
                    self.level_text(text_size=14, text=f'Player 1 - Health: {entity.health} | Score: {entity.score}',
                                    text_color=C_GREEN, text_pos=(10, 20))
                if entity.name == 'Player2':
                    self.level_text(text_size=14, text=f'Player 2 - Health: {entity.health} | Score: {entity.score}',
                                    text_color=C_CYAN, text_pos=(10, 35))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # o mesmo que quit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout == 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        return True

                found_player = False
                for ent in self.entity_list:
                    if isinstance(ent, Player):
                        found_player = True

                if not found_player:
                    return False

            # print text
            self.level_text(text_size=14, text=f'{self.name} - Timeout: {self.timeout / 1000 :.1f}s',
                            text_color=C_WHITE, text_pos=(10, 5))
            self.level_text(text_size=14, text=f'fps: {clock.get_fps() :.0f}', text_color=C_WHITE,
                            text_pos=(10, WIN_HEIGHT - 35))
            self.level_text(text_size=14, text=f'entidades: {len(self.entity_list)}', text_color=C_WHITE,
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
