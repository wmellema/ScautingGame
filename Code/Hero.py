import Ragnarok as r
import math
from TileHeroCharacter import TileHeroCharacter
import pygame



class Hero(TileHeroCharacter):

    def __init__(self, tileMap, GameScreen):
        super(Hero,self).__init__(tileMap,GameScreen)

        # Some of the variables used for physics and stuff
        block_jump_height = 6
        tile_height = 16
        fall_acceleration= 8 * tile_height
        self.jump_velocity = math.sqrt(2 * (fall_acceleration) * (block_jump_height * tile_height))
        self.run_speed = 145
        self.velocity = r.Vector2()
        self.acceleration = r.Vector2(0, fall_acceleration)

    def __step(self, old_pos, desired_pos):
        super().step(old_pos,desired_pos,True)
        collisions = r.TileMapManager.active_map.grab_collisions(r.Vector2(old_pos.X, self.coords.Y))
        check_horizontal = True
        for collision in collisions:
            if "Hazard" in collision.binding_type:
                self.hazard_touched_method(self)
                check_horizontal = False
                collisions = []
                break


        if check_horizontal:
            collisions = r.TileMapManager.active_map.grab_collisions(r.Vector2(self.coords.X, old_pos.Y))
            for collision in collisions:
                if "Hazard" in collision.binding_type:
                    '''
                    =================================
                    Do something with this collision!
                    If this is difficult: ask!
                    =================================
                    '''
                    pass

        self.desired_position = self.coords

    def __update_movement(self):
        old_pos = self.coords.copy()
        previous_position = self.coords.copy()
        direction = self.desired_position - old_pos
        y_step_count = int(abs(direction.Y) / 16) + 1
        x_step_count = int(abs(direction.X) / 16) + 1

        #This code prevents the block from ever moving more than one block per update cycle.
        if y_step_count > 1:
            old_pos = self.tile_map.pixels_to_tiles(old_pos)
            old_pos = self.tile_map.tiles_to_pixels(old_pos)
            self.desired_position.Y = old_pos.Y + (16 * r.sign(direction.Y))

        if x_step_count > 1:
            old_pos = self.tile_map.pixels_to_tiles(old_pos)
            old_pos = self.tile_map.tiles_to_pixels(old_pos)
            self.desired_position.X = old_pos.X + (16 * r.sign(direction.X))

        self.__step(old_pos, self.desired_position)

    def __handle_input(self, milliseconds):
        if r.Ragnarok.get_world().Keyboard.is_down(pygame.K_RIGHT):
            self.desired_position += r.Vector2(self.run_speed * (milliseconds / 1000.0), 0)
        '''
        Code for going left. TIP! Inverse of right!
        '''

        if r.Ragnarok.get_world().Keyboard.is_down(pygame.K_UP):
            if self.CURRENT_STATE != self.JUMPING_STATE:
                self.velocity = r.Vector2(0, -self.jump_velocity)
                self.CURRENT_STATE = self.JUMPING_STATE

    def update(self, milliseconds):
        if not self.is_paused:
            self.velocity += self.acceleration * (milliseconds / 1000.0)
            self.desired_position += self.velocity * (milliseconds / 1000.0)
            self.__update_movement()
            self.__handle_input(milliseconds)
            self.bounding_box.x = self.coords.X
            self.bounding_box.y = self.coords.Y
            r.Ragnarok.get_world().Camera.desired_pan = self.coords
            super(TileHeroCharacter, self).update(milliseconds)
