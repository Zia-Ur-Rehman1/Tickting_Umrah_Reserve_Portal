from multiprocessing import cpu_count
from os import environ



bind = '0.0.0.0:8000'
max_requests = 1000
worker_connections = 1000
# worker_class = 'gevent'
workers = cpu_count() * 2 + 1