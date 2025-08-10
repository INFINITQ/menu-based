"""
Minimal AWS boto3 wrappers for EC2 launch/terminate and CloudWatch logs.

This file expects AWS credentials to be configured in the environment or via
~/.aws/credentials on the RHEL host.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, jsonify, request

from app.auth import login_required

aws_bp = Blueprint('aws_api', __name__)


@aws_bp.route('/launch_ec2', methods=['POST'])
@login_required
def launch_ec2():
    payload = request.json or {}
    ami = payload.get('ami') or os.environ.get('DEFAULT_AMI')
    instance_type = payload.get('instance_type') or 't3.micro'
    key_name = payload.get('key_name')

    if not ami:
        return jsonify({'error': 'ami is required'}), 400

    ec2 = boto3.client('ec2')
    try:
        resp = ec2.run_instances(ImageId=ami, InstanceType=instance_type, MinCount=1, MaxCount=1, KeyName=key_name)
        inst = resp['Instances'][0]
        return jsonify({'instance_id': inst['InstanceId'], 'state': inst['State']}), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500


@aws_bp.route('/terminate_ec2', methods=['POST'])
@login_required
def terminate_ec2():
    payload = request.json or {}
    instance_id = payload.get('instance_id')
    if not instance_id:
        return jsonify({'error': 'instance_id required'}), 400
    ec2 = boto3.client('ec2')
    try:
        resp = ec2.terminate_instances(InstanceIds=[instance_id])
        return jsonify(resp['TerminatingInstances'][0]), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500


@aws_bp.route('/cloudwatch_logs', methods=['POST'])
@login_required
def cloudwatch_logs():
    payload = request.json or {}
    log_group = payload.get('log_group')
    start_minutes = int(payload.get('last_minutes', 60))

    if not log_group:
        return jsonify({'error': 'log_group required'}), 400

    logs = boto3.client('logs')
    end_time = int(datetime.utcnow().timestamp() * 1000)
    start_time = int((datetime.utcnow() - timedelta(minutes=start_minutes)).timestamp() * 1000)

    try:
        resp = logs.filter_log_events(logGroupName=log_group, startTime=start_time, endTime=end_time, limit=100)
        events = [{'message': e['message'], 'timestamp': e['timestamp']} for e in resp.get('events', [])]
        return jsonify({'events': events}), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500
