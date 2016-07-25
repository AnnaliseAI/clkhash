#!/usr/bin/env python3.4

import anonlink.entitymatch
import concurrent.futures


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def calc_chunk_result(chunk_number, chunk, filters2, k, threshold):
    chunk_results = anonlink.entitymatch.calculate_filter_similarity(chunk, filters2,
                                                                     k=k, threshold=threshold)

    partial_sparse_result = []
    # offset chunk's A index by chunk_size * chunk_number
    chunk_size = len(chunk)
    offset = chunk_size * chunk_number
    for (ia, score, ib) in chunk_results:
        partial_sparse_result.append((ia + offset, score, ib))

    return partial_sparse_result


def calculate_filter_similarity(filters1, filters2, k=10, threshold=0.5):
    """
    Example way of computing similarity scores in parallel.

    :param filters1:
    :param filters2:
    :return:
    """

    results = []

    with concurrent.futures.ProcessPoolExecutor() as executor:

        futures = []
        chunk_size = int(20000000 / len(filters2))
        for i, chunk in enumerate(chunks(filters1, chunk_size)):
            future = executor.submit(calc_chunk_result, i, chunk, filters2, k, threshold)
            futures.append(future)

        for future in futures:
            results.extend(future.result())

    return results
