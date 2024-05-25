import multiprocessing
from fetch_and_process import fetch_and_process


def run_fetch_and_process(start, end):
    fetch_and_process(start, end)


if __name__ == '__main__':
    processes = []
    for i in range(10):
        start_row = i * 100
        end_row = start_row + 100
        p = multiprocessing.Process(
            target=run_fetch_and_process, args=(start_row, end_row))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
