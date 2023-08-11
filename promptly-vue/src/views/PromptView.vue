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
        <a-row :gutter='12'>
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


                <a-collapse>
                    <a-collapse-panel header="Prompt Args">

                        <a-list item-layout="horizontal" :data-source="args">
                            <template #renderItem="{ item }">
                                <a-list-item>
                                    <!-- <template #actions>
                            <a key="list-loadmore-edit">edit</a>
                            <a key="list-loadmore-more">more</a>
                        </template> -->
                                    <a-input-group>
                                        <a-space direction="horizontal">
                                            <a-typography-text>
                                                Key
                                            </a-typography-text>
                                            <a-input v-model:value="item.key"></a-input>

                                            <a-typography-text>
                                                Value
                                            </a-typography-text>
                                            <a-input v-model:value="item.value"></a-input>

                                        </a-space>

                                    </a-input-group>
                                </a-list-item>
                            </template>
                        </a-list>
                    </a-collapse-panel>
                </a-collapse>

                <a-divider></a-divider>


                <a-card title="Prompt">
                    <a-button @click="() => { prompt.messages.forEach((item) => item.enable = false) }">Disable
                        All
                    </a-button>
                    <a-button @click="() => { prompt.messages.forEach((item) => item.enable = true) }">Enable
                        All
                    </a-button>


                    <div>
                        <PromptInput :messages="prompt.messages" with-copy with-control
                            @order-up="index => order(index, -1)" @order-down="index => order(index, 1)"
                            @remove="index => deletePrompt(index)" @add="index => addPrompt(index, '')">

                        </PromptInput>
                    </div>

                    <a-divider>
                        <a-space>
                            <a-button @click="() => prompt.messages.push({})">
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
                            <a-button @click="commit">Commit</a-button>
                            <a-button @click="reload">Reload</a-button>
                            <a-button @click="gotoTesting">Goto Testing</a-button>
                            <a-button @click="gotoCommit">Goto Commit</a-button>
                        </a-space>

                    </a-space>
                </a-card>

                <a-card title="Corresponding Response">

                    <a-space direction="horizontal">
                        <a-button>Good</a-button>
                        <a-button>Bad</a-button>
                    </a-space>

                    <a-divider type="vertical"></a-divider>

                    <a-space>
                        <a-button @click="sendToPrompt">Append to prompt</a-button>
                    </a-space>

                    <a-divider></a-divider>

                    <a-textarea v-model:value="response" :auto-size="{ minRows: 20 }" placeholder="textarea with clear icon"
                        allow-clear />
                </a-card>

            </a-col>
        </a-row>
    </div>
</template>

<script lang="ts" setup>
import { useClipboard } from '@vueuse/core';
import { ref } from 'vue';

import { CopyOutlined, PlusOutlined } from '@ant-design/icons-vue';

import { useRoute } from 'vue-router';

import { useSnapshotStore } from '@/stores/snapshot';

import PromptInput from "@/components/PromptInput.vue";
import { ApiFactory, ApiHelper } from "@/scripts/api";
import { RouteHelper } from '@/scripts/router';
import type { NotificationPlacement } from "ant-design-vue";
import { notification } from 'ant-design-vue';
import type { Commit } from 'sdk/models';
import type { Message } from "../../sdk";
import PromptCard from '../components/PromptCard.vue';

const [notification_api, contextHolder] = notification.useNotification();

// use
const store = useSnapshotStore()
const r = useRoute()
const { text, copy, copied, isSupported } = useClipboard({})
const api = ApiFactory()
const key = r.params.key.toString()

// props
const props = defineProps<{
}>()

// field
console.log(store.source.args)
const args = ref(store.source.args)
const response = ref(<string>"")
const prompt = ref(
    {
        "history": [],
        "messages": <Message[]>[
            { id: 1, role: "角色1", content: "内容1", enable: true, order: 0 },
            // 其他数据项
        ],

    }
)

// created
fetchProfile(key);



// methods
function sendToPrompt() {
    addPrompt(prompt.value.messages[prompt.value.messages.length - 1].index, response.value)
}

function deletePrompt(order: number) {
    let ms = prompt.value.messages

    ms.splice(order, 1); // 删除指定索引的元素

    ms.forEach((elem, index) => elem.order = index)
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


async function commit() {
    await api.apiPromptKeyPost(prompt.value.messages, key)

    let commit: Commit = {
        messages: prompt.value.messages,
        response: response.value
    }
    api.apiCommitPost(commit, key,).then(() => {

    })
}

function addPrompt(index: number, content: string) {
    let m: Message = { content: content, role: 'user', enable: true, id: 0, order: 0 }
    prompt.value.messages.splice(index, 0, [m])

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


async function fetchProfile(key: string) {
    await api.apiPromptKeyGet(key)
        .then(response => {
            prompt.value = response.data;
            store.sendSource(key, prompt.value.messages, [])
        })
        .catch(error => {
            console.error(error);
            return null;
        });
}

function reload() {
    fetchProfile(key);
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
    await api.apiPromptKeyPost(prompt.value.messages, key)

    response.value = ''
    let res = await ApiHelper.doChat(key, prompt.value.messages, args.value)
    response.value = res.data;
}
</script>
  