from __future__ import print_function

import os
import tempfile
# noinspection PyProtectedMember
from timeit import default_timer as timer

from clkhash.clk import generate_clk_from_csv
from clkhash.randomnames import NameList


def compute_hash_speed(num, quiet=False, use_multiprocessing=True):
    # type: (int, bool, bool) -> float
    """ Hash time.
    """
    namelist = NameList(num)

    os_fd, tmpfile_name = tempfile.mkstemp(text=True)

    schema = NameList.SCHEMA
    header_row = ','.join([f.identifier for f in schema.fields])

    with open(tmpfile_name, 'wt') as f:
        f.write(header_row)
        f.write('\n')
        for person in namelist.names:
            print(','.join([str(field) for field in person]), file=f)

    with open(tmpfile_name, 'rt') as f:
        start = timer()
        generate_clk_from_csv(f, 'secret', schema, progress_bar=not quiet, use_multiprocessing=use_multiprocessing)
        end = timer()

    os.close(os_fd)
    os.remove(tmpfile_name)

    elapsed_time = end - start
    if not quiet:
        print("{:6d} hashes in {:.6f} seconds. {:.2f} KH/s".format(num, elapsed_time, num / (1000 * elapsed_time)))
    return num / elapsed_time


if __name__ == '__main__':
    for n in [100, 1000, 10000, 50000, 100000]:
        compute_hash_speed(n, quiet=n <= 10000)
