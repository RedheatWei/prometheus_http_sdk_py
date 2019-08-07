# A simple prometheus http sdk

## Example

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
        step=15
    )
print(data)
```

* cover to dict

```python
data.coverDict()
```

* cover to json

```python
data.coverJson()
```