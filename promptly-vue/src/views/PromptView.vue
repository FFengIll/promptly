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
        <a-row :gutter='12'>
            <a-col class="gutter-row" :span="12">
                <a-collapse>
                    <a-collapse-panel header="History">
                        <div v-for="h in data.profile.history">
                            <a-space direction="horizontal" align="baseline">
                                <a-button @click="copy(h)">
                                    <template #icon>
                                        <CopyOutlined/>
                                    </template>
                                </a-button>
                                <p>{{ h }}</p>
                                <!-- <a-textarea v-bind="h"> </a-textarea> -->


                                <!-- <button v-on:click="setContent(item.id, h)">Set</button> -->

                            </a-space>
                        </div>
                    </a-collapse-panel>
                </a-collapse>
                <a-card title="Prompt">
                    <a-button @click="() => { data.profile.messages.forEach((item) => item.enable = false) }">Disable
                        All
                    </a-button>
                    <a-button @click="() => { data.profile.messages.forEach((item) => item.enable = true) }">Enable
                        All
                    </a-button>

                    <a-divider>
                        <a-space>
                            <a-button @click="()=>data.profile.messages.unshift({})">
                                <template #icon>
                                    <PlusOutlined/>
                                </template>
                            </a-button>
                        </a-space>

                    </a-divider>


                    <div v-for="item in data.profile.messages" :key="item.id" class="card">
                        <!-- <template #extra><a href="#">more</a></template> -->


                        <a-row>


                            <!-- role -->
                            <a-space direction="vertical">

                                <a-radio-group v-model:value="item.role" option-type="button" button-style="solid">
                                    <a-radio-button value="user">User</a-radio-button>
                                    <a-radio-button value="system">System</a-radio-button>
                                    <a-radio-button value="assistant">Assitant</a-radio-button>
                                </a-radio-group>
                            </a-space>

                            <!-- role select -->
                            <!-- <a-select ref="select" v-model:value="item.role" style="width: 120px">
                                <a-select-option value="user">
                                    <span style="color: black">User</span></a-select-option>
                                <a-select-option value="system">
                                    <span style="color: red">System</span>
                                </a-select-option>
                                <a-select-option value="assistant">
                                    <span style="color: blue">Assistant</span>
                                </a-select-option>
                            </a-select> -->

                            <!-- enable toggle -->
                            <a-space direction="horizontal">
                                <span></span>
                                <a-typography-text>Enable</a-typography-text>
                                <a-switch v-model:checked="item.enable"></a-switch>
                            </a-space>
                        </a-row>
                        <a-row :gutter="12" align="middle">


                            <a-col :span="20">
                                <!-- content edit -->
                                <a-textarea v-model:value="item.content" placeholder="textarea with clear icon"
                                            allow-clear
                                            :auto-size="{ minRows: 3, maxRows: 5 }"/>

                            </a-col>

                            <a-col :span="2">
                                <a-space direction="vertical">
                                    <!-- up down the order -->
                                    <a-button type="primary" shape="round" @click="order(item.id, -1)">
                                        <template #icon>
                                            <UpOutlined/>
                                        </template>
                                    </a-button>
                                    <a-button type="primary" shape="round" @click="order(item.id, 1)">
                                        <template #icon>
                                            <DownOutlined/>
                                        </template>
                                    </a-button>
                                </a-space>
                            </a-col>
                            <a-col :span="2">
                                <a-space direction="vertical">

                                    <a-popconfirm title="Are you sure delete this task?" ok-text="Yes" cancel-text="No"
                                                  @confirm="deletePrompt(item.order)">
                                        <a-button>
                                            <template #icon>
                                                <CloseOutlined/>
                                            </template>
                                        </a-button>
                                    </a-popconfirm>


                                </a-space>
                            </a-col>
                        </a-row>

                        <a-divider>
                            <a-space>
                                <a-button @click="addPrompt(item.id, '')">
                                    <template #icon>
                                        <PlusOutlined/>
                                    </template>
                                </a-button>
                            </a-space>

                        </a-divider>

                    </div>

                </a-card>
            </a-col>

            <a-col class="gutter-row" :span="12">

                <a-collapse>

                    <a-collapse-panel header="Snapshot">
                        <div class="scroll-short">

                            <div v-for="snapshot in data.profile.snapshots">
                                <a-divider>
                                    <a-button @click="useSnapshot(snapshot)">
                                        Use Snapshot
                                    </a-button>
                                </a-divider>
                                <PromptPreview :messages="snapshot.prompt"></PromptPreview>
                                <a-textarea v-model:value="snapshot.response">

                                </a-textarea>
                            </div>
                        </div>
                    </a-collapse-panel>
                </a-collapse>

                <a-card title="Operation">
                    <a-button @click="chat">Chat</a-button>
                    <a-button @click="snapshot">Snapshot</a-button>
                    <a-button @click="reload">Reload</a-button>
                    <a-button @click="goToDebug">Go To Debug</a-button>
                    <a-button @click="openNotification('test','info')">Notice</a-button>

                </a-card>


                <a-card title="Prompt Preview">
                    <div class="scroll-short">
                        <PromptPreview :messages="data.profile.messages.filter((i) => i.enable)"></PromptPreview>
                    </div>
                </a-card>
                <a-card title="Corresponding Response">
                    <a-space direction="horizontal">
                        <a-button @click="sendToPrompt">Send To Prompt</a-button>
                        <a-button>Good</a-button>
                        <a-button>Bad</a-button>
                    </a-space>
                    <a-textarea v-model:value="data.response" :auto-size="{ minRows: 20 }"
                                placeholder="textarea with clear icon" allow-clear/>
                </a-card>

            </a-col>
        </a-row>
    </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue';
import useClipboard from 'vue-clipboard3';

import {CloseOutlined, CopyOutlined, DownOutlined, PlusOutlined, UpOutlined} from '@ant-design/icons-vue';

import {useRoute, useRouter} from 'vue-router';
import {DefaultApiFactory} from '../../sdk/apis/default-api';

import {useSnapshotStore} from '@/stores/snapshot';

import PromptPreview from '../components/PromptPreview.vue';
import type {Message, PromptItem, Snapshot} from "../../sdk";
import type {NotificationPlacement} from "ant-design-vue";
import {notification} from 'ant-design-vue';

const [notification_api, contextHolder] = notification.useNotification();

// use
const store = useSnapshotStore()
const router = useRouter()
const {toClipboard} = useClipboard()

const api = DefaultApiFactory(undefined, "http://localhost:8000")

// field
const data = ref({
    key: "",
    history: [{
        messages: [
            {id: 1, role: "角色1", content: "内容1", enable: true, order: 0},
        ],
        response: ""
    }],
    response: "",
    profile: {
        "history": ["1"],
        "messages": [
            {id: 1, role: "角色1", content: "内容1", enable: true, order: 0, history: []},
            // 其他数据项
        ],
        "snapshots": [
            {
                "prompt": [
                    {role: 'user', content: 'snapshot'}
                ],
                "response": ""
            }
        ]
    }
})

// created
const route = useRoute();
data.value.key = route.params.key.toString();
fetchProfile(data.value.key);

// methods
function sendToPrompt() {
    addPrompt(data.value.profile.messages[data.value.profile.messages.length - 1].id, data.value.response)
}

function deletePrompt(order: number) {
    let ms = data.value.profile.messages

    ms.splice(order, 1); // 删除指定索引的元素

    ms.forEach((elem, index) => elem.order = index)
}

function goToDebug() {
    store.sendToDebug(data.value.profile.messages)
    router.push('/view/debug')
}

function useSnapshot(snapshot: Snapshot) {
    console.log(snapshot)
    let target = data.value.profile.messages
    let prompt = snapshot.prompt
    data.value.response = snapshot.response
    for (let i = 0; i < target.length; i++) {
        if (i >= prompt.length) {
            target[i].enable = false
        } else {
            target[i].enable = true
            target[i].role = prompt[i].role
            target[i].content = prompt[i].content
        }

    }
}

function snapshot() {

    let key = data.value.key
    let prompt: PromptItem[] = []
    data.value.profile.messages.forEach(
        (item: Message): any => {
            if (item.enable) {
                let res: PromptItem = {role: item.role, content: item.content}
                prompt.push(res)
            }

        }
    )
    let snapshot: Snapshot = {prompt: prompt, response: data.value.response}
    api.apiProfileKeySnapshotPost(snapshot, key,).then(() => {

    })
}

function addPrompt(id: number, content: string) {
    let index = data.value.profile.messages.findIndex((item) => item.id == id)
    let order = data.value.profile.messages[index].order
    let max_id = 0
    data.value.profile.messages.forEach((item) => {
        if (item.id > max_id) {
            max_id = item.id
        }
    })

    data.value.profile.messages.splice(
        index + 1,
        0,
        {role: "user", id: max_id + 1, enable: true, content: content, order: order, history: []}
    )

    data.value.profile.messages.forEach((elem, index) => {
        elem.order = index;
        elem.id = index
    })

    console.log(data.value.profile.messages)
}

function order(id: number, delta: number) {
    let index = data.value.profile.messages.findIndex((m) => {
        return (m.id == id)
    })

    if (index < 0) {
        return
    }

    console.log(index)

    let temp = data.value.profile.messages[index]
    data.value.profile.messages[index] = data.value.profile.messages[index + delta]
    data.value.profile.messages[index + delta] = temp

    for (var i = 0; i < data.value.profile.messages.length; i++) {
        data.value.profile.messages[i].order = i
    }

    console.log(data.value.profile.messages)
}

function setContent(id: number, content: string) {
    data.value.profile.messages.forEach((m) => {
        if (m.id == id) {
            m.content = content
        }
    })
}

async function copy(content: string) {
    await toClipboard(content)
}

async function fetchProfile(key: string) {
    api.apiProfileKeyGet(key)
        .then(response => {
            data.value.profile = response.data;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
}

function reload() {
    fetchProfile(data.value.key);
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
    var res = data.value.profile.messages;
    console.log(res);
    api.apiChatKeyPost(res, data.value.key)
        .then(response => {
            data.value.response = response.data;
            console.log("result", response.data);
            console.log("data.value.response", data.value.response)
            data.value.history.push(
                {
                    messages: data.value.profile.messages,
                    response: response.data
                }
            )

            return data.value.response
        })
        .then((msg: string) => {
            openNotification(msg, 'success')
        })
        .catch(error => {
            openNotification(error, 'error')
            console.error(error.toString());
            return;
        });

}
</script>
  