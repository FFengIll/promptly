

<template>
    <a-card title="Click to Open Prompt Detail">
        <a-list v-for="item in keys" :key="item" size="small">
            <a-list-item>
                <a v-bind:href="generateHref(item)">{{ item }}</a>
            </a-list-item>
        </a-list>

    </a-card>
</template>
  
<script lang="ts" setup>
import router from "@/router";
import { DefaultApiFactory } from "../../sdk/apis/default-api";

import { ref } from 'vue'

const keys = ref([
    '1', '2', '3'
])

const api = DefaultApiFactory(undefined, "http://localhost:8000")

fetchList()



function generateHref(key: string) {
    // 处理按钮点击事件
    console.log("Button clicked for item with ID:", key);

    // TODO: jump to another page /prompt/id
    // router.push('')

    return '/view/prompt/' + key
}

async function fetchList() {
    return api.listProfileApiProfileGet().then(
        response => {
            console.log(response.data)
            keys.value = response.data.keys
            return response.data
        }
    ).catch(
        error => {
            console.error(error)
        }
    )
}

</script>