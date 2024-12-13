import random, time, multiprocessing, json
from multiprocessing.pool import ThreadPool


def write_to_file(results):
    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)


def worker(task_queue, result_queue):
    while True:
        number = task_queue.get()
        if number is None:
            break
        result = process_number(number)
        result_queue.put(result)


def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(number):
    factorial = 1
    for i in range(2, number + 1):
        factorial *= i
    return factorial


def use_multithreading_pool(numbers):
    with ThreadPool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_number, numbers)
    return results


def use_multiprocessing_pool(numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_number, numbers)
        return results
    

def use_multiprocessing(numbers):
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Manager().Queue()
    num_processes = multiprocessing.cpu_count()
    processes = []
    results = []

    for number in numbers:
        task_queue.put(number)

    for _ in range(num_processes):
        task_queue.put(None)

    for _ in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(task_queue, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not result_queue.empty():
        results.append(result_queue.get())

    return results
    

def use_single(numbers):
    results = []
    for number in numbers:
        results.append(process_number(number))
    return results


def main():
    test_results = {}
    numbers = generate_data(10000)
    start = time.time()
    results = use_multithreading_pool(numbers)
    test_results['multithreading_pool'] = time.time() - start

    start = time.time()
    results = use_multiprocessing_pool(numbers)
    test_results['multiprocessing_pool'] = time.time() - start

    start = time.time()
    results = use_multiprocessing(numbers)
    test_results['multiprocessing'] = time.time() - start

    start = time.time()
    results = use_single(numbers)
    test_results['single'] = time.time() - start

    write_to_file(test_results)


if __name__ == '__main__':
    main()