"""
Docker API endpoints using docker SDK (docker-py).

Provides REST endpoints for the basic docker actions you specified.
"""
from __future__ import annotations

import typing
from flask import Blueprint, jsonify, request

try:
    import docker
except Exception:  # pragma: no cover - docker SDK optional
    docker = None

from app.auth import login_required

docker_bp = Blueprint('docker_api', __name__)


def get_client():
    if docker is None:
        raise RuntimeError('docker SDK not installed')
    return docker.from_env()


@docker_bp.route('/images', methods=['GET'])
@login_required
def list_images():
    client = get_client()
    images = client.images.list()
    result = [{'id': img.short_id, 'tags': img.tags} for img in images]
    return jsonify(result)


@docker_bp.route('/containers', methods=['GET'])
@login_required
def list_containers():
    client = get_client()
    all_flag = request.args.get('all', 'false').lower() == 'true'
    containers = client.containers.list(all=all_flag)
    result = [{'id': c.short_id, 'name': c.name, 'status': c.status} for c in containers]
    return jsonify(result)


@docker_bp.route('/start', methods=['POST'])
@login_required
def start_container():
    payload = request.json or {}
    name = payload.get('name')
    if not name:
        return jsonify({'error': 'container name required'}), 400
    client = get_client()
    try:
        container = client.containers.get(name)
        container.start()
        return jsonify({'status': 'started', 'id': container.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@docker_bp.route('/stop', methods=['POST'])
@login_required
def stop_container():
    payload = request.json or {}
    name = payload.get('name')
    if not name:
        return jsonify({'error': 'container name required'}), 400
    client = get_client()
    try:
        container = client.containers.get(name)
        container.stop()
        return jsonify({'status': 'stopped', 'id': container.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@docker_bp.route('/rm', methods=['POST'])
@login_required
def remove_container():
    payload = request.json or {}
    name = payload.get('name')
    if not name:
        return jsonify({'error': 'container name required'}), 400
    client = get_client()
    try:
        container = client.containers.get(name)
        container.remove(force=True)
        return jsonify({'status': 'removed', 'id': container.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@docker_bp.route('/rmi', methods=['POST'])
@login_required
def remove_image():
    payload = request.json or {}
    name = payload.get('name')
    if not name:
        return jsonify({'error': 'image name required'}), 400
    client = get_client()
    try:
        client.images.remove(name=name, force=True)
        return jsonify({'status': 'image_removed', 'name': name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@docker_bp.route('/inspect', methods=['GET'])
@login_required
def inspect_container():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'container name required'}), 400
    client = get_client()
    try:
        container = client.containers.get(name)
        return jsonify(container.attrs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@docker_bp.route('/logs', methods=['GET'])
@login_required
def container_logs():
    name = request.args.get('name')
    tail = int(request.args.get('tail', '200'))
    if not name:
        return jsonify({'error': 'container name required'}), 400
    client = get_client()
    try:
        container = client.containers.get(name)
        logs = container.logs(tail=tail).decode(errors='ignore')
        return jsonify({'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500