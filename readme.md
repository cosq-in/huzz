# 💅 huzz

**huzz** is a cross-platform, full-screen tui observability toolkit. strictly lowercase, period-free, and always locked in.

## 🚀 high-utility observability

- **huzz**: the service/asset unit.
- **aura**: overall unit health/rizz (0-100).
- **motion**: real-time activity/throughput levels.
- **fine shi**: functional integrity (no lies detected).
- **is she going**: operational status (ready for the motion).
- **cooked**: critical infrastructure failure.

## 📦 installation

```bash
pip install huzz
```

### aws support
```bash
pip install "huzz[aws]"
```

## 📖 how it works (no cap)

### standard usage
```python
from huzz import HuzzRegistry, HuzzEntity
from huzz.cli import run_tui

infra = HuzzRegistry("tokyo-node-1")
infra.add_asset(HuzzEntity(name="api-v2", aura=99, locked_in=True))

run_tui(infra)
```

### core cloudwatch integration
`huzz` includes a built-in CloudWatch adapter.

```python
from huzz import HuzzRegistry, HuzzEntity, CloudWatchAdapter
from huzz.cli import run_tui

registry = HuzzRegistry("aws-monitor")
adapter = CloudWatchAdapter(region="us-east-1")

registry.add_asset(HuzzEntity(
    name="my-ec2-instance", 
    type="EC2", 
    metadata={"cw_name": "i-0abc12345"}
))

# use the core adapter in the audit loop
registry.audit(update_fn=adapter.update_asset)
run_tui(registry)
```

## 💅 cli toolkit
type `huzz` in your terminal to see the live dashboard. supports windows, linux, and macos.

## 🙏 credits & inspiration
inspired by **cj.mcc_**. 
- **creator**: [cj.mcc_ (@cj.mcc_)](https://www.instagram.com/cj.mcc_/)

---
*stay locked in, keep the motion going.*
