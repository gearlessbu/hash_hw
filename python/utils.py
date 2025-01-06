import numpy as np
import pathlib
import shutil

def create_folder(folder_name, exist_ok):
    pathlib.Path(folder_name).mkdir(parents=True, exist_ok=exist_ok)

def delete_folder(folder_name):
    shutil.rmtree(folder_name)

def delete_file(file_name):
    pathlib.Path(file_name).unlink()

def file_exist(file_name):
    return pathlib.Path(file_name).is_file()

def read_fvecs(file_path):
    """
    Read a .fvecs file and return the data as a numpy array.

    Args:
        file_path (str): Path to the .fvecs file.

    Returns:
        np.ndarray: A 2D array where each row is a vector.
    """
    with open(file_path, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.float32)
        f.close()
    with open(file_path, 'rb') as f:
        data_int = np.frombuffer(f.read(), dtype=np.int32)
        f.close()
    dim = int(data_int[0])  # 获取维度
    # print(dim)
    vectors = data.reshape(-1, dim + 1)  # 每个向量包括维度值和数据
    return vectors[:, 1:]  # 跳过每行的第一个维度值，只返回数据部分

def read_ivecs(file_path):
    """
    Read a .fvecs file and return the data as a numpy array.

    Args:
        file_path (str): Path to the .fvecs file.

    Returns:
        np.ndarray: A 2D array where each row is a vector.
    """
    with open(file_path, 'rb') as f:
        data_int = np.frombuffer(f.read(), dtype=np.int32)
        f.close()
    dim = int(data_int[0])  # 获取维度
    # print(dim)
    vectors = data_int.reshape(-1, dim + 1)  # 每个向量包括维度值和数据
    return vectors[:, 1:]  # 跳过每行的第一个维度值，只返回数据部分


if __name__ == "__main__":

    # 使用示例
    # file_path = "../datasets/siftsmall/siftsmall_base.fvecs"
    file_path = "../datasets/siftsmall/siftsmall_groundtruth.ivecs"
    file_path = "../datasets/sift/sift_query.fvecs"
    # file_path = "../datasets/sift/sift_groundtruth.ivecs"
    vectors = read_fvecs(file_path)
    # vectors = read_ivecs(file_path)
    print("Shape of vectors:", vectors.shape)
