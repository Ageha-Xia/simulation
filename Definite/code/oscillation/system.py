from tqdm import tqdm

class System:
    def __init__(self, objects, strings, dampers):
        self.objects = objects
        self.strings = strings
        self.dampers = dampers
        
        for obj in self.objects:
            obj.init(1e-3)
        
    
    def run(self, dt, steps, disable_tqdm=False):
        if disable_tqdm:
            for i in range(2, steps):
                for obj in self.objects:
                    obj.update(dt)
        else :
            for i in tqdm(range(2, steps)):
                for obj in self.objects:
                    obj.update(dt)
    
    def get_energy(self):
        energy = 0
        for obj in self.objects:
            energy += obj.get_energy()
        for string in self.strings:
            energy += string.get_energy()
            
        return energy
    
    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)