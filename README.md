# MeshVertexAverager
 
MeshVertexAverager is a lightweight Python tool for averaging vertex positions across multiple OBJ meshes that share identical topology and vertex order.
 
Although originally developed for creating average human faces, it can be used with any mesh dataset that shares the same topology.
 
![Workflow](images/workflow.png)
 
The example above averages three meshes.
 
MeshVertexAverager can process any number of meshes, limited only by available system memory.
 
## Features
 
- Average multiple OBJ meshes
- Preserve topology
- Preserve vertex order
- Generate an averaged mesh
- Works with any number of meshes
- Suitable for average face generation
- Supports averaging of 2 or more meshes
 
## Requirements
 
- Python 3.10 or newer
- NumPy
- Trimesh
 
## Installation
 
Clone the repository:
 
```bash
git clone https://github.com/shimazakyo-sys/MeshVertexAverager.git
cd MeshVertexAverager
```
 
Install dependencies:
 
```bash
pip install -r requirements.txt
```
 
or
 
```bash
pip install numpy trimesh
```
 
## Directory Structure
 
```text
MeshVertexAverager/
├── input_meshes/
├── output/
├── average_mesh.py
├── README.md
├── LICENSE
└── requirements.txt
```
 
## Usage
 
Place your OBJ files into:
 
```text
input_meshes/
```
 
Run:
 
```bash
python average_mesh.py
```
 
The averaged mesh will be created in:
 
```text
output/
```
 
as:
 
```text
average_mesh.obj
```
 
## Input Requirements
 
All meshes must:
 
- Be OBJ format
- Have identical topology
- Have identical vertex count
- Have identical vertex order
 
MeshVertexAverager does not perform:
 
- Mesh registration
- Retopology
- Vertex correspondence estimation
 
Input meshes must already be aligned and topology-compatible.
 
## License
 
MIT License