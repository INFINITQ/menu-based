"""
Wrapper utilities for interacting with Docker using docker-py.
"""
from __future__ import annotations

from typing import Any, Dict, List

try:
    import docker
    from docker.errors import NotFound, APIError
except Exception:  # docker SDK optional at import-time
    docker = None


def client_available() -> bool:
    return docker is not None


def get_client():
    if docker is None:
        raise RuntimeError("docker SDK not installed. Install with: pip install docker")
    return docker.from_env()


def list_images() -> List[Dict[str, Any]]:
    c = get_client()
    imgs = c.images.list()
    return [{'id': i.short_id, 'tags': i.tags} for i in imgs]


def list_containers(all_containers: bool = False) -> List[Dict[str, Any]]:
    c = get_client()
    containers = c.containers.list(all=all_containers)
    return [{'id': cont.short_id, 'name': cont.name, 'status': cont.status} for cont in containers]


def start_container(name: str) -> Dict[str, Any]:
    c = get_client()
    try:
        cont = c.containers.get(name)
        cont.start()
        return {'status': 'started', 'id': cont.id}
    except NotFound as e:
        raise
    except APIError as e:
        raise


def stop_container(name: str) -> Dict[str, Any]:
    c = get_client()
    cont = c.containers.get(name)
    cont.stop()
    return {'status': 'stopped', 'id': cont.id}


def remove_container(name: str, force: bool = True) -> Dict[str, Any]:
    c = get_client()
    cont = c.containers.get(name)
    cont.remove(force=force)
    return {'status': 'removed', 'id': cont.id}


def remove_image(name: str, force: bool = True) -> Dict[str, Any]:
    c = get_client()
    c.images.remove(name=name, force=force)
    return {'status': 'image_removed', 'name': name}


def inspect_container(name: str) -> Dict[str, Any]:
    c = get_client()
    cont = c.containers.get(name)
    return cont.attrs


def get_logs(name: str, tail: int = 200) -> str:
    c = get_client()
    cont = c.containers.get(name)
    return cont.logs(tail=tail).decode(errors='ignore')