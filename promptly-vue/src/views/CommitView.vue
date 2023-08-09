<script setup lang="ts">
import PromptInput from "@/components/PromptInput.vue";
import router from "@/router";
import { ApiFactory } from "@/scripts/api";
import { RouteHelper } from "@/scripts/router";
import { format } from "@/scripts/template";
import { useSnapshotStore } from "@/stores/snapshot";
import { PlusOutlined, SyncOutlined } from "@ant-design/icons-vue";
import { storeToRefs } from "pinia";
import type { Argument, CommitRequest, Message } from "sdk/models";
import { ref } from "vue";
import { useRoute } from 'vue-router';
import type { Commit } from "../../sdk";

//
const api = ApiFactory()
const store = useSnapshotStore()

// 
const route = useRoute()
console.log(route)
const key = ref<string>(route.params.key.toString())

//
const autoSave = ref<boolean>(true)
const { source } = storeToRefs(store)

const commits = ref<Commit[]>(
    []
)

const args = ref<Argument[]>(
    []
)

console.log("store source", source.value)

getCommit(source.value.name)

async function getCommit(name: string) {


    await api.apiCommitGet(name).then(
        response => {
            console.log('request', response.data)

            commits.value = response.data.commits.filter(item => item.messages.length > 0)
            console.log('data', commits.value)

            args.value = response.data.args
            console.log('args', args.value)

        }
    ).catch(error => {
        console.log(error)
    })

    console.log(store.source)

    if (commits.value.length <= 0) {
        await api.apiPromptKeyGet(name).then(
            response => {
                console.log('request', response.data)

                commits.value = [
                    {
                        messages: response.data.messages
                    }
                ]
            }
        ).catch(error => {
            console.log(error)
        })
    }
}

async function doCommit(ref) {
    let another = JSON.parse(JSON.stringify(ref))
    another.response = ""

    await saveCommit(key.value, commits.value)

    commits.value.unshift(another)
}


async function doChat(it: Commit) {
    commits.value[0].response = ""

    console.log(it.messages)

    let ms = it.messages?.filter((item: Message) => item.enable)
    ms = JSON.parse(JSON.stringify(ms))
    ms.forEach((item) => {
        item.content = format(item.content, args.value)
    })
    console.log("will chat with messages", ms)

    await api.apiChatPost(ms).then(
        (response) => {
            it.response = response.data
        }
    )

    // await api.api
}

function gotoTest(it: Commit, args: Argument[]) {
    store.sendSource(store.source.name, it.messages, args)
    router.push('/view/debug')
}

async function saveCommit(key: string, data: Commit[],) {
    let req: CommitRequest = {
        commits: data,
        args: []
    }

    await api.apiCommitPost(req, key).then(
        response => {
            console.log("success")
        }
    )
}

async function saveArgument(key: string, args: Argument[]) {
    let req: CommitRequest = {
        commits: [],
        args: args
    }

    await api.apiCommitPost(req, key).then(
        response => {
            console.log("success")
        }
    )
}

async function saveIteration(key: string, data: Commit[], args: Argument[]) {
    let req: CommitRequest = {
        iters: data,
        args: args
    }

    await api.apiCommitPost(req, key).then(
        response => {
            console.log("success")
        }
    )
}

function dropCommit(index: number) {
    console.log(index)
    commits.value.splice(index, 1)
}

function newArg() {
    args.value.push({ key: '', value: '' })
}

function cleanArgs() {
    args.value = args.value.filter(item => item.key != '' && item.value != '')
    console.log(args.value)
}

async function gotoAdvance(iter: Commit) {
    let res = iter.messages.map(item => {
        let copied = { ...item };
        return copied
    })

    let name = key.value

    await api.apiPromptKeyPost(res, name)
        .then(
            response => {
                console.log(response)
            }
        )
        .catch(error => {
            console.error(error)
        })

    RouteHelper.toAdvance(name)
}

</script>

<template>
    <a-row>
        <a-col>
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
        </a-col>
        <a-col>
            <a-button @click="newArg()">
                <template #icon>
                    <PlusOutlined />
                </template>
            </a-button>
            <a-button @click="cleanArgs()">
                <template #icon>
                    <SyncOutlined />
                </template>
            </a-button>
        </a-col>
    </a-row>
    <a-row :gutter="[16, 16]">
        <a-col :span="24" class="gutter-row">
            <a-space direction="horizontal">
                <a-input-group compact>
                    <a-input v-model:value="key" style="width: 100px" />
                    <a-button type="primary" @click="getCommit(key)">Get</a-button>
                    <a-button type="primary" @click="saveIteration(key, commits, args)">Save</a-button>
                </a-input-group>
                <a-checkbox v-model:checked="autoSave">Auto Save</a-checkbox>
                <a-button @click="gotoAdvance(key)">Goto Advance</a-button>
            </a-space>
        </a-col>
    </a-row>
    <a-row :gutter="[16, 16]">
        <a-col :span="8" v-for="(  prompt, index  ) in   commits  " align="center" :key="index">
            <a-card>
                <!--        response-->
                <a-textarea v-model:value="prompt.response" :auto-size="{ minRows: 5, maxRows: 10 }">

                </a-textarea>

                <!--        button-->
                <a-button @click="doChat(prompt)">Request</a-button>
                <a-button @click="gotoTest(prompt, args)">Goto Test</a-button>
                <a-button @click="gotoAdvance(prompt)">Goto Advance</a-button>
                <a-button @click="doCommit(prompt)">Commit</a-button>
                <a-button @click="dropCommit(index)">Drop</a-button>


                <!--        prompt-->
                <PromptInput :messages="prompt.messages" mode="simple" with-copy>

                </PromptInput>

            </a-card>


        </a-col>
    </a-row>
</template>

<style></style>
