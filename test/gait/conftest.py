from tempfile import TemporaryDirectory as TempDir
from pathlib import Path

from pytest import fixture
import h5py
import numpy as np
from scipy.interpolate import interp1d

from ..base_conftest import *


def _get_sample_accel(goal_fs):
    path = resolve_data_path('gait_data.h5', 'gait')
    with h5py.File(path, 'r') as f:
        accel = f['accel'][()]
        time = f['time'][()]

    fs = 1 / np.mean(np.diff(time))

    if fs > (1.015 * goal_fs):
        t_ = np.arange(time[0], time[-1], 1 / goal_fs)
        a_ = np.zeros((t_.size, 3))
        for i in range(3):
            a_[:, i] = np.interp(t_, time, accel[:, i])
        fs_ = goal_fs
    elif fs < (0.985 * goal_fs):
        assert False, "Original FS too low for goal_fs, failing test"
    else:
        t_ = time
        a_ = accel
        fs_ = goal_fs

    return t_, fs_, a_


@fixture(scope='module')
def get_sample_accel():
    return _get_sample_accel


@fixture(scope='module')
def get_sample_bout_accel():
    def get_stuff(freq):
        t, fs, accel = _get_sample_accel(freq)

        if freq == 50.0:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                starts = f['Truth']['Gait Classification']['gait_starts_50'][()]
                stops = f['Truth']['Gait Classification']['gait_stops_50'][()]

            idx = np.argmax(stops - starts)
            bout_acc = accel[starts[idx]:stops[idx], :]
            bout_time = t[starts[idx]:stops[idx]]
        elif freq == 20.0:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                starts = f['Truth']['Gait Classification']['gait_starts_20'][()]
                stops = f['Truth']['Gait Classification']['gait_stops_20'][()]

            idx = np.argmax(stops - starts)
            bout_acc = accel[starts[idx]:stops[idx], :]
            bout_time = t[starts[idx]:stops[idx]]
        else:
            assert False, "Invalid frequency"

        vaxis = np.argmax(np.mean(bout_acc, axis=0))
        return bout_acc, bout_time, vaxis, np.sign(np.mean(bout_acc, axis=0)[vaxis])

    return get_stuff


@fixture(scope='module')
def get_contact_truth():
    def get_stuff(fs):
        if fs > 50.0:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                ic = f['Truth']['Gait Events']['ic_50'][()]
                fc = f['Truth']['Gait Events']['fc_50'][()]
        else:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                ic = f['Truth']['Gait Events']['ic_20'][()]
                fc = f['Truth']['Gait Events']['fc_20'][()]

        return ic, fc
    return get_stuff


@fixture(scope='module')
def get_gait_classification_truth():
    def get_stuff(freq):
        if freq >= 50.0:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                starts = f['Truth']['Gait Classification']['gait_starts_50'][()]
                stops = f['Truth']['Gait Classification']['gait_stops_50'][()]
        else:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                starts = f['Truth']['Gait Classification']['gait_starts_20'][()]
                stops = f['Truth']['Gait Classification']['gait_stops_20'][()]

        return starts, stops
    return get_stuff


@fixture(scope='module')
def get_bgait_samples_truth():  # boolean gait classification
    def get_stuff(case):
        starts = np.array([0, 150, 165, 200, 225, 400, 770, 990])
        stops = np.array([90, 160, 180, 210, 240, 760, 780, 1000])

        if case == 1:
            dt = 1 / 50
            time = np.arange(0, 1000 * dt, dt)
            n_max_sep = 25  # 0.5 seconds
            n_min_time = 75  # 1.5 seconds

            bouts = [
                slice(0, 90),
                slice(150, 240),
                slice(400, 780)
            ]
        elif case == 2:
            dt = 1 / 100
            time = np.arange(0, 1000 * dt, dt)
            n_max_sep = 50  # 0.5 seconds
            n_min_time = 200  # 2 seconds

            bouts = [
                slice(400, 780)
            ]

        elif case == 3:
            dt = 1 / 50
            time = np.arange(0, 1000 * dt, dt)
            n_max_sep = 75  # 1.5 seconds
            n_min_time = 5  # 0.1 seconds

            bouts = [
                slice(0, 240),
                slice(400, 780),
                slice(990, 1000)
            ]
        else:
            dt = 1 / 50
            time = np.arange(0, 1000 * dt, dt)
            n_max_sep = 6  # 0.12 seconds
            n_min_time = 5  # 0.1 seconds

            bouts = [
                slice(0, 90),
                slice(150, 180),
                slice(200, 210),
                slice(225, 240),
                slice(400, 760),
                slice(770, 780),
                slice(990, 1000)
            ]
        return starts, stops, time, n_max_sep * dt, n_min_time * dt, bouts
    return get_stuff


@fixture(scope='module')
def get_strides_truth():
    def get_stuff(fs, keys):
        gait = {}
        if fs >= 50:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                for k in keys:
                    gait[k] = f['Truth']['Strides'][f'{k}_50'][()]
        else:
            with h5py.File(resolve_data_path('gait_data.h5', 'gait'), 'r') as f:
                for k in keys:
                    gait[k] = f['Truth']['Strides'][f'{k}_20'][()]

        return gait
    return get_stuff


@fixture
def sample_gait():
    gait = {
        'IC': np.array([10, 35, 62, 86, 111, 10, 35, 62, 86, 111, 5, 20, 25, 55, 80]),
        'FC opp foot': np.array([15, 41, 68, 90, 116, 15, 41, 68, 90, 116, 10, 25, 28, 65, 90]),
        'FC': np.array([40, 65, 90, 115, 140, 40, 65, 90, 115, 140, 35, 50, 55, 85, 110]),
        'delta h': np.array([
            0.05, 0.055, 0.05, 0.045, np.nan,
            0.05, 0.055, 0.05, 0.045, np.nan,
            0.05, 0.05, 0.05, 0.05, np.nan
        ]),
        'Bout N': np.array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3])
    }
    return gait


@fixture(scope='module')
def sample_gait_aux():
    def y(x):
        return np.sin(np.pi * x / x.max()) + np.sin(5 * np.pi * x/x.max()) / (x+1)

    a = np.concatenate(
        (
            y(np.arange(25)),
            y(np.arange(27)),
            y(np.arange(24)),
            y(np.arange(25)),
            y(np.arange(25)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(25)),
            y(np.arange(27))
        )
    ).reshape((-1, 1))

    gait_aux = {
        'accel': [
            a, a, a
        ],
        'inertial data i': np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2]),
        'vert axis': np.array([0] * 15)
    }

    return gait_aux


@fixture
def sample_gait_nan_bout():
    gait = {
        'IC': np.array([10, 35, 62, 86, 111, 11, 35]),
        'FC opp foot': np.array([15, 41, 68, 90, 116, 15, 41]),
        'FC': np.array([40, 65, 90, 115, 140, 41, 65]),
        'delta h': np.array([0.05, 0.055, 0.05, 0.045, np.nan, np.nan, np.nan]),
        'Bout N': np.array([1, 1, 1, 1, 1, 2, 2])
    }
    return gait


@fixture(scope='module')
def sample_gait_aux_nan_bout():
    def y(x):
        return np.sin(np.pi * x / x.max()) + np.sin(5 * np.pi * x/x.max()) / (x+1)

    a = np.concatenate(
        (
            y(np.arange(25)),
            y(np.arange(27)),
            y(np.arange(24)),
            y(np.arange(25)),
            y(np.arange(25)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(25)),
            y(np.arange(27))
        )
    ).reshape((-1, 1))

    gait_aux = {
        'accel': [
            a, a
        ],
        'inertial data i': np.array([0, 0, 0, 0, 0, 1, 1]),
        'vert axis': np.array([0] * 7)
    }

    return gait_aux


@fixture
def sample_gait_no_bout():
    gait = {
        'IC': np.array([10, 35, 62, 86, 111, 11, 35]),
        'FC opp foot': np.array([15, 41, 68, 90, 116, 15, 41]),
        'FC': np.array([40, 65, 90, 115, 140, 41, 65]),
        'delta h': np.array([0.05, 0.055, 0.05, 0.045, np.nan, np.nan, np.nan]),
        'Bout N': np.array([1, 1, 1, 1, 1, 3, 3])
    }
    return gait


@fixture(scope='module')
def sample_gait_aux_no_bout():
    def y(x):
        return np.sin(np.pi * x / x.max()) + np.sin(5 * np.pi * x/x.max()) / (x+1)

    a = np.concatenate(
        (
            y(np.arange(25)),
            y(np.arange(27)),
            y(np.arange(24)),
            y(np.arange(25)),
            y(np.arange(25)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(24)),
            y(np.arange(25)),
            y(np.arange(27))
        )
    ).reshape((-1, 1))

    gait_aux = {
        'accel': [
            a, a, a
        ],
        'inertial data i': np.array([0, 0, 0, 0, 0, 2, 2]),
        'vert axis': np.array([0] * 7)
    }

    return gait_aux


@fixture(scope='class')
def sample_datasets():
    study1_td = TempDir()
    study1_path = Path(study1_td.name)
    study2_td = TempDir()
    study2_path = Path(study2_td.name)

    for k in range(2):
        # study 1
        with h5py.File(study1_path / f'subject_{k}.h5', 'w') as f:
            for j in range(3):
                ag = f.create_group(f'activity{j}')
                ag.attrs.create('Gait Label', 1 if j == 1 else 0)

                for i in range(2):
                    agt = ag.create_group(f'Trial {i}')
                    agt.attrs.create('Sampling rate', 100.0)

                    agt.create_dataset('Accelerometer', data=np.random.rand(1500, 3) + np.array([[0, 0, 1]]))

    # study 2
        with h5py.File(study2_path / f'subject_{k}.h5', 'w') as f:
            for j in range(2):
                ag = f.create_group(f'activity{j}')
                ag.attrs.create('Gait Label', 1 if j == 1 else 0)

                for i in range(3):
                    agt = ag.create_group(f'Trial {i}')
                    agt.attrs.create('Sampling rate', 50.0)

                    agt.create_dataset('Accelerometer', data=np.random.rand(1000, 3) + np.array([[0, 1, 0]]))

    yield [study1_path, study2_path]

    # clean up the temporary directories
    study1_td.cleanup()
    study2_td.cleanup()
