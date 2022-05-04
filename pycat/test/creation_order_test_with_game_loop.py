from pycat.core import Window, Sprite

window = Window()

class Tester(Sprite):
    def on_create(self):
        self.frame = 0
    def on_update(self, dt):
        print('-------------- Start Frame '+str(self.frame)+' ------------------')

        if self.frame == 0:

            s1 = window.create_sprite(tag='one')
            window.dump_all_sprites()
            print('Get sprites: '+str(len(window.get_all_sprites())))
            s1.delete()
            window.dump_all_sprites()


            for _ in range(4):
                window.create_sprite(tag='two')
            window.dump_all_sprites()
            print('Get with tag: '+str(len(window.get_sprites_with_tag('two'))))
            window.delete_sprites_with_tag('two')
            window.dump_all_sprites()

        print('-------------- End Frame '+str(self.frame)+' ------------------')
        window.dump_all_sprites()

        if self.frame > 1:
            self.delete()
        self.frame += 1
        
        


window.create_sprite(Tester, tag='tester')

window.run()

