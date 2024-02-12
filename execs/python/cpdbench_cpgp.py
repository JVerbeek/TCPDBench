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
import numpy as np
import tensorflow as tf
import sys
import os
sys.path.append(os.path.expanduser("~")+"/TCPDBench/execs/python")
print(sys.path)
from cpgp.models import CPGP

jitter = 1e-8
# custom_config = gpflow.settings.get_settings()
# custom_config.numerics.jitter_level = jitter

# custom_config = gpflow.settings.get_settings()
# custom_config.numerics.jitter_level = jitter
# custom_config.float_type = tf.float64
from cpdbench_utils import (
    load_dataset,
    make_param_dict,
    exit_with_error,
    exit_with_timeout,
    exit_success,
)

kernels = {"RBF": gpflow.kernels.RBF(),
 "Linear": gpflow.kernels.Linear(),
 "Matern52": gpflow.kernels.Matern52(),
 "RationalQuadratic": gpflow.kernels.RationalQuadratic()
}

def run_cpgp(mat, params):
    results = []
    for i in range(10):
        model = gpflow.kernels.ChangePoints(kernels=[params["kernel1"], params["kernel2"]], locations=[params["location"]])
        cpgp = CPGP(model)
        res = cpgp.fit(mat)
        if res["opt"] < best:
            best = res["opt"]
            best_model = cpgp
    samples, parameter_samples = best_model.sample_hyperparams()
    return best_model.model.kernel.locations


def parse_args():
    parser = argparse.ArgumentParser(description="Wrapper for CPGP")
    parser.add_argument(
        "-i", "--input", help="path to the input data file", default="/home/janneke/TCPDBench/datasets/gdp_argentina.json"
    )
    parser.add_argument(
        "--kernel1", help="Kernel one", type=str, default="RBF"
    )
    parser.add_argument(
        "--kernel2", help="Kernel two", type=str, default="RBF"
    )
    parser.add_argument(
        "--prior-scale", help="Scale for HMC prior", type=float, default=10.0)
    parser.add_argument(
        "--location", help="Initial location", type=int, default=0
    )
    parser.add_argument(
        "--n_inducing_points", help="Inducing points", type=int, default=10
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
    locations = run_cpgp(mat, parameters)
    stop_time = time.time()
    runtime = stop_time - start_time

    exit_success(data, args, {}, locations, runtime, __file__)


if __name__ == "__main__":
    main()
