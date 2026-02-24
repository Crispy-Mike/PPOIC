import pygame

class Button:
    def __init__(self,x,y,height,width,text,screen):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.rect=pygame.Rect(x,y,width,height)
        self.active=False
        self.text=text
        self.text_color = (255, 255, 255)
        self.color=(100,100,100)
        self.font=pygame.font.Font(None, 36)
        self.screen=screen


    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
        pygame.draw.rect(self.screen,(0,0,0),self.rect,2)
        text_surface=self.font.render(self.text, True, self.text_color)
        text_rect=text_surface.get_rect(center=self.rect.center)

        self.screen.blit(text_surface,text_rect)