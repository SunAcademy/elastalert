from prometheus_client import start_http_server, Summary
from prometheus_client import Gauge, CollectorRegistry


class Prometheus:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.metrics = {}
        start_http_server(8000)

    def add_metrics(self, rule, data):
        print rule, data
        name = rule["name"]
        g = self.get_metircs(name)
        g.set(len(data))

    def get_metircs(self, name="None", describe="This is generate from elastalert"):
        if name in self.metrics:
            return self.metrics[name]
        g = Gauge(name, describe)
        self.metrics[name] = g
        return g
