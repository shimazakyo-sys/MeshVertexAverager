"""
MeshVertexAverager v1.0

Average vertex positions across multiple OBJ meshes
with identical topology and vertex order.

License: MIT
Author: Shimazakyo
"""

import os
import trimesh
import numpy as np

# ---------------------------------------------------------
# MeshVertexAverager
# このプログラムは「input_meshes」フォルダに入れた
# 複数の同一トポロジーOBJメッシュを読み込み、
# 対応する頂点座標を平均して
# 新しい平均メッシュをoutput フォルダに生成します。
# ---------------------------------------------------------

INPUT_DIR = "input_meshes"
OUTPUT_DIR = "output"
OUTPUT_FILE = "average_mesh.obj"

def load_meshes(input_dir):
    """OBJ メッシュを全部読み込む"""
    meshes = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".obj"):
            path = os.path.join(input_dir, filename)
            mesh = trimesh.load(path, process=False)
            meshes.append(mesh)
            print(f"読み込み完了: {filename}")
    return meshes

def compute_average_mesh(meshes):
    """複数メッシュの平均メッシュを作る"""

    # すべて同じ頂点数であることを確認
    vertex_counts = [mesh.vertices.shape[0] for mesh in meshes]
    if len(set(vertex_counts)) != 1:
        raise ValueError("頂点数が一致しません。同一トポロジーかつ同一頂点順序のOBJのみを使用してください。")

    # 頂点を全部集める
    all_vertices = np.array([mesh.vertices for mesh in meshes])

    # 平均を取る（軸=0 → メッシュ間で平均）
    avg_vertices = np.mean(all_vertices, axis=0)

    # 面（faces）はどのメッシュでも同じなので、最初のものを使う
    faces = meshes[0].faces

    # 新しい平均メッシュを作る
    avg_mesh = trimesh.Trimesh(vertices=avg_vertices, faces=faces, process=False)
    return avg_mesh

def save_mesh(mesh, output_dir, filename):
    """平均メッシュを OBJ として保存"""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    mesh.export(path)
    print(f"平均形状を保存しました: {path}")

def main():
    print("MeshVertexAverager v1.0")
    print("Creating averaged mesh...")

    meshes = load_meshes(INPUT_DIR)

    if len(meshes) == 0:
        print("input_meshes に OBJ がありません。")
        return

    faces_ref = meshes[0].faces

    for mesh in meshes[1:]:
        if not np.array_equal(mesh.faces, faces_ref):
            raise ValueError(
                "面情報が一致しません。同一トポロジーのメッシュのみ使用できます。"
            )

    avg_mesh = compute_average_mesh(meshes)
    save_mesh(avg_mesh, OUTPUT_DIR, OUTPUT_FILE)

    print("処理完了！平均形状ができました。")

if __name__ == "__main__":
    main()
