"""This is a standalone file for creating a task in libero."""
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


@register_mu(scene_type="office")
class OfficeSceneCustom(InitialSceneTemplates):
    def __init__(self):
        super().__init__(
            workspace_name="living_room_table",
            fixture_num_info={
                "living_room_table": 1,
                "wooden_two_layer_shelf": 1,
                "white_storage_box": 1,
                "wine_rack": 1,
            },
            object_num_info={
                "black_book": 1,
                "yellow_book": 1,
                "red_coffee_mug": 1,
                "wine_bottle": 1,
                "orange_juice": 1,
            },
        )

    # ------------------------------------------------------------------ #
    def define_regions(self):
        # ── fixture ──
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[0.10,  0.35],
                region_name="wooden_two_layer_shelf_init_region",
                target_name=self.workspace_name,
                region_half_len=0.01,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[ 0.20,  -0.15],
                region_name="white_storage_box_init_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[ -0.05,  -0.30],   # wine rack
                region_name="wine_rack_init_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )

        # ── each object one init_region ──
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.30,  0.35],    # black book
                region_name="black_book_init_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.18,  0.25],    # yellow book
                region_name="yellow_book_init_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[ -0.10,  0.10],   # wine bottle
                region_name="wine_bottle_init_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.20,  -0.25],    # orange juice
                region_name="orange_juice_init_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )
        self.regions.update(
            self.get_region_dict(
                region_centroid_xy=[-0.35, -0.25],    # red coffee mug
                region_name="red_coffee_mug_init_region",
                target_name=self.workspace_name,
                region_half_len=0.02,
            )
        )

        self.xy_region_kwargs_list = get_xy_region_kwargs_list_from_regions_info(
            self.regions
        )

    # ------------------------------------------------------------------ #
    @property
    def init_states(self):
        return [
            # fixtures
            ("On", "wooden_two_layer_shelf_1", "living_room_table_wooden_two_layer_shelf_init_region"),
            ("On", "wine_rack_1",    "living_room_table_wine_rack_init_region"),
            ("On", "white_storage_box_1", "living_room_table_white_storage_box_init_region"),

            # movable objects
            ("On", "black_book_1",    "living_room_table_black_book_init_region"),
            ("On", "yellow_book_1",   "living_room_table_yellow_book_init_region"),
            ("On", "wine_bottle_1",    "living_room_table_wine_bottle_init_region"),
            ("On", "orange_juice_1",  "living_room_table_orange_juice_init_region"),
            ("On", "red_coffee_mug_1","living_room_table_red_coffee_mug_init_region"),
        ]

# ("In", "black_book_1", "wooden_two_layer_shelf_1_bottom_region"),
# ("On", "black_book_1", "wooden_two_layer_shelf_1_top_side"),
# ("In", "yellow_book_1", "wooden_two_layer_shelf_1_top_region"),


def main():

    # Write your reward code here
    scene_name = "office_scene_custom"
    language = "Place two books flat in different layers of the shelf, and mug on top"
    register_task_info(
        language,
        scene_name=scene_name,
        objects_of_interest=["black_book_1", "yellow_book_1", "wooden_two_layer_shelf_1", "red_coffee_mug_1"],
        goal_states=[
            ("Or", 
                ("All", (
                    ("In", "black_book_1", "wooden_two_layer_shelf_1_bottom_region"),
                    ("In", "yellow_book_1", "wooden_two_layer_shelf_1_top_region"),
                    )
                ),
                ("All", (
                    ("In", "black_book_1", "wooden_two_layer_shelf_1_top_region"),
                    ("In", "yellow_book_1", "wooden_two_layer_shelf_1_bottom_region"),
                    )
                ),
            ),
            ("On", "red_coffee_mug_1", "wooden_two_layer_shelf_1_top_side"),
            ("AxisAlignedWithin", "black_book_1", "z", 85, 95),
            ("AxisAlignedWithin", "yellow_book_1", "z", 85, 95),
            ("Upright", "red_coffee_mug_1"),
            ("Not", ("InContact", "gripper0_finger1", "red_coffee_mug_1")),
            ("Not", ("InContact", "gripper0_finger2", "red_coffee_mug_1")),
            ("Not", ("InContact", "gripper0_hand", "red_coffee_mug_1")),
            ("Not", ("InContact", "gripper0_finger1_pad", "red_coffee_mug_1")),
            ("Not", ("InContact", "gripper0_finger2_pad", "red_coffee_mug_1")),
        ],
    )

    bddl_file_names, failures = generate_bddl_from_task_info()
    print(bddl_file_names)


if __name__ == "__main__":
    main()
