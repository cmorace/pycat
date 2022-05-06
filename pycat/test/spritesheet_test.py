from pycat.core import Window, Sprite, Point

from pycat.experimental.spritesheet import UniversalLPCSpritesheet
from pycat.experimental.animation import Animator

window = Window()

lpc_spritesheet = UniversalLPCSpritesheet('img/lpc_test_spritesheet.png')

class AnimatedSprite(Sprite):
    def on_create(self):
        self.scale = 2
        self.animator = Animator({
            'hurt': lpc_spritesheet.get_textures_by_pattern('hurt'),
            'shoot_right': lpc_spritesheet.get_textures_by_pattern('shoot_right'),
            'slash_right': lpc_spritesheet.get_textures_by_pattern('slash_right'),
            'walk_right': lpc_spritesheet.get_textures_by_pattern('walk_right'),
            'smash_right': lpc_spritesheet.get_textures_by_pattern('smash_right'),
            'cast_right': lpc_spritesheet.get_textures_by_pattern('cast_right'),

            'idle_right': lpc_spritesheet.get_textures_by_pattern('idle_right'),
            'idle_left': lpc_spritesheet.get_textures_by_pattern('idle_left'),
            'idle_up': lpc_spritesheet.get_textures_by_pattern('idle_up'),
            'idle_down': lpc_spritesheet.get_textures_by_pattern('idle_down'),
        })
        self.animator.speed = 0.1

    def on_update(self,dt):
        self.texture = self.animator.tick(dt)
        print(self.animator._frame_idx)


hurt = window.create_sprite(AnimatedSprite, position=Point(100,100))
hurt.animator.play('hurt')

shoot_right = window.create_sprite(AnimatedSprite, position=Point(200,100))
shoot_right.animator.play('shoot_right')

slash_right = window.create_sprite(AnimatedSprite, position=Point(300,100))
slash_right.animator.play('slash_right')

walk_right = window.create_sprite(AnimatedSprite, position=Point(400,100))
walk_right.animator.play('walk_right')

smash_right = window.create_sprite(AnimatedSprite, position=Point(500,100))
smash_right.animator.play('smash_right')

cast_right = window.create_sprite(AnimatedSprite, position=Point(600,100))
cast_right.animator.play('cast_right')


idle_right = window.create_sprite(AnimatedSprite, position=Point(100,300))
idle_right.animator.play('idle_right')

idle_left = window.create_sprite(AnimatedSprite, position=Point(200,300))
idle_left.animator.play('idle_left')

idle_up = window.create_sprite(AnimatedSprite, position=Point(300,300))
idle_up.animator.play('idle_up')

idle_down = window.create_sprite(AnimatedSprite, position=Point(400,300))
idle_down.animator.play('idle_down')

window.run()
