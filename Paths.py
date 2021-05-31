CURRENT_PATH = ""
FOLDER_PATHS = {}


def initialize_paths(current_path):
    import os

    FOLDER_PATHS["Sprites"] = os.path.join(current_path, 'Data', 'Sprites')
    FOLDER_PATHS["Pieces"] = os.path.join(current_path, 'Data', 'Sprites', 'Pieces')
    FOLDER_PATHS["Sounds"] = os.path.join(current_path, 'Data', 'Sounds')
    FOLDER_PATHS["TrainedModels"] = os.path.join(current_path, 'Data', 'TrainedModels')
    FOLDER_PATHS["Stockfish"] = os.path.join(current_path, 'Data', 'Stockfish')
    FOLDER_PATHS["Leaderboards"] = os.path.join(current_path, 'Data', 'Leaderboards')
