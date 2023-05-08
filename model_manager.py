import torch

class ModelManager:
    def __init__(self):
        self.model_paths = {
            'astrals': r'C:\Users\19512\yolov5\runs\train\astral_runecrafting\weights\best.pt',
            't95_wisps': r'C:\Users\19512\yolov5\runs\train\t95_div\weights\best.pt',
            'desert_sandstone': r'C:\Users\19512\yolov5\runs\train\desert_sandstone\weights\best.pt',
            'rc_navigation': r'C:\Users\19512\yolov5\runs\train\abyss_rc_navigation\weights\best.pt',
            'the_abyss': r'C:\Users\19512\yolov5\runs\train\the_abyss\weights\best.pt',
            'mage_and_riftmodel': r'C:\Users\19512\yolov5\runs\train\rc_nav\weights\best.pt',
            'blood_rc': r'C:\Users\19512\yolov5\runs\train\blood_rift_altar\weights\best.pt',
            'aerated_sediment': r'C:\Users\19512\yolov5\runs\train\rc_nav\weights\best.pt',
            'mage_of_zamorak': r'C:\Users\19512\yolov5\runs\train\mage_of_zamorak\weights\best.pt'
        }
        self.models = {}

    def get_model(self, model_name):
        if model_name not in self.models:
            self.models[model_name] = torch.hub.load('ultralytics/yolov5', 'custom', self.model_paths[model_name])
        return self.models[model_name]
