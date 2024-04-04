import json
import copy
import sys

import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

CUBE_VERTICES = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
], dtype=float)

CUBE_VERTICES[:, 0] *= 0.1651
CUBE_VERTICES[:, 1] *= 0.1651
CUBE_VERTICES[:, 1] -= 0.1651 / 2
CUBE_VERTICES[:, 2] *= 0.1651
CUBE_VERTICES[:, 2] -= 0.1651 / 2


CUBE_EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def plot_transformation(H, plt_ax, color, thickness):
    transformed_vertices = np.dot(H, np.vstack([CUBE_VERTICES.T, np.ones(CUBE_VERTICES.shape[0])]))

    for edge in CUBE_EDGES:
        plt_ax.plot3D(transformed_vertices[0, edge], transformed_vertices[1, edge], transformed_vertices[2, edge], color=color, linewidth=thickness)

    zero = np.zeros((4, 1))
    zero[3, 0] = 1
    zero = H @ zero

    plt_ax.scatter(zero[0], zero[1], zero[2], color=color, s=5)


def load_map(path):
    with open(path, "r") as f:
        ideal_field_map = json.loads(f.read())

    ideal_transforms = {}

    for tag in ideal_field_map["tags"]:
        H_world_tag = np.eye(4, 4)

        H_world_tag[0, 3] = tag["pose"]["translation"]["x"]
        H_world_tag[1, 3] = tag["pose"]["translation"]["y"]
        H_world_tag[2, 3] = tag["pose"]["translation"]["z"]

        H_world_tag[:3, :3] = scipy.spatial.transform.Rotation.from_quat((
            tag["pose"]["rotation"]["quaternion"]["X"],
            tag["pose"]["rotation"]["quaternion"]["Y"],
            tag["pose"]["rotation"]["quaternion"]["Z"],
            tag["pose"]["rotation"]["quaternion"]["W"])).as_matrix()

        ideal_transforms[tag["ID"]] = H_world_tag

    return ideal_transforms

plt_fig = plt.figure(figsize=(5, 5))
plt_ax = plt_fig.add_subplot(projection="3d")

ideal_transforms = load_map(sys.argv[1])
observed_transforms = load_map(sys.argv[2])

for tag_id, transform in observed_transforms.items():
    plot_transformation(transform, plt_ax, "lime", 1)

for tag_id, transform in ideal_transforms.items():
    plot_transformation(transform, plt_ax, "red", 1)

red_patch = mpatches.Patch(color="red", label="Ideal Map")
blue_patch = mpatches.Patch(color="lime", label="Observed Map")

plt.legend(handles=[red_patch, blue_patch])

plt_ax.set_xlabel("X")
plt_ax.set_ylabel("Y")
plt_ax.set_zlabel("Z")

plt.axis("equal")
plt.show()
