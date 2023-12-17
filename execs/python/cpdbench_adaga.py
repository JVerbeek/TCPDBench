#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A method that always returns no change points

Author: G.J.J. van den Burg
Date: 2020-05-07
License: MIT
Copyright: 2020, The Alan Turing Institute

"""

import argparse
import time
import gpflow
import tensorflow as tf

jitter = 1e-8
custom_config = gpflow.settings.get_settings()
custom_config.numerics.jitter_level = jitter

custom_config = gpflow.settings.get_settings()
custom_config.numerics.jitter_level = jitter
custom_config.float_type = tf.float64
from cpdbench_utils import (
    load_dataset,
    make_param_dict,
    exit_with_error,
    exit_with_timeout,
    exit_success,
)

from adaga.inducing_points_version.core.adaptive_regionalization import AdaptiveRegionalization

def run_adaga(mat, params):
    with gpflow.settings.temp_settings(custom_config):
        x = list(range(len(mat)))
        y = mat
        regionalization = AdaptiveRegionalization(domain_data=x,
                                              system_data=y,
                                              delta=params["delta"],
                                              min_w_size=params["min_window_size"],
                                              n_ind_pts=params["min_inducing_poitns"],
                                              seed=params["seed"],
                                              batch_size=params["batch_size"],
                                              kern=params["kernel"])
        regionalization.regionalize()
    return regionalization



def parse_args():
    parser = argparse.ArgumentParser(description="Wrapper for ADAGA")
    parser.add_argument(
        "-i", "--input", help="path to the input data file", required=True
    )
    parser.add_argument(
        "--window_size"
    )
    parser.add_argument(
        "--delta", help="Threshold for the T1/T2 error", type=float, default=0.6
    )
    parser.add_argument(
        "--kernel", help="Kernel used by ADAGA", type=str, default="RBF"
    )
    parser.add_argument(
        "--batch_size", help="Batch size with which new points are added", type=int, default=15
    )
    parser.add_argument("-o", "--output", help="path to the output file")
    return parser.parse_args()


def main():
    args = parse_args()

    data, mat = load_dataset(args.input)

    start_time = time.time()

    defaults = {
    }

    # insert some code that runs adaga here
    parameters = make_param_dict(args, defaults)
    regions = run_adaga(mat, parameters)
    locations = regions.closed_windows

    stop_time = time.time()
    runtime = stop_time - start_time

    exit_success(data, args, {}, locations, runtime, __file__)


if __name__ == "__main__":
    main()
