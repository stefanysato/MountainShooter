#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import pygame

from code.Const import ENTITY_HEALTH


# CLASSE MODELO
class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = pygame.image.load('./assets/' + name + '.png').convert_alpha()
        # convert_alpha => converte a imagem para o mesmo formato de pixel do display surface principal
        # aumenta a performance do jogo; pode ser usado o .convert() também
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0
        self.health = ENTITY_HEALTH[self.name]

    @abstractmethod
    def move(self, ):
        pass
