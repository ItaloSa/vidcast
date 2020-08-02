import threading
# import time
# from random import randint


class Queue:
    queue = []
    running = 0

    def __init__(self, parallel=1):
        self.parallel = parallel

    def thread_func(self, function, context):
        print(f'>> Queue -> thread_func')
        function(context)
        # time.sleep(randint(2,8))
        self.running -= 1
        self.check_queue()

    def dequeue(self):
        print(f'>> Queue -> dequeue')
        item = self.queue.pop(0)
        job = threading.Thread(
            target=self.thread_func,
            args=(item['func'], item['ctxt'])
        )
        job.start()
        self.running += 1

    def check_queue(self):
        print(f'>> Queue -> check_queue')
        if self.running < self.parallel and len(self.queue):
            self.dequeue()

    def enqueue(self, function, context):
        print(f'>> Queue -> enqueue')
        self.queue.append({'func': function, 'ctxt': context})
        self.check_queue()
        return len(self.queue)

# queue = Queue(parallel=3)

# def cachorro(context):
#     print(f'dog: {context['name']}')

# itemA = {'name': 'foo'}
# queue.enqueue(cachorro, itemA)
# time.sleep(2)

