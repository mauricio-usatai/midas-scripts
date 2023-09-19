import time

import docker
from containers import (
    containers,
    configure_minio,
    wait_for_container,
)
from logger import (
    logging,
    log_execution,
)


logger = logging.getLogger()
docker_c = docker.from_env()


@log_execution
def run(container_name: str) -> None:
    docker_c.containers.run(
        **containers[container_name],
        detach=True,
    )
    wait_for_container(container_name)


def main():
    # Create container network
    if not docker_c.networks.list(names="midas"):
        docker_c.networks.create("midas", driver="bridge")

    # Start minio and create inital bucket
    docker_c.containers.run(
        **containers["minio"],
        detach=True,
    )

    time.sleep(5)  # Wait for MinIO to go up
    configure_minio()
    logger.info("Minio configured")

    # Run
    run("midas-news-parser")
    run("midas-news-scorer")
    run("midas-heuristic-scorer")


if __name__ == "__main__":
    main()
