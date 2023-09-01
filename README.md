# prompt

The prompt engineering tools.

# deps

- python: fastapi
- typescript: vuejs v3
- build: taskfile, poetry, pnpm
- db: mongodb
- env: docker
- (DEPRECATED) gui: pysimplegui

# run

- task install
- task build
- task run

> task is coming from `Taskfile`, you must install `task`.
> see [Taskfile](https://taskfile.dev/) for more details.
> see [Install](https://taskfile.dev/installation/) to install `task`.

# features

- build a prompt
- run a prompt (with available model service)
- using arguments for prompt
- commit prompt into history to save snapshot
- testing a prompt (with loop and cases)
