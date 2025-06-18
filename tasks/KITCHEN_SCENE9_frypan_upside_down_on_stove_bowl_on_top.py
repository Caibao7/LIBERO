"""This is a standalone file for create a task in libero."""
import numpy as np

from libero.libero.utils.bddl_generation_utils import (
    get_xy_region_kwargs_list_from_regions_info,
)
from libero.libero.utils.mu_utils import register_mu, InitialSceneTemplates
from libero.libero.utils.task_generation_utils import (
    register_task_info,
    get_task_info,
    generate_bddl_from_task_info,
)

from libero.libero.benchmark.mu_creation import *

def main():

    scene_name = "kitchen_scene9"
    language = "position the frypan upside down on the stove with the bowl resting upright on top of it"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["chefmate_8_frypan_1", "flat_stove_1", "white_bowl_1", "wooden_two_layer_shelf_1"],
        goal_states=[
            ("relaxedOn", "chefmate_8_frypan_1", "flat_stove_1"),
            ("UpsideDown", "chefmate_8_frypan_1"),
            ("relaxedOn", "white_bowl_1", "chefmate_8_frypan_1"),
            ("Upright", "white_bowl_1"),
            ("Not", ("relaxedOn", "white_bowl_1", "flat_stove_1")),
            ("Not", ("relaxedOn", "white_bowl_1", "wooden_two_layer_shelf_1")),
            ("Not", ("RelaxedOn", "chefmate_8_frypan_1", "wooden_two_layer_shelf_1")),
        ]
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main() 