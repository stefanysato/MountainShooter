import pygame

print('Setup Start')
pygame.init()
window = pygame.display.set_mode(size=(800, 600))
print('Setup Finish')

print('Loop Start')
while True:
    # check for all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # close window
            quit() # end pygame