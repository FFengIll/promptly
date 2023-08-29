<script setup lang="ts">
import PromptInput from "@/components/PromptInput.vue";
import router from "@/router";
import { BackendHelper, backend } from "@/scripts/backend";
import { RouteHelper } from "@/scripts/router";
import { useSnapshotStore } from "@/stores/snapshot";
import { storeToRefs } from "pinia";
import type { ArgumentSetting, CommitItem } from "sdk/models";
import { onMounted, ref } from "vue";
import { useRoute } from 'vue-router';

import CaseInput from '@/components/CaseInput.vue';
import { ArgumentHelper } from "@/scripts/argument";
import type { Argument } from "../../sdk/models";

//
const store = useSnapshotStore()

// 
const route = useRoute()
console.log(route)
const key = ref<string>(route.params.key.toString())

//
const autoSave = ref<boolean>(true)
const { source } = storeToRefs(store)

const commits = ref<CommitItem[]>(
    []
)
const argSetting = ref<ArgumentSetting>(
    {
        name: "",
        args: {}
    }
)
const args = ref<Map<string, string>>(new Map())


console.log("store source", source.value)

onMounted(
    () => {
        backend.apiPromptArgsNameGet(key.value)
            .then(response => {
                argSetting.value = response.data

                console.log('setting', argSetting.value)
                let tmp = argSetting.value.args
                for (let key in tmp) {
                    if (tmp.hasOwnProperty(key)) {
                        const values = tmp[key];
                        console.log(tmp, key, values)
                        args.value.set(key, values[0])
                    }
                }

                console.log("arguments", args.value)

            })
        getCommit(source.value.name)
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

    console.log(store.source)

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


function gotoTest(it: CommitItem, args: Argument[]) {
    store.sendSource(store.source.name, it.messages!!, args)
    router.push('/view/debug')
}


async function saveCommits(key: string, data: CommitItem[]) {

    await backend.apiCommitsNamePut(data, key).then(
        response => {
            console.log("success")
        }
    )
}

function dropCommit(index: number) {
    console.log(index)
    commits.value.splice(index, 1)
}


async function replay(key: string, commit: CommitItem) {
    commit.response = ""
    let response = await BackendHelper.doChat("", commit.messages!!, commit.args!!)
    console.log('response', response)
    commit.response = response.data

    console.log(commits.value)
}

async function doChat(key: string, commit: CommitItem) {
    commit.response = ""
    let response = await BackendHelper.doChat("", commit.messages!!, ArgumentHelper.toArgumentList(args.value))
    console.log('response', response)
    commit.response = response.data

    console.log(commits.value)
}

async function gotoPrompt(commit: CommitItem) {

    let name = key.value

    await backend.apiPromptNamePut(commit.messages!!, name)

    console.log("args", args.value)

    let items = ArgumentHelper.toArgumentList(args.value)

    store.sendSource(name, commit.messages!!, items)

    RouteHelper.toPrompt(name)
}

const pagination = {
    onChange: (page: number) => {
        console.log(page);
    },
    pageSize: 3,
};

</script>

<template>
    <a-row :gutter="[16, 16]">
        <a-col :span="10">
            <CaseInput :setting="argSetting" :args="args" @select="(key, value) => { args.set(key, value) }">
            </CaseInput>
        </a-col>

        <a-col :span="10" class="gutter-row">
            <a-space direction="horizontal">
                <a-input-group compact>
                    <a-input v-model:value="key" style="width: 200px" />
                    <a-button type="primary" @click="getCommit(key)">Get</a-button>
                    <a-button type="primary" @click="saveCommits(key, commits)">Save</a-button>
                </a-input-group>
                <a-checkbox v-model:checked="autoSave">Auto Save</a-checkbox>
            </a-space>
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

        <a-col :span="8" v-for="(  commit, index  ) in    commits   " align="center" :key="index">
            <a-card>
                <!--        response-->
                <a-card :title="commit.model || 'GPT-3.5'">

                    <template #extra>
                        <a-typography-text>

                        </a-typography-text>
                    </template>
                    <a-textarea v-model:value="commit.response" :auto-size="{ minRows: 6, maxRows: 6 }">

                    </a-textarea>
                </a-card>
                <a-divider></a-divider>


                <!--        button-->
                <a-button @click="doChat(key, commit)">Request</a-button>
                <a-button @click="replay(key, commit)">Replay</a-button>
                <a-button @click="gotoTest(commit, args)">Goto Test</a-button>
                <a-button @click="gotoPrompt(commit)">Goto Prompt</a-button>
                <a-button @click="dropCommit(index)">Drop</a-button>

                <a-divider></a-divider>

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



                <!-- prompt -->
                <PromptInput :title="'Prompt'" :messages="commit.messages!!" with-copy with-sidebar>

                </PromptInput>

            </a-card>
        </a-col>
    </a-row>
</template>

<style></style>
