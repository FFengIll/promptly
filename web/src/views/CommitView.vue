<script setup lang="ts">
import PromptInput from "@/components/PromptInput.vue";
import { backend, BackendHelper } from "@/scripts/backend";
import { RouteHelper } from "@/scripts/router";

import type { ArgumentSetting, CommitItem, UpdatePromptBody } from "@/sdk/models";
import { onMounted, ref } from "vue";
import { useRoute } from 'vue-router';

import { HeartOutlined, HeartTwoTone } from "@ant-design/icons-vue";

import ArgumentPanel from '@/components/ArgumentPanel.vue';
import { openNotification } from "@/scripts/notice";
import type { Argument } from "@/sdk/models";
import { useConfigStore } from "@/stores/global-config";
import VueMarkdown from "vue-markdown-render";

//
const store = useConfigStore()

// 
const route = useRoute()
console.log(route)
const key = ref<string>(route.params.key.toString())

//
const autoSave = ref<boolean>(true)

const starOnly = ref<boolean>(false)

const commits = ref<CommitItem[]>(
    []
)
const argSetting = ref<ArgumentSetting>(
    {
        name: "",
        args: []
    }
)
const args = ref<Argument[]>(new Array<Argument>())



onMounted(
    () => {
        backend.apiPromptArgsNameGet(key.value)
            .then(response => {
                argSetting.value = response.data
                console.log('setting', argSetting.value)
            })
        getCommit(key.value)
    }
)


async function getCommit(name: string) {

    await backend.apiCommitsNameGet(name).then(
        response => {
            console.log('request', response.data)

            commits.value = response.data.filter((item: CommitItem) => item.messages.length > 0)
            console.log('data', commits.value)

        }
    ).catch(error => {
        console.log(error)
    })


    if (commits.value.length <= 0) {
        await backend.apiPromptNameGet(name).then(
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




async function saveCommits(key: string, data: CommitItem[]) {

    await backend.apiCommitsNamePut(data, key).then(
        response => {
            console.log("success")
        }
    )
}

function dropCommit(commit: CommitItem, index: number) {
    if (commit.star ?? false) {
        return
    }

    console.log(index)
    commits.value.splice(index, 1)
}


async function replay(commit: CommitItem) {
    commit.response = ""
    let response = await BackendHelper.doChat(commit.options!!, commit.messages, commit.args!!)
    console.log('response', response)
    commit.response = response.data

    console.log(commits.value)
}

async function doChat(commit: CommitItem) {
    commit.response = ""
    await BackendHelper.doChat(commit.options!!, commit.messages, args.value)
        .then((res) => {
            console.log('response', res)
            commit.response = res.data

            console.log(commits.value)
        })
        .catch((err) => {
            openNotification(err.toString(), 'error')
        })
}

async function gotoPrompt(commit: CommitItem) {

    let name = key.value
    let body: UpdatePromptBody = {
        messages: commit.messages,
        args: args.value
    }
    await backend.apiPromptNamePut(body, name)
        .then(
            () => {
                RouteHelper.toPrompt(name)
            }
        )
        .catch((err) => {
            openNotification(err.toString(), 'error')
        })
}

const pagination = {
    onChange: (page: number) => {
        console.log(page);
    },
    pageSize: 3,
};

async function changeStar(commit: CommitItem) {
    let value = !(commit.star ?? false)
    await backend.apiActionStarPost(
        {
            name: key.value,
            md5: commit.md5!!,
            value: value
        }
    ).then(response => {
        commit.star = value
    })
        .catch((err) => {
            openNotification(err.toString(), 'error')
        })
}


function selectArg(key: string, value: string) {
    for (const item of args.value) {
        if (item.key == key) {
            item.value = value
            return
        }
    }
    args.value.push({ key: key, value: value })
}


const simpleModel = ref(true)


</script>

<template>
    <a-row :gutter="[16, 16]">

        <a-col :span="10" class="gutter-row">
            <a-space direction="vertical">
                <a-space direction="horizontal">
                    <a-input-group compact>
                        <a-button type="primary" @click="getCommit(key)">Refresh</a-button>
                        <a-button type="primary" @click="saveCommits(key, commits)">Save</a-button>
                    </a-input-group>
                    <a-checkbox v-model:checked="autoSave">Auto Save</a-checkbox>
                    <a-divider type="vertical"></a-divider>
                    <a-checkbox v-model:checked="starOnly">Star Only</a-checkbox>
                    <a-checkbox v-model:checked="simpleModel">Simple</a-checkbox>
                </a-space>


            </a-space>

        </a-col>

        <a-col :span="10">
            <ArgumentPanel :setting="argSetting" :args="args" @select="selectArg">
            </ArgumentPanel>
        </a-col>

        <!-- <a-col>
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
        </a-col> -->
    </a-row>
    <a-row :gutter="[16, 16]">

    </a-row>
    <a-divider></a-divider>
    <a-row :gutter="[16, 16]">

        <a-col :span="8" v-for="(  commit, index  ) in    commits   " :key="index">
            <a-card v-if="(starOnly && (commit.star ?? false)) || (!starOnly)">

                <div v-if="!simpleModel">
                    <!--        button-->
                    <a-button @click="doChat(commit)">Request</a-button>
                    <a-button @click="replay(commit)">Replay</a-button>
                    <a-button @click="gotoPrompt(commit)">Goto Prompt</a-button>
                    <a-button @click="dropCommit(commit, index)">Drop</a-button>

                    <a-divider></a-divider>
                </div>


                <!-- args -->

                <a-card title="Args">


                    <a-space v-for="( item, index ) in  commit.args " :key="index">
                        <a-typography-text :content="item.key">
                        </a-typography-text>
                        <a-input :value="item.value">
                        </a-input>
                    </a-space>
                </a-card>
                <a-divider></a-divider>

                <!--response-->
                <a-card :title="commit.options!!.model" class="highlight-ant-card-head ">


                    <template #extra>
                        <a-button @click="changeStar(commit)">
                            <template #icon>
                                <HeartTwoTone v-if="commit.star" two-tone-color="#eb2f96" />
                                <HeartOutlined v-else />
                            </template>
                        </a-button>
                    </template>

                    <a-typography-text>Request Timecost: {{ (commit.timecost?? 0) / 1000 }} seconds</a-typography-text>

                    <a-divider></a-divider>

                    <vue-markdown :source="commit.response" :options="{}"
                        style="height: 100px; overflow-y: scroll;"></vue-markdown>
                </a-card>
                <a-divider></a-divider>



                <!-- prompt -->
                <PromptInput :title="'Prompt'" :messages="commit.messages!!" with-copy with-sidebar
                    :with-enable="simpleModel">

                </PromptInput>

            </a-card>
        </a-col>
    </a-row>
</template>

<style>
.highlight-ant-card-head {
    background-color: #2feb55b6
}

.ant-card-head {
    background-color: #2feb55
}
</style>
@/stores/global-config