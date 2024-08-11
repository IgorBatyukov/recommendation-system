############
# Streaming Payments Processor, two vendors edition.
#
# We decided to improve the payment processor from the previous
# exercise and hired two vendors. One was to implement `stream_payments()`
# function, and another `store_payments()` function.
#
# The function `process_payments_2()` is processing a large, but finite
# amount of payments in a streaming fashion.
#
# Unfortunately the vendors did not coordinate their efforts, and delivered
# their functions with incompatible APIs.
#
# TODO: Your task is to analyse the APIs of `stream_payments()` and
# `store_payments()` and to write glue code in `process_payments_2()`
# that allows us to store the payments using these vendor functions.
#
# NOTE: you need to take into account the following restrictions:
# - You are allowed only one call each to `stream_payments()` and
# to `store_payments()`
# - You can not read from the storage.
# - You can not use disk as temporary storage.
# - Your system has limited memory that can not hold all payments.
#
############

import threading
from queue import Queue


# This is a library function, you can't modify it.
def stream_payments(callback_fn):
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in range(10):
        callback_fn(i)


# This is a library function, you can't modify it.
def store_payments(amount_iterator):
    """
    Iterates over the payment amounts from amount_iterator
    and stores them to a remote system.
    """
    # Sample implementation to make the code run in coderpad.
    # Do not rely on this exact implementation.
    for i in amount_iterator:
        print(i)


def callback_example(amount):
    print(amount)
    return True


def process_payments_2():
    """
    TODO:
    Modify `process_payments_2()`, write glue code that enables
    `store_payments()` to consume payments produced by `stream_payments()`
    """
    streaming_queue = Queue()

    def payment_callback(amount):
        streaming_queue.put(amount)
        return True

    stream_thread = threading.Thread(target=stream_payments, args=(payment_callback,))
    stream_thread.start()

    def payment_iterator():
        while stream_thread.is_alive() or not streaming_queue.empty():
            yield streaming_queue.get(timeout=0.1)

    store_payments(payment_iterator())
    stream_thread.join()


if __name__ == '__main__':
    process_payments_2()
