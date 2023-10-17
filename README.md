# Promptly

The prompt engineering tools.

# Features

- build a prompt.
- run a prompt (with available model service).
- using arguments for prompt.
- commit prompt into commit repository to save a snapshot.
- testing a prompt (with loop or cases).

# Deps

- python: 3.8 and above
  - use fastapi for backend
- typescript:
  - use vuejs v3 for front
- build tools: taskfile, poetry, pnpm
  - `brew install go-task node swagger-codegen`
  - `pip3 install poetry`
    - if it is too slow, try `pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
  - `npm install -g pnpm`
    - if it is too slow, try `npm config set registry https://registry.npmmirror.com`
- db: mongodb
- env: docker
  - install docker desktop: https://www.docker.com/products/docker-desktop/
  - use image container for db
- ~~(DEPRECATED) gui: pysimplegui~~

# Run

## Install & Run [recommand]

- task install
- task dist
- task run

> task is coming from `Taskfile`, you must install `task`.
> see [Taskfile](https://taskfile.dev/) for more details.
> see [Install](https://taskfile.dev/installation/) to install `task`.

## Build & Dev [for developer only]

- task install
- task dev
- task run

## Run With Docker [WIP]

run bellow

```sh
# start db
task db-start

# start promptly
...
```

> visit `localhost:8000` to use.


# Data
Run `task data-dump` to dump your data into `data/mongodb.zip`.

While put file to `data/mongodb.zip`, run `task data-load` will load your data with db restart.

# Config

LLM api token is sensitive, so we only put a separate file for it.

- run `task config` to generate config file `config/llm.yaml`.
- edit `config/llm.yaml` with your own info.
- by default, `task run` will load `config/llm.yaml`.

Since some areas are block by OpenAI, if you can not access LLM service, config your proxy at first.
e.g.
```shell
export ALL_PROXY="socks5h://0.0.0.0:10888"
```