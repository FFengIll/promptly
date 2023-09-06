<style scoped>
.large-font {
    font-size: 200%
}
</style>

<template>
    <a-card title="Project List">
        <a-space direction="horizontal">
            <a-input v-model:value="newGroup" placeholder="input group" size="large">
            </a-input>
            <a-input v-model:value="newName" placeholder="input name" size="large">
            </a-input>
            <a-button @click="create_profile(newGroup, newName)">
                Create
            </a-button>



            <a-button @click="fetchList(true)">
                <template #icon>
                    <SyncOutlined></SyncOutlined>
                </template>
            </a-button>


        </a-space>

        <a-divider></a-divider>

        <a-card v-for="(values, key) in group" :title="key || '[default]'">
            <a-list :data-source="values.sort()" size="small" :grid="{ gutter: 16, column: 4 }">
                <template #renderItem="{ item }">
                    <a-list-item>
                        <a-typography-link class="large-font" @click="openPrompt(item)">
                            {{ item }}
                        </a-typography-link>
                    </a-list-item>
                </template>
            </a-list>
        </a-card>
    </a-card>
</template>

<script lang="ts" setup>
import router from "@/router";

import { backend } from "@/scripts/backend";
import { useSnapshotStore } from "@/stores/snapshot";
import { SyncOutlined } from "@ant-design/icons-vue";
import { onMounted, ref } from 'vue';


// field
const group = ref({
    "": []
})


const store = useSnapshotStore()

const newName = ref<string>("")
const newGroup = ref<string>("")

// created
onMounted(
    () => {
        fetchList(false)
    }
)


function openPrompt(key: string) {
    router.push(`/view/prompt/${key}`)
}


async function create_profile(group: string, name: string) {
    await backend.apiPromptPost({ group: group }, name)
    fetchList(true)
}


async function fetchList(refresh: boolean) {
    return backend.apiPromptGet(refresh).then(
        response => {
            group.value = response.data['data']
            console.log(response.data)
            return response.data
        }
    ).catch(
        error => {
            console.error(error)
        }
    )
}

</script>