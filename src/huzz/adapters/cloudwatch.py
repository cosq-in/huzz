from datetime import datetime, timedelta
from typing import Optional
from ..models import HuzzEntity

try:
    import boto3
except ImportError:
    boto3 = None

class CloudWatchAdapter:
    """
    cloudwatch adapter: connects huzz to real-time aws metrics.
    requires boto3 (pip install "huzz[aws]")
    """
    def __init__(self, region: str = "us-east-1"):
        if boto3:
            self.cw = boto3.client('cloudwatch', region_name=region)
        else:
            self.cw = None

    def update_asset(self, asset: HuzzEntity):
        """
        automatically maps cloudwatch metrics to asset stats.
        uses metadata: cw_namespace, cw_name, cw_metric
        """
        if not self.cw:
            # simulated fallback logic for development
            import random
            asset.aura = random.randint(75, 100)
            asset.motion = abs(random.gauss(50, 20))
            return

        try:
            namespace = asset.metadata.get("cw_namespace", "AWS/EC2")
            name = asset.metadata.get("cw_name", asset.name)
            metric = asset.metadata.get("cw_metric", "CPUUtilization")
            dimension_name = "InstanceId" if "EC2" in namespace else "LoadBalancer"

            response = self.cw.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric,
                Dimensions=[{'Name': dimension_name, 'Value': name}],
                StartTime=datetime.utcnow() - timedelta(minutes=5),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )

            if response['Datapoints']:
                avg = response['Datapoints'][0]['Average']
                
                # logic pivot depending on metric type
                if metric == "CPUUtilization":
                    asset.aura = int(max(0, 100 - avg))
                    asset.motion = avg * 2
                else:
                    asset.motion = avg
                
                asset.fine_shi = asset.aura > 10
                asset.cooked = asset.aura < 5
                
        except Exception as e:
            asset.fine_shi = False
            asset.metadata["cw_error"] = str(e)
