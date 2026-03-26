import sys
import os
import time
from datetime import datetime, timedelta

# ensure local src is used
sys.path.append(os.path.join(os.getcwd(), "src"))

from huzz import HuzzRegistry, HuzzEntity
from huzz.cli import run_tui

# try to import boto3, fallback to mock if not installed
try:
    import boto3
except ImportError:
    print("💅 [dim]boto3 not found. installing...[/dim]")
    boto3 = None

class CloudWatchAdapter:
    """connects huzz to aws cloudwatch."""
    def __init__(self, region="us-east-1"):
        if boto3:
            self.cw = boto3.client('cloudwatch', region_name=region)
        else:
            self.cw = None

    def update_huzz(self, asset: HuzzEntity):
        """maps cloudwatch metrics to huzz slang."""
        if not self.cw:
            # simulated data if boto3 is missing
            import random
            asset.aura = random.randint(70, 100)
            asset.motion = abs(random.gauss(100, 20))
            asset.fine_shi = True
            return

        # real cloudwatch lookup logic (example: CPU Utilization)
        try:
            name = asset.metadata.get("cw_name", asset.name)
            namespace = asset.metadata.get("cw_namespace", "AWS/EC2")
            
            response = self.cw.get_metric_statistics(
                Namespace=namespace,
                MetricName="CPUUtilization",
                Dimensions=[{'Name': 'InstanceId', 'Value': name}],
                StartTime=datetime.utcnow() - timedelta(minutes=5),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                avg_cpu = response['Datapoints'][0]['Average']
                # aura = inverse of cpu pressure
                asset.aura = int(max(0, 100 - avg_cpu))
                asset.motion = avg_cpu * 1.5 # arbitrary motion scale
                asset.fine_shi = avg_cpu < 90 # cooked if over 90%
                asset.cooked = avg_cpu > 95
        except Exception as e:
            asset.fine_shi = False
            asset.metadata["error"] = str(e)

def main():
    """dev x cloudwatch demo."""
    registry = HuzzRegistry("AWS Cloud-Vibe Monitor")
    adapter = CloudWatchAdapter()

    # add your ec2 huzz units
    registry.add_asset(HuzzEntity(
        name="i-0abc123def456", 
        type="EC2", 
        metadata={"cw_name": "i-0abc123def456", "env": "prod"}
    ))
    
    registry.add_asset(HuzzEntity(
        name="payment-service-lb", 
        type="ALB", 
        metadata={"cw_namespace": "AWS/ApplicationELB"}
    ))

    # run the live dashboard with the cloudwatch auditor
    run_tui(registry, duration=None)

if __name__ == "__main__":
    main()
