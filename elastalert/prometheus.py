from prometheus_client import start_http_server, Summary
from prometheus_client import Counter, CollectorRegistry


class Prometheus:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.metrics = {}
        start_http_server(8000)

    def add_metrics(self, rule, data):
        name = rule["name"]
        g = self.get_metircs(name, labels=rule["labels"])
        if rule.get("aggregation_query_element"):
            self.set_aggregation_values(g, data=data, r=rule)
        else:
            g = self.add_labels(g, data=data and data[0] or {}, r=rule)
            g.inc(len(data))

    def set_aggregation_values(self, metric, data={}, r={}):
        if data:
            ex_bucket_aggs = data.values() and data.values()[0] or False
            if not ex_bucket_aggs:
                return True
            bucket_aggs = ex_bucket_aggs.get("bucket_aggs")
            if not bucket_aggs:
                return True
            buckets = bucket_aggs.get("buckets")
            if not buckets:
                return True
            for bucket in buckets:
                m = self.add_labels(metric, data=bucket, r=r)
                m.inc(bucket.get("doc_count", 0))
        else:
            m = self.add_labels(metric, data, r)
            m.inc(0)

    def add_labels(self, metric, data={}, r={}):
        m = metric
        l = r["labels"]
        v = []
        for x in l:
            if l[x][:2] == "$.":
                v.append(data.get(l[x][2:], "/"))
            else:
                v.append(l[x])
        m = m.labels(*v)
        return m

    def get_metircs(self, name="None", describe="This is generate from elastalert", labels={}):
        if name in self.metrics:
            return self.metrics[name]
        g = Counter(name, describe, labelnames=labels.keys())
        self.metrics[name] = g
        return g
