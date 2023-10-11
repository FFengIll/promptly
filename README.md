# prompt

The prompt engineering tools.

# features

- build a prompt.
- run a prompt (with available model service).
- using arguments for prompt.
- commit prompt into commit repository to save a snapshot.
- testing a prompt (with loop or cases).

# deps

- python: 3.8 and above
  - use fastapi for backend
- typescript:
  - use vuejs v3 for front
- build tools: taskfile, poetry, pnpm
  - `brew install go-task node swagger-codegen`
  - `pip install poetry`
    - if it is too slow, try `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
  - `npm install -g pnpm`
    - if it is too slow, try `npm config set registry https://registry.npmmirror.com`
- db: mongodb
- env: docker
  - install docker desktop: https://www.docker.com/products/docker-desktop/
  - use image container for db
- ~~(DEPRECATED) gui: pysimplegui~~

# run

## run in docker

run bellow

```sh
# start db
task db-start

# start promptly
...
```

> visit `localhost:8000` to use.

## build to run

- task install
- task dist
- task run

> task is coming from `Taskfile`, you must install `task`.
> see [Taskfile](https://taskfile.dev/) for more details.
> see [Install](https://taskfile.dev/installation/) to install `task`.

## build to dev

- task install
- task dev
- task run

# config

LLM api token is sensitive, so we only put a separate file for it.

```sh
# create and writhe this file for LLM api url and key
vim promptly/config.py

# with bellow content; use your own url and key
key = "fake_cq5gn6rkyjgom6ocpeevuhjn7x8phaly"
url = "http://localhost:8080/api/v1"

# or run export to set env; use your own url and key
export LLM_KEY="fake_cq5gn6rkyjgom6ocpeevuhjn7x8phaly"
export LLM_API="http://localhost:8080/api/v1"
```

By default, promptly use `gpt-3.5-turbo` (the latest).

Some other LLM is hardcode in `web/src/scripts/llm.ts`, you may edit it for your own.

If you can not access LLM service, config your proxy first.
e.g.

```shell
export ALL_PROXY="socks5h://0.0.0.0:10888"
```