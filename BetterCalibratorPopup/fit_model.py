import numpy as np
import json
from pathlib import Path


def main() -> None:
    base_dir = Path(".") # TODO
    input_offsets_path = base_dir / "offsets.json"
    input_offsets_data = json.loads(input_offsets_path.read_text())

    centers_display = np.array(input_offsets_data["centers_display"])
    centers_pressed = np.array(input_offsets_data["centers_pressed"])

    A = construct_matrix_A(vec=centers_pressed, vec_dash=centers_display)
    b = construct_vector_b(vec=centers_pressed, vec_dash=centers_display)

    # solve the least squares problem
    x = np.linalg.lstsq(A, b, rcond=None)[0].ravel()

    # create the output structure
    output = {
        "sx": x[0],
        "sy": x[1],
        "tx": x[2],
        "ty": x[3]
    }
    print(f"Fitted model: {repr(output)}")
    output_model_path = base_dir / "model.json"
    output_model_path.write_text(json.dumps(output, indent=4))


def construct_matrix_A(vec: np.ndarray, vec_dash: np.ndarray) -> np.ndarray:
    n_points = vec.shape[0]
    A = np.zeros((2 * n_points, 4))
    for i in range(n_points):
        A[2 * i] = np.array([vec[i][0], 0, 1, 0])
        A[2 * i + 1] = np.array([0, vec[i][1], 0, 1])
    return A

def construct_vector_b(vec: np.ndarray, vec_dash: np.ndarray) -> np.ndarray:
    n_points = vec.shape[0]
    b = np.zeros((2 * n_points, 1))
    for i in range(n_points):
        b[2 * i] = vec_dash[i][0]
        b[2 * i + 1] = vec_dash[i][1]
    return b


if __name__ == "__main__":
    main()
