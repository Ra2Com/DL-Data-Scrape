from pathlib import Path
import shutil

from config import DEADLOCK_PATH, PATH_TO_GC, PATH_TO_HEROES, PATH_TO_MODS


def dump_localization():
    shutil.copy(Path(DEADLOCK_PATH) / PATH_TO_GC,     "data/citadel_gc_english.txt")
    shutil.copy(Path(DEADLOCK_PATH) / PATH_TO_HEROES, "data/citadel_heroes_english.txt")
    shutil.copy(Path(DEADLOCK_PATH) / PATH_TO_MODS,   "data/citadel_mods_english.txt")
