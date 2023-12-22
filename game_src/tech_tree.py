import pygame as pg
import time



class TechTree:
    def __init__(self) -> None:
        pg.init()

        img_know = pg.image.load('./tech_images/knowledge.png')
        img_shop = pg.image.load('./tech_images/shop.png')
        img_atta = pg.image.load('./tech_images/attack.png')

        self.template = pg.image.load('./tech_images/template.png')
        self.img_lock = pg.image.load('./tech_images/locked.png')

        self.font = pg.font.SysFont("mono", 30)
        self.tfont = pg.font.SysFont("helvetica", 12)
        descrip = open('./tech_images/description.txt', 'r')
        self.description = []
        for line in descrip:
            self.description.append(line.strip())

        self.window_dict = {
            "k" : (100, 0, img_know, 2),
            "s" : (20, 185, img_shop, 5),
            "a" : (180, 185, img_atta, 7),
        }


    def render(self, session):
        level = session.hero.level
        tech_tree = session.hero.techtree
        screen = pg.display.set_mode((280, 300), pg.HIDDEN)

        screen.blit(self.template, (0, 0))

        for i, skill in enumerate(self.window_dict):
            tupl = self.window_dict[skill]
            tech_skill_level = tech_tree[[x for x, i in enumerate(tech_tree) if i.shortname == skill][0]].level
            if level < tupl[3]:
                img = self.img_lock
            else:
                img = tupl[2]
                try:
                    desc = self.description[i].split('%')[tech_skill_level]
                except:
                    desc = ' '
                if len(desc) > 20:
                    desc1, desc2 = ' '.join(desc.split(' ')[:3]), ' '.join(desc.split(' ')[3:])
                    text1, text2 = self.tfont.render(desc1, True, "white"), self.tfont.render(desc2, True, "white")
                    screen.blit(text1, (tupl[0]+40-(text1.get_width()/2), tupl[1] + 80))
                    screen.blit(text2, (tupl[0]+40-(text2.get_width()/2), tupl[1] + 95))
                else:
                    text = self.tfont.render(desc, True, "white")
                    screen.blit(text, (tupl[0]+40-(text.get_width()/2), tupl[1] + 80))
            screen.blit(img, (tupl[0], tupl[1]))
            if tech_skill_level != 0:
                cimg = self.font.render(str(tech_skill_level), True, "white")
                screen.blit(cimg, (tupl[0] + 55, tupl[1] + 45))
        

        pg.display.flip()
        pg.image.save(screen, './tech_images/image.png')


'''```tech_tree = {"know": 4, "atta": 3, "shop": 0}
render(5, tech_tree)
'''