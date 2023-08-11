<style scoped>
.large-font {
    font-size: 200%
}
</style>

<template>
    <a-card title="Project List">
        <a-space direction="horizontal">


            <a-input-search v-model:value="store.source.name" placeholder="input search text" size="large"
                @search="create_profile">
                <template #enterButton>
                    <a-button>Create</a-button>
                </template>
            </a-input-search>

            <a-button @click="fetchList(true)">
                Refresh
            </a-button>


        </a-space>

        <a-divider></a-divider>

        <a-list :data-source="keys" size="small" :grid="{ gutter: 16, column: 4 }">
            <template #renderItem="{ item }">
                <a-list-item>
                    <a-typography-link class="large-font" @click="openPrompt(item)">
                        {{ item }}
                    </a-typography-link>
                </a-list-item>
            </template>
        </a-list>
    </a-card>
</template>

<script lang="ts" setup>
import router from "@/router";

import { ApiFactory } from "@/scripts/api";
import { useSnapshotStore } from "@/stores/snapshot";
import { ref } from 'vue';

const api = ApiFactory()

// field
const keys = ref([
    '1', '2', '3'
])


const store = useSnapshotStore()

// created
fetchList(false)

function openPrompt(key: string) {
    router.push(`/view/prompt/${key}`)
}


async function create_profile(name: string) {
    await api.apiPromptKeyPut(name)
    fetchList(true)
}


async function fetchList(refresh: boolean) {
    return api.apiPromptGet(refresh).then(
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