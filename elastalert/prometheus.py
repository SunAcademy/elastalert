from prometheus_client import start_http_server, Summary
from prometheus_client import Gauge, CollectorRegistry


class Prometheus:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.metrics = {}
        start_http_server(8000)

    def add_metrics(self, rule, data):
        name = rule["name"]
        g = self.get_metircs(name, labels=rule["labels"])
        g = self.add_labels(g, rule["labels"])
        if data is None:
            return g.set(0)
        g.set(len(data))

    def add_labels(self, metrics, x={}):
        m = metrics
        m = m.labels(*x.values())
        return m

    def get_metircs(self, name="None", describe="This is generate from elastalert", labels={}):
        if name in self.metrics:
            return self.metrics[name]
        g = Gauge(name, describe, labelnames=labels.keys())
        self.metrics[name] = g
        return g
