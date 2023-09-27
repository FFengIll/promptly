# prompt

The prompt engineering tools.

# deps

- python: fastapi
- typescript: vuejs v3
- build: taskfile, poetry, pnpm
  - `brew install go-task`
  - `pip install poetry`
  - `npm install -g pnpm`
- db: mongodb
- env: docker
  - install docker desktop: https://www.docker.com/products/docker-desktop/
- ~~(DEPRECATED) gui: pysimplegui~~

# run

- task install
- task build
- task run

> task is coming from `Taskfile`, you must install `task`.
> see [Taskfile](https://taskfile.dev/) for more details.
> see [Install](https://taskfile.dev/installation/) to install `task`.

# features

- build a prompt.
- run a prompt (with available model service).
- using arguments for prompt.
- commit prompt into commit repository to save a snapshot.
- testing a prompt (with loop or cases).
