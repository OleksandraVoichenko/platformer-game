from settings import *

def import_image(*filepath, format = 'png', alpha = True):
    full_path = join(*filepath) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf


def import_folder(*filepath):
    frames = []
    for folder_path, _, file_names in walk(join(*filepath)):
        for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames