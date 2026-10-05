"""
MeshVertexAverager v1.1.0

Average vertex positions across multiple OBJ meshes
with identical topology and vertex order.

Features:
- Preserves quad polygons
- Preserves n-gons
- No automatic triangulation

License: MIT
Author: shimazakyo
"""

import os
import numpy as np

INPUT_DIR = "input_meshes"
OUTPUT_DIR = "output"
OUTPUT_FILE = "average_mesh.obj"


def load_obj(path):
    """
    OBJ読み込み
    頂点とface行を取得
    """

    vertices = []
    face_lines = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:

            if line.startswith("v "):
                parts = line.strip().split()
                vertices.append(
                    [
                        float(parts[1]),
                        float(parts[2]),
                        float(parts[3]),
                    ]
                )

            elif line.startswith("f "):
                face_lines.append(line.rstrip())

    return np.array(vertices, dtype=np.float64), face_lines


def load_meshes(folder):
    """
    OBJ群を読み込み
    """

    obj_files = sorted(
        [
            f
            for f in os.listdir(folder)
            if f.lower().endswith(".obj")
        ]
    )

    if not obj_files:
        return [], None

    meshes = []
    reference_faces = None

    for i, filename in enumerate(obj_files):

        path = os.path.join(folder, filename)

        vertices, faces = load_obj(path)

        if i == 0:
            reference_faces = faces

        meshes.append(vertices)

        print(f"Loaded: {filename}")

    return meshes, reference_faces


def validate_meshes(meshes, reference_faces, folder):
    """
    同一トポロジー確認
    """

    obj_files = sorted(
        [
            f
            for f in os.listdir(folder)
            if f.lower().endswith(".obj")
        ]
    )

    vertex_counts = [len(v) for v in meshes]

    if len(set(vertex_counts)) != 1:
        raise ValueError(
            "OBJの頂点数が一致していません。"
        )

    for filename in obj_files:

        path = os.path.join(folder, filename)

        _, faces = load_obj(path)

        if faces != reference_faces:
            raise ValueError(
                f"{filename} の面情報が一致しません。\n"
               "同一トポロジーかつ同一頂点順序のOBJのみ使用してください。"
            )


def compute_average_vertices(meshes):
    """
    頂点位置平均
    """

    stacked = np.stack(meshes, axis=0)

    return np.mean(stacked, axis=0)


def save_average_obj(avg_vertices, face_lines, output_path):
    """
    OBJ保存
    face情報は元OBJをそのまま保持
    """

    with open(output_path, "w", encoding="utf-8") as f:

        f.write("# MeshVertexAverager v1.1.0\n")
        f.write("# Averaged mesh\n\n")

        for v in avg_vertices:
            f.write(
                f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n"
            )

        f.write("\n")

        for face in face_lines:
            f.write(face + "\n")


def main():

    print("MeshVertexAverager v1.1.0")
    print("Creating averaged mesh...")

    meshes, face_lines = load_meshes(INPUT_DIR)

    if len(meshes) == 0:
        print("input_meshes に OBJ がありません。")
        return

    validate_meshes(
        meshes,
        face_lines,
        INPUT_DIR
    )

    avg_vertices = compute_average_vertices(meshes)

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    save_average_obj(
        avg_vertices,
        face_lines,
        output_path
    )

    print()
    print("処理完了！")
    print(f"保存先: {output_path}")


if __name__ == "__main__":
    main()