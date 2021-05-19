from pathlib import Path

from pytest import fixture
from numpy import load


@fixture
def gnactv_file():
    cwd = Path.cwd().parts

    if cwd[-1] == "read":
        return Path("data/gnactv_sample.bin")
    elif cwd[-1] == "test":
        return Path("read/data/gnactv_sample.bin")
    elif cwd[-1] == "scikit-imu":
        return Path("test/read/data/gnactv_sample.bin")


@fixture
def gnactv_truth():
    cwd = Path.cwd().parts

    if cwd[-1] == "read":
        path = "data/gnactv_data.npz"
    elif cwd[-1] == "test":
        path = "read/data/gnactv_data.npz"
    elif cwd[-1] == "scikit-imu":
        path = "test/read/data/gnactv_data.npz"

    dat = load(path, allow_pickle=False)

    data = {
        i: dat[i] for i in ['accel', 'time', 'temperature', 'light']
    }
    data["day_ends"] = {(8, 12): dat["day_ends_8_12"]}

    return data


@fixture
def ax3_file():
    cwd = Path.cwd().parts

    if cwd[-1] == "read":
        return Path("data/ax3_sample.cwa")
    elif cwd[-1] == "test":
        return Path("read/data/ax3_sample.cwa")
    elif cwd[-1] == "scikit-imu":
        return Path("test/read/data/ax3_sample.cwa")


@fixture
def ax3_truth():
    cwd = Path.cwd().parts

    if cwd[-1] == "read":
        path = "data/ax3_data.npz"
    elif cwd[-1] == "test":
        path = "read/data/ax3_data.npz"
    elif cwd[-1] == "scikit-imu":
        path = "test/read/data/ax3_data.npz"

    dat = load(path, allow_pickle=False)

    data = {
        i: dat[i] for i in ['accel', 'time', 'temperature', 'fs']
    }
    data["day_ends"] = {(8, 12): dat["day_ends_8_12"]}

    return data


@fixture
def ax6_file():
    cwd = Path.cwd().parts

    if cwd[-1] == "read":
        return Path("data/ax6_sample.cwa")
    elif cwd[-1] == "test":
        return Path("read/data/ax6_sample.cwa")
    elif cwd[-1] == "scikit-imu":
        return Path("test/read/data/ax6_sample.cwa")


@fixture
def ax6_truth():
    cwd = Path.cwd().parts

    if cwd[-1] == "read":
        path = "data/ax6_data.npz"
    elif cwd[-1] == "test":
        path = "read/data/ax6_data.npz"
    elif cwd[-1] == "scikit-imu":
        path = "test/read/data/ax6_data.npz"

    dat = load(path, allow_pickle=False)

    data = {
        i: dat[i] for i in ['accel', 'time', 'gyro', 'temperature', 'fs']
    }
    data["day_ends"] = {(8, 12): dat["day_ends_8_12"]}

    return data
