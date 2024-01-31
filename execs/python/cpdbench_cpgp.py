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
from cpgp.cpgp.models import fit_GPR, make_GPR
from cpgp.cpgp.hmc import run_hmc

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

def run_cpgp(mat, params):
    # Find best initial cp candidate out of 10 tries
    # Set HMC priors
    # Sample 1000 MC samples
    results = []
    for _ in range(10):
        model = make_GPR(X, Y, k)
        result = fit_GPR(model)
        results.append((result, model)) if result["success"] else None
    _, model = min(results)
    model, samples, parameter_samples = run_hmc(model=model, num_samples=1000, num_burnin_steps=100)
    return



def parse_args():
    parser = argparse.ArgumentParser(description="Wrapper for ADAGA")
    parser.add_argument(
        "-i", "--input", help="path to the input data file", required=True
    )
    parser.add_argument(
        "--min_window_size", default=15
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
    regions = run_cpgp(mat, parameters)
    locations = [[int(j) for j in list(i.values())] for i in regions.closed_windows]
    stop_time = time.time()
    runtime = stop_time - start_time

    exit_success(data, args, {}, locations, runtime, __file__)


if __name__ == "__main__":
    main()
