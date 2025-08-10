"""
Simple boto3 helpers used by the Flask app.

Note: boto3 credentials should be configured on the host via environment
variables or ~/.aws/credentials as usual.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Any, List

import boto3
from botocore.exceptions import ClientError


def launch_ec2(ami: str, instance_type: str = 't3.micro', key_name: str | None = None) -> Dict[str, Any]:
    ec2 = boto3.client('ec2')
    params = dict(ImageId=ami, InstanceType=instance_type, MinCount=1, MaxCount=1)
    if key_name:
        params['KeyName'] = key_name
    resp = ec2.run_instances(**params)
    return resp['Instances'][0]


def terminate_ec2(instance_id: str) -> Dict[str, Any]:
    ec2 = boto3.client('ec2')
    resp = ec2.terminate_instances(InstanceIds=[instance_id])
    return resp['TerminatingInstances'][0]


def get_cloudwatch_logs(log_group: str, last_minutes: int = 60) -> List[Dict[str, Any]]:
    logs = boto3.client('logs')
    end_time = int(datetime.utcnow().timestamp() * 1000)
    start_time = int((datetime.utcnow() - timedelta(minutes=last_minutes)).timestamp() * 1000)

    resp = logs.filter_log_events(logGroupName=log_group, startTime=start_time, endTime=end_time, limit=500)
    events = [{'message': e['message'], 'timestamp': e['timestamp']} for e in resp.get('events', [])]
    return events