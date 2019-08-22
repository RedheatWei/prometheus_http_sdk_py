# A simple prometheus http sdk

## Example

* import
```python
from prometheus_http_sdk.prometheus_http import PrometheusApi
```

* get data
```python
data = PrometheusApi("http://prometheus").query_range(
        query=":node_cpu_saturation_load1:",
        range_time="6h",
    )
print(data)
```

* get all data
```python
data = PrometheusApi("http://prometheus").query_all(
        query=":node_cpu_saturation_load1:",
        step=60,
        end=time.time()-600
    )
print(data)
```

* convert to dict

```python
data.convertDict()
```

* convert to dict with tensorflow type

```python
data.convertDict(tfType=True)
```


* convert to json

```python
data.convertJson()
```