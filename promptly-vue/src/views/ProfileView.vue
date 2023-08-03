<template>
    <a-space direction="horizontal">
        <a-button @click="refresh">
            Refresh
        </a-button>


        <a-input-search
            v-model:value="key"
            placeholder="input search text"
            size="large"
            @search="create_profile"
        >
            <template #enterButton>
                <a-button>Create</a-button>
            </template>
        </a-input-search>

    </a-space>

    <a-card title="Click to Open Prompt Detail">
        <a-list v-for="item in keys" :key="item" size="small">
            <a-list-item>
                <a v-bind:href="generateHref(item)">{{ item }}</a>
            </a-list-item>
        </a-list>

    </a-card>
</template>

<script lang="ts" setup>
import {DefaultApiFactory} from "../../sdk/apis/default-api";

import {ref} from 'vue';

const api = DefaultApiFactory(undefined, "http://localhost:8000")

// field
const keys = ref([
    '1', '2', '3'
])

const key = ref<string>("")

// created
fetchList()

function refresh() {
    api.apiCaseRefreshGet()
    fetchList()
}

function create_profile(name: string) {
    api.apiProfileKeyPut(name)
    refresh()
}

function generateHref(key: string) {
    // 处理按钮点击事件
    console.log("Button clicked for item with ID:", key);

    // TODO: jump to another page /prompt/id
    // router.push('')

    return '/view/prompt/' + key
}

async function fetchList() {
    return api.apiProfileGet().then(
        response => {
            console.log(response.data)
            keys.value = response.data.keys
            keys.value.sort()
            return response.data
        }
    ).catch(
        error => {
            console.error(error)
        }
    )
}

</script>