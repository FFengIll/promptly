<style>
.scroll-short {
    height: 200px;
    /* 设置组件容器的固定高度 */
    overflow: auto;
    /* 设置溢出部分自动滚动 */
}
</style>

<template>
    <div>
        <a-typography-title>{{ key }}</a-typography-title>
        <a-row :gutter='6'>
            <a-col class="gutter-row" :span="12">

                <a-collapse>
                    <a-collapse-panel header="History">
                        <a-space direction="horizontal" align="baseline" v-for="h in prompt.history">
                            <a-button @click="copy(h)">
                                <template #icon>
                                    <CopyOutlined />
                                </template>
                            </a-button>
                            <p>{{ h }}</p>
                            <!-- <a-textarea v-bind="h"> </a-textarea> -->


                            <!-- <button v-on:click="setContent(item.index, h)">Set</button> -->

                        </a-space>
                    </a-collapse-panel>
                </a-collapse>

                <a-card title="Argument">

                    <template #extra>
                        <a-button @click="fetchArgument(key)">
                            <template #icon>
                                <SyncOutlined />
                            </template>
                        </a-button>
                    </template>

                    <CaseInput :setting="argSetting" :args="args" @select=selectArg>
                        <template #extra>
                            <a-row justify="center">
                                <a-space direction="horizontal">


                                    <a-select ref="select" v-model:value="argKey" style="width: 120px" show-search>
                                        <a-select-option v-for="k in args.keys()" :key="k">{{ k }}</a-select-option>
                                    </a-select>

                                    <a-input v-model:value="argKey">
                                    </a-input>

                                    <a-input v-model:value="argValue">
                                    </a-input>

                                    <a-button @click="newArg()">
                                        <template #icon>
                                            <PlusOutlined />
                                        </template>
                                        New
                                    </a-button>
                                </a-space>

                            </a-row>

                        </template>
                    </CaseInput>


                </a-card>


                <a-divider></a-divider>

                <a-card title="Model">

                    <template #extra>
                        <ModelSelect :model="model" :defaultModel="(() => { return prompt.defaultModel })()"
                            v-on:select="(value) => { model = value }" v-on:default="(value) => {
                                    let body: UpdatePromptBody = <UpdatePromptBody>({ defaultModel: value })
                                    backend.apiPromptNamePut(body, prompt.name)
                                        .then(() => {
                                            console.log(value)
                                            prompt.defaultModel = value
                                        })

                                }
                                " style="width: 200px">

                        </ModelSelect>
                        <a-button @click="fetchArgument(key)">
                            <template #icon>
                                <SyncOutlined />
                            </template>
                        </a-button>
                    </template>

                </a-card>

                <a-divider></a-divider>

                <a-card title="Prompt">
                    <template #extra>
                        <a-button @click="reload">

                            <template #icon>
                                <SyncOutlined />
                            </template>
                        </a-button>
                    </template>

                    <a-row justify="end">
                        <a-button @click="() => { prompt.messages.forEach((item) => item.enable = false) }">Disable
                            All
                        </a-button>
                        <a-button @click="() => { prompt.messages.forEach((item) => item.enable = true) }">Enable
                            All
                        </a-button>
                    </a-row>

                    <a-row justify="space-around">
                        <PromptInput :messages="prompt.messages" with-copy with-control
                            @order-up="index => order(index, -1)" @order-down="index => order(index, 1)"
                            @remove="index => deletePrompt(index)" @add="index => addPrompt(index, '')">
                        </PromptInput>
                    </a-row>

                    <a-divider>
                        <a-space>
                            <a-button @click="() => prompt.messages.push({ role: 'system', enable: true, content: '' })">
                                <template #icon>
                                    <PlusOutlined />
                                </template>
                            </a-button>
                        </a-space>

                    </a-divider>

                </a-card>

            </a-col>


            <a-col class="gutter-row" :span="12">


                <a-collapse>

                    <a-collapse-panel header="Prompt Preview">
                        <PromptCard :messages="prompt.messages.filter((i) => i.enable)"></PromptCard>
                    </a-collapse-panel>
                </a-collapse>


                <a-card title="Operation">
                    <a-space direction="vertical">
                        <a-space direction="horizontal">
                            <a-button @click="chat">Request</a-button>
                            <a-button @click="doCommit">Commit</a-button>
                        </a-space>
                        <a-space direction="horizontal">
                            <a-button @click="gotoTesting">Goto Testing</a-button>
                            <a-button @click="gotoCommit">Goto Commit</a-button>
                        </a-space>

                    </a-space>
                </a-card>

                <a-card title="Corresponding Response">
                    <a-skeleton :loading="loading" active avatar>
                        <div>
                            <a-space direction="horizontal">
                                <a-button>Good</a-button>
                                <a-button>Bad</a-button>
                            </a-space>

                            <a-divider type="vertical"></a-divider>

                            <a-space>
                                <a-button @click="responseToPrompt">Append to prompt</a-button>
                            </a-space>

                            <a-divider></a-divider>

                            <a-textarea v-model:value="response" :auto-size="{ minRows: 20 }"
                                placeholder="textarea with clear icon" allow-clear />
                        </div>
                    </a-skeleton>

                </a-card>

            </a-col>
        </a-row>
    </div>
</template>

<script lang="ts" setup>
import { useClipboard } from '@vueuse/core';
import { onMounted, ref } from 'vue';

import { CopyOutlined, PlusOutlined, SyncOutlined } from '@ant-design/icons-vue';

import { useRoute } from 'vue-router';

import { useSnapshotStore } from '@/stores/snapshot';

import CaseInput from '@/components/CaseInput.vue';
import ModelSelect from '@/components/ModelSelect.vue';
import PromptInput from "@/components/PromptInput.vue";
import { BackendHelper, backend } from "@/scripts/backend";
import { RouteHelper } from '@/scripts/router';
import type { NotificationPlacement } from "ant-design-vue";
import { notification } from 'ant-design-vue';
import type { ArgRequest, Argument, ArgumentSetting, Message, NewCommitBody, Prompt, UpdatePromptBody } from "../../sdk";
import PromptCard from '../components/PromptCard.vue';

const [notification_api, contextHolder] = notification.useNotification();

// use
const store = useSnapshotStore()
const r = useRoute()
const { text, copy, copied, isSupported } = useClipboard({})

const key = r.params.key.toString()

// props
const props = defineProps<{}>()

// field
console.log(store.source.args)

const loading = ref(false)
const model = ref<string>("")

const argValue = ref<string>("")
const argKey = ref<string>("")
const response = ref(<string>"")
const argSetting = ref<ArgumentSetting>(
    {
        name: "",
        args: {}
    }
)
const args = ref<Argument[]>([])
const prompt = ref<Prompt>(
    <Prompt>{
        "history": [],
        "messages": <Message[]>[
            { role: "角色1", content: "内容1", enable: true },
            // 其他数据项
        ],
        model: "",
    }
)

// created
onMounted(
    () => {
        fetchPrompt(key)

    }
)


function selectArg(key: string, value: string) {
    for (const item of args.value) {
        if (item.key == key) {
            item.value = value
            return
        }
    }
    args.value.push({ key: key, value: value })
}

async function newArg() {
    let body: ArgRequest = {
        key: argKey.value,
        value: argValue.value
    }

    if (argKey.value == "" || argValue.value == "") {
        return
    }

    await backend.apiPromptArgsNamePut(body, key)
        .then(response => {
            selectArg(argKey.value, argValue.value)
        })

    await fetchArgument(key)

}


// methods
function responseToPrompt() {
    addPrompt(prompt.value.messages.length - 1, response.value)
}

function deletePrompt(index: number) {
    let ms = prompt.value.messages

    ms.splice(index, 1); // 删除指定索引的元素
}

function gotoCommit() {
    console.log(key)

    store.sendSource(key, prompt.value.messages, [])
    RouteHelper.toCommit(key)
}

function gotoTesting() {
    store.sendSource(key, prompt.value.messages, [])
    RouteHelper.toTesting(key)
}


async function doCommit() {
    let body: NewCommitBody = {
        name: key,
        commit: {
            messages: prompt.value.messages,
            response: response.value,
            args: args.value,
            model: model.value,
        },
    }
    backend.apiCommitPost(body).then(() => {

    })
}

function addPrompt(index: number, content: string) {
    let m: Message = { content: content, role: 'user', enable: true, }
    prompt.value.messages.splice(index, 0, m)

    console.log(prompt.value.messages)
}

function order(index: number, delta: number) {
    let another = index + delta
    console.log('index', index, another)
    if (another < 0 || another >= prompt.value.messages.length) {
        return
    }
    let current = prompt.value.messages[index]
    let next = prompt.value.messages[index + delta]

    prompt.value.messages[index] = next
    prompt.value.messages[index + delta] = current

    console.log(prompt.value.messages)
}


async function fetchArgument(name: string) {
    await backend.apiPromptArgsNameGet(name)
        .then(response => {
            argSetting.value = response.data

            console.log('response', argSetting.value)

        }).catch(error => {
            console.log(error)
        })

}

async function fetchPrompt(name: string) {
    await fetchArgument(name)

    await backend.apiPromptNameGet(name)
        .then(response => {
            console.log(response.data)
            prompt.value = response.data;

            model.value = prompt.value.model
            console.log(model.value)

            args.value = prompt.value.args
            console.log(args.value)

        })
        .catch(error => {
            console.error(error);
            return null;
        });
}

function reload() {
    fetchPrompt(key);
}


function openNotification(message: string, status: string) {
    let placement: NotificationPlacement = 'bottomRight'
    notification[status]({
        message: status,
        description: message,
        placement,
    });
}

async function chat() {
    console.log("model", model.value)
    console.log(prompt.value.messages)
    let body: UpdatePromptBody = {
        messages: prompt.value.messages!!,
        model: model.value,
        args: args.value,
    }
    await backend.apiPromptNamePut(body, key)

    loading.value = true

    response.value = ''
    let res = await BackendHelper.doChat(model.value, prompt.value.messages, args.value)
    response.value = res.data;

    loading.value = false
}
</script>
