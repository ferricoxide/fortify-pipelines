# Version Util Container

The `create_app_version.py` container is designed to be run as a simple, direct-execution, CI-focussed container. The container can be run either from local Docker service or (as it's primarily intended) via a GitLab Runner. The included `Dockerfile` has been tested to work against CentOS 7, CentOS 8-stream and UBI8 base container-images. Specifically, it has been tested against the official/public CentsOS 8-stream image hosted at [quay.io](https://quay.io/repository/centos/centos?tab=tags&tag=stream8): This is the default image used if `docker build` is invoked without appropriate, overriding `--build-arg` values

To generate a container that doen't use the official/public CentsOS 8-stream image hosted at quay.io, invoke the container build operation similarly to the following:

~~~
docker build \
  --build-arg DOCKER_REGISTRY="<REGISTRY_FQDN>" \
  --build-arg DOCKER_IMAGE="<SOURCE_IMAGE_REGISTRY_PATH>" \
  --build-arg DOCKER_VERSION="<SOURCE_IMAGE_VERSION_TAG>" \
  -t <REGISTRY_FQDN>/<DESTINATION_IMAGE_REGISTRY_PATH>/ssc-version-util:<SOURCE_IMAGE_VERSION_TAG> .
~~~
