<style>
.scroll-short {
    height: 300px;
    /* 设置组件容器的固定高度 */
    overflow: auto;
    /* 设置溢出部分自动滚动 */
}
</style>

<template>
    <div>
        <a-row :gutter='12'>
            <a-col class="gutter-row" :span="14">
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


                    <div v-for="item in data.profile.messages" :key="item.id" class="card">
                        <!-- <template #extra><a href="#">more</a></template> -->

                        <a-row :gutter="12" align="middle">
                            <a-col :span="4">
                                <a-space direction="vertical">
                                    <!-- role select -->
                                    <a-select ref="select" v-model:value="item.role" style="width: 120px">
                                        <a-select-option value="user">
                                            <span style="color: black">User</span></a-select-option>
                                        <a-select-option value="system">
                                            <span style="color: red">System</span>
                                        </a-select-option>
                                        <a-select-option value="assistant">
                                            <span style="color: blue">Assistant</span>
                                        </a-select-option>
                                    </a-select>

                                    <!-- enable toggle -->
                                    <a-space direction="horizontal">
                                        Enable&nbsp;
                                        <a-switch v-model:checked="item.enable"></a-switch>
                                    </a-space>

                                </a-space>
                            </a-col>
                            <a-col :span="16">
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
                                                  @confirm="deletePrompt(item.id)">
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

            <a-col class="gutter-row" :span="10">

                <a-collapse>

                    <a-collapse-panel header="Snapshot">
                        <div class="scroll-short">

                            <div v-for="snapshot in data.profile.snapshots">
                                <a-divider>
                                    <a-button @click="useSnapshot(snapshot)">
                                        Use Snapshot
                                    </a-button>
                                </a-divider>
                                <PromptPreview :messages="snapshot"></PromptPreview>
                            </div>
                        </div>
                    </a-collapse-panel>
                </a-collapse>

                <a-card title="Operation">
                    <a-button @click="chat">Chat</a-button>
                    <a-button @click="snapshot">Snapshot</a-button>
                    <a-button @click="reload">Reload</a-button>
                    <a-button @click="goToDebug">Go To Debug</a-button>

                </a-card>


                <a-card title="Prompt Preview">
                    <div class="scroll-short">
                        <PromptPreview :messages="data.profile.messages.filter((i)=>i.enable)"></PromptPreview>
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
import type {Message, PromptItem} from "../../sdk";
import type {SnapshotRequest} from "../../sdk";

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
        "snapshots": [[{role: 'user', content: 'snapshot'}]]
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

function goToDebug() {
    store.sendToDebug(data.value.profile.messages)
    router.push('/view/debug')
}

function deletePrompt(id: number) {
    api.apiProfileKeyIdDelete(data.value.key, id).then(response => {
        data.value.profile = response.data
    })

}

function useSnapshot(snapshot: PromptItem[]) {
    console.log(snapshot)
    let target = data.value.profile.messages
    for (let i = 0; i < target.length; i++) {
        if (i >= snapshot.length) {
            target[i].enable = false
        } else {
            target[i].enable = true
            target[i].role = snapshot[i].role
            target[i].content = snapshot[i].content
        }

    }
}

function snapshot() {

    let key = data.value.key
    let snapshot: PromptItem[] = []
    data.value.profile.messages.forEach(
        (item: Message): any => {
            if (item.enable) {
                let res: PromptItem = {role: item.role, content: item.content}
                snapshot.push(res)
            }

        }
    )
    let body: SnapshotRequest = {snapshot: snapshot}
    api.apiProfileKeySnapshotPost(body, key,).then(() => {

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

    var cur = 0
    data.value.profile.messages.forEach((item) => {
        item.order = cur;
        cur++;
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
        })
        .catch(error => {
            console.error(error);
            return;
        });

}
</script>
  