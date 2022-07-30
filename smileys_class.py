from time import time
from random import choice, random

from config import *
from crosses import add_cross
from zombies import zombies
from global_items import CreatureStatus, smilies_data, Creature, handle, distance_between_objects, random_attribute, new_pos, smilies, plants, evolution_status

import global_items

FROM = 0
TO = 1
FOOD_PREFERENCE_CHANCE_CHILD = 0.9 # The chance that the child will inherit the food preference of the parent
DEVIATION_OF_RANDOM_PROPERTIES = 0.1 # Proportionates to standard deviation

class Smiley(Creature): # The class of the smileys
    def __init__(
        self,
        generation_n: int,
        energy: float,
        food_preference: str,
        vision_distance: float,
        speed: float,
        procreation_threshold: float,
        colour: tuple,
        species_id: int,
        x: float,
        y: float
    ):
        super().__init__(vision_distance=vision_distance, speed=speed, x=x, y=y)
        self.species_id = species_id
        self.status = CreatureStatus()
        self.status.description = SLEEPING
        self.image_reference = None

        # Setting up the inborn properties of a smiley:
        self.species = colour
        self.food_preference = food_preference
        self.procreation_threshold = procreation_threshold
        self.smart = sum(colour) > 400 # Smart zombies have black eyes and a black mouth

        # Non-inborn properties
        self.generation_n = generation_n
        self.birth_time = time()
        self.energy = energy
        self.stimulus_start = float('-inf')
        self.stimulus = choice(('💀!', '😑', '😐'))
        self.previous_x, self.previous_y = x, y

    @handle
    def D_one_action(self):
        '''Maintaining the behaviour of the smileys.'''
        
        # Using energy of the smiley for a better vision distance
        self.energy -= self.vision_distance*smilies_data['energy_for_vision']

        if self.status.description != SLEEPING: # If the smiley is not sleeping then it is moving (which is obvious)
            self.energy -= self.speed*smilies_data['energy_for_moving']

        # Checking whether it is time for the smiley to die or not
        if self.energy <= 0:
            add_cross(self.x, self.y)
            smilies.remove(self)
            return

        # Check if Wrap is needed (the action of moving a smiley into the opposite side of the evolution field)
        if self.status.description == RUNNING_AWAY: # Only do the Wrap if the smiley we are working with is running away from another smiley
            x_new, y_new = new_pos(self)
            if (x_new, y_new) != (self.x, self.y): # Making sure Wrap is needed
                self.x, self.y = x_new, y_new
                self.status.description = SLEEPING
                for creature in smilies+zombies:
                    if creature.status.description == FOLLOWING_SMILEY and creature.status.parameter is self:
                        creature.status.description = SLEEPING
                return
        
        # Escaping smiley-pursuers
        visible_pursuers = tuple(filter(
            lambda smiley: smiley.status.description == FOLLOWING_SMILEY and 
            smiley.status.parameter is self 
            and distance_between_objects(self, smiley) <= self.vision_distance,
            smilies))
        if visible_pursuers != ():
            dangerous_pursuers = [] # All of the objects of visible_pursuers that can get to the place where self current is not dying on the way towards this
            for pursuer in visible_pursuers:
                distance = distance_between_objects(self, pursuer)
                time = distance/pursuer.speed
                final_energy = pursuer.energy - time*total_energy_loss(pursuer)
                if final_energy > 0: 
                    dangerous_pursuers.append(pursuer)
            if dangerous_pursuers != []: # Escaping the closest pursuers
                closest_pursuer = min(dangerous_pursuers, key=lambda pursuer: distance_between_objects(self, pursuer))
                self.one_step_from(closest_pursuer)
                self.status.description = RUNNING_AWAY
                self.status.parameter = closest_pursuer
                return
        
        # Escaping zombie-pursuers
        visible_pursuers = tuple(filter(
            lambda zombie: zombie.status.description == FOLLOWING_SMILEY 
                and zombie.status.parameter is self 
                and distance_between_objects(self, zombie) <= self.vision_distance,
                zombies))
        if visible_pursuers != (): # Escaping the closest pursuers
            closest_pursuer = min(visible_pursuers, 
                            key=lambda pursuer: distance_between_objects(self, pursuer))
            self.one_step_from(closest_pursuer)
            self.status.description = RUNNING_AWAY
            self.status.parameter = closest_pursuer
            return

        # Escaping the zombie boss
        zombie_boss = evolution_status.zombie_boss
        if zombie_boss is not None:
            # Scarpering from the boss only if it is not asleep
            if not zombie_boss.sleeping:
                if distance_between_objects(self, zombie_boss) < self.vision_distance:
                    self.one_step_from(zombie_boss)
                    self.status.description = RUNNING_AWAY
                    self.status.parameter = None
                    return

        # Escaping the zombies
        dangerous_zombies = tuple(filter(
            lambda zombie: zombie.status.description != SLEEPING 
                and self.vision_distance >= distance_between_objects(self, zombie),
                zombies))
        
        closest_zombie = min(dangerous_zombies, 
                key=lambda zombie: distance_between_objects(self, zombie), default=None)
        if closest_zombie is not None:
            self.one_step_from(closest_zombie)
            self.status.description = RUNNING_AWAY
            self.status.parameter = None
            return

        # Selecting food
        found_smiley = self.find_smiley()
        found_plant = self.find_plant()

        if found_smiley is None and found_plant is None:
            self.status.description = SLEEPING
            return
        elif found_smiley is None and found_plant is not None:
            self.status.description, self.status.parameter = found_plant
        elif found_smiley is not None and found_plant is None:
            self.status.description, self.status.parameter = found_smiley
        else:
            if self.food_preference == SMILIES:
                self.status.description, self.status.parameter = found_smiley
            else:
                self.status.description, self.status.parameter = found_plant    

        # If the smiley chased another smiley and caught it and the energy of the prey was lower than the energy of the catcher, then the prey is eaten by the catcher
        if self.status.description == FOLLOWING_SMILEY:
            prey = self.status.parameter
            self.one_step_to(prey)
            if distance_between_objects(self, prey) <= self.speed:
                if self.energy > prey.energy:
                    self.energy += prey.energy
                    smilies.remove(prey)
                    self.procreate()
                else:
                    self.status.description = SLEEPING   

        # If the smiley is going towards a plant and reaches it, then the plant it eaten
        if self.status.description == FOLLOWING_PLANT:
            plant_prey = self.status.parameter
            self.one_step_to(plant_prey)
            if distance_between_objects(self, plant_prey) <= self.speed:
                self.energy += PLANT_ENERGY
                plants.remove(plant_prey)
                self.procreate()
    
    def one_step(self, object_: object, direction: str):
        '''Stepping from/to an object.'''
        dx, dy = object_.x - self.x, object_.y - self.y
        distance = distance_between_objects(self, object_)
        coeff = self.speed/distance
        if direction == TO:
            self.x, self.y = self.x + coeff*dx, self.y + coeff*dy
        else:
            self.x, self.y = self.x - coeff*dx, self.y - coeff*dy   

    def one_step_from(self, pursuer: object):
        '''Stepping from the pursuer.'''
        self.one_step(pursuer, FROM)

    def one_step_to(self, pursued: object):
        '''Stepping to the pursued smiley.'''
        self.one_step(pursued, TO)

    def find_plant(self) -> tuple[str, object] | None:
        '''Finding the plant which is suitable for self.'''
        feasible_plants = []
        # feasible_plants consists of plants that are qualified as suitable for self by the following conditions:
        # Condition1: The plant is within the vision distance
        # Condition2: The plant is not going to be eaten by any of the smileys with the same species within the vision distance
        other_smileys = set(smilies) - {self}

        for plant in global_items.plants:
            Condition1 = distance_between_objects(self, plant) - global_items.half_plant_size <= self.vision_distance
            if not Condition1:
                continue

            Condition2 = not any(
                smiley.status.description == FOLLOWING_PLANT and
                smiley.status.parameter is plant and
                smiley.species == self.species
                and distance_between_objects(self, smiley) <= self.vision_distance
                for smiley in other_smileys
            )
            if not Condition2:
                continue

            feasible_plants.append(plant)

        if feasible_plants == []:
            return None 

        # far_enough_from_boss is a list which consists of plants which are far enough from the zombie boss
        # Smileys occasionally get stuck on the same spot going toward a plant and straight away being repelled by the zombie boss without this being done
        if evolution_status.zombie_boss is None:
            far_enough_from_zombie_boss = feasible_plants
        else:    
            if evolution_status.zombie_boss.sleeping:
                far_enough_from_zombie_boss = feasible_plants
            else:    
                far_enough_from_zombie_boss = list(filter(
                    lambda plant: distance_between_objects(plant, evolution_status.zombie_boss) > self.vision_distance, 
                    feasible_plants))
        if far_enough_from_zombie_boss == []:
            return None

        if not self.smart:
            return (
                FOLLOWING_PLANT,
                min(far_enough_from_zombie_boss, key=lambda p: distance_between_objects(self, p))
            )

        # It is needed to handle a few more things if the smiley is considered smart
        profitable_plants = [] # The plants that are worth being eaten because the energy which is received from them can make up the energy that was spent to catch them
        for plant in far_enough_from_zombie_boss:
            distance = distance_between_objects(self, plant)
            time = distance/self.speed
            self_final_energy = self.energy - time*total_energy_loss(self)
            if self_final_energy <= 0:
                continue # Self will die before the plant is caught because of a low level of energy
            if self_final_energy + PLANT_ENERGY <= self.energy - time*self.vision_distance*smilies_data['energy_for_vision']:
                continue # It is not worth it to attempt to catch the plant in terms of the energy
            profitable_plants.append(plant)
        
        matchless_plants = [] # The plants from profitable_plants that can be caught by self faster than the competitors without dying
        for plant in profitable_plants:
            self_distance = distance_between_objects(self, plant)
            self_time = self_distance/self.speed

            competitors = filter(
                lambda smiley: smiley.status.description == FOLLOWING_PLANT and smiley.status.parameter is plant,
                other_smileys) # The smileys that are going towards the plant

            faster_competitors = [] # The smileys from competitors that will catch the plant earlier than self (the possibility of them dying on the path towards to plant is not taken into account)
            for smiley in competitors:
                smiley_distance = distance_between_objects(smiley, plant)
                smiley_time = smiley_distance/smiley.speed
                if smiley_time <= self_time:
                    faster_competitors.append({'smiley': smiley, 'time': smiley_time})

            successful_competitors = [] # The smileys from faster_competitors that will catch the plant without dying
            for item in faster_competitors:
                smiley = item['smiley']
                if smiley.energy >= item['time']*total_energy_loss(smiley):
                    successful_competitors.append(smiley)
            
            if successful_competitors == []:
                matchless_plants.append(plant) 
        
        if matchless_plants == []:
            return 
        
        return (
            FOLLOWING_PLANT,
            min(matchless_plants, key=lambda p: distance_between_objects(self, p))
        )
        
    def find_smiley(self) -> tuple[str, object] | None:
        '''Finding the smiley which is suitable for self.'''
        feasible_smileys = []
        # feasible_smileys consists of smileys that are qualified as suitable for self by the following conditions:
        # Condition1: The smiley has different species
        # Condition2: The smiley has a lower amount of energy
        # Condition3: The smiley is within the vision distance
        # Condition4: The smiley is not being chased by any of the smileys with the same species within the vision distance
        
        other_smileys = set(smilies) - {self}

        for another_smiley in other_smileys:
            Condition1 = another_smiley.species != self.species
            if not Condition1:
                continue

            Condition2 = self.energy > another_smiley.energy
            if not Condition2:
                continue

            Condition3 = distance_between_objects(self, another_smiley)-HALF_SMILEY_SIZE <= self.vision_distance
            if not Condition3:
                continue

            Condition4 = not any(
                smiley.status.description == FOLLOWING_SMILEY and
                smiley.status.parameter is another_smiley and
                smiley.species == self.species
                and distance_between_objects(self, smiley) <= self.vision_distance
                for smiley in other_smileys
            )
            if not Condition4:
                continue
            
            feasible_smileys.append(another_smiley)

        if feasible_smileys == []:
            return None

        if not self.smart:
            return (FOLLOWING_SMILEY, 
            min(feasible_smileys, key=lambda s: distance_between_objects(self, s)))

        # It is needed to handle a few more things if the smiley is considered smart
        wholesome_smileys = [] # smileys that are worth being caught by self in terms of the energy (the difference of lost and achieved energy)
        for smiley in filter(lambda smiley: smiley.speed < self.speed, feasible_smileys):
            catch_time = time_to_reach(self, smiley) # Estimation of time which is needed for self to catch smiley
            smiley_final_energy = smiley.energy - catch_time*total_energy_loss(smiley) # Energy of the prey when it is caught (the chance of the prey dying is not considered)
            self_final_energy = self.energy - catch_time*total_energy_loss(self) # Energy of self when it catches the smiley (the chance of self dying is not considered)
            if smiley_final_energy <= 0:
                continue # The smiley will die before it's caught because of a low level of energy
            if self_final_energy <= 0:
                continue # Self will die before it's caught because of a low level of energy
            if self_final_energy + smiley_final_energy <= self.energy - catch_time*self.vision_distance*smilies_data['energy_for_vision']: # Left part of the calculation contains the energy of self when it eats the smiley, and the right part contains the energy of self if it does not attempt to catch the smiley after the same time as if it would attempt to
                continue # It is not worth it to attempt to catch the smiley in terms of the energy
            wholesome_smileys.append(smiley)
        
        profitable_smileys = [] # smileys from wholesome_smileys that can be caught by self quicker than by the rest of the smileys that are current pursuing this smiley
        for smiley in wholesome_smileys:
            self_catch_time = time_to_reach(self, smiley)

            competitors = filter(
                lambda s: s.status.description == FOLLOWING_SMILEY and s.status.parameter is smiley,
                other_smileys) # Competitors for self
            
            if all(c for c in competitors if time_to_reach(c, smiley) > self_catch_time):
                profitable_smileys.append(smiley)
        
        if profitable_smileys == []:
            return None
        return (FOLLOWING_SMILEY, min(profitable_smileys, key=lambda b: distance_between_objects(self, b)))
        
    def one_procreation(self, gap: int):
        '''Creating one child. This function is hereafter used for creating two children.'''
        smiley = Smiley(
            generation_n=self.generation_n+1,
            energy=self.energy/2,
            food_preference=self.food_preference if random() < FOOD_PREFERENCE_CHANCE_CHILD else SMILIES if self.food_preference == PLANTS else PLANTS,
            vision_distance=random_attribute(self.vision_distance, deviation=DEVIATION_OF_RANDOM_PROPERTIES),
            speed=random_attribute(self.speed, deviation=DEVIATION_OF_RANDOM_PROPERTIES),
            procreation_threshold=random_attribute(self.procreation_threshold, deviation=DEVIATION_OF_RANDOM_PROPERTIES),
            colour=self.species,
            species_id=self.species_id,
            x=self.x+gap,
            y=self.y+gap
        )

        smilies.append(smiley)

    def procreate(self):
        '''The process of procreating twice.'''
        if self.energy > self.procreation_threshold:
            # Creating 2 children with different gaps
            self.one_procreation(gap=PLACEMENT_GAP)
            self.one_procreation(gap=-PLACEMENT_GAP)
            smilies.remove(self) # The parent is removed from the array of the smileys as it has been split into its two children
        else: # If there isn't enough energy, the smiley falls asleep
            self.status.description = SLEEPING

def time_to_reach(pursuer: object, pursued: object) -> float: 
    '''
    Approximate estimation of time which is needed for pursuer to catch pursued.\n
    The estimation implies that throughout the pursuit pursuer chases pursued and pursued runs away.\n
    It is possible for pursued not to see pursuer at the beginning of the pursuit. This is what is not considered by this function.\n
    This function is only called when the speed of pursuer is greater than the speed of pursued.
    '''
    distance = distance_between_objects(pursuer, pursued)
    return distance/(pursuer.speed - pursued.speed)

def total_energy_loss(smiley: object) -> float: # Energy loss every time one_action() is called
    '''This function is never called alone. The output of it is always multiplied by a value of time.'''
    return smilies_data['energy_for_vision']*smiley.vision_distance + smilies_data['energy_for_moving']*smiley.speed