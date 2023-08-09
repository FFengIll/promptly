<script setup lang="ts">
import PromptInput from "@/components/PromptInput.vue";
import router from "@/router";
import { ApiFactory } from "@/scripts/api";
import { useSnapshotStore } from "@/stores/snapshot";
import { storeToRefs } from "pinia";
import { ref } from "vue";
import type { Iteration } from "../../sdk";

const api = ApiFactory()
const store = useSnapshotStore()

const autoSave = ref<boolean>(true)
const { source } = storeToRefs(store)
const key = ref(source.value.name)

const data = ref<Iteration[]>(
    [

    ]
)

console.log("store source", source.value)

getIteration(source.value.name)

async function getIteration(name: string) {
    await api.apiIterationGet(name).then(
        response => {
            data.value = response.data.iters.filter(item => item.messages.length > 0)
            console.log(data.value)

        }
    ).catch(error => {
        console.log(error)
    })

    console.log(store.source)

    if (store.source.messages.length > 0) {
        data.value.unshift(store.source)
    }

}

function nextIteration(ref) {
    let another = JSON.parse(JSON.stringify(ref))
    another.response = ""

    data.value.unshift(another)
}


async function doChat(it: Iteration) {
    if (autoSave) {
        await saveIteration(key.value, data.value)
    }

    console.log(it.messages)

    let ms = it.messages?.filter((item) => item.enable)
    console.log("will chat with messages", ms)
    await api.apiChatPost(ms).then(
        (response) => {
            it.response = response.data
        }
    )
}

function gotoDebug(it: Iteration) {
    store.sendSource(it.messages, store.source.name)
    router.push('/view/debug')
}

async function saveIteration(key: string, data: Iteration[]) {
    await api.apiIterationPost(data, key).then(
        response => {
            console.log("success")
        }
    )
}

function dropIteration(index: number) {
    console.log(index)
    data.value.splice(index, 1)
}

async function writeSource(iter: Iteration) {
    let res = iter.messages.map(item => {
        let copied = { ...item };
        return copied
    })

    await api.apiProfileKeyPost(res, store.source.name)
        .then(
            response => {
                console.log(response)
            }
        )
        .catch(error => {
            console.error(error)
        })
}

</script>

<template>
    <a-row :gutter="[16, 16]">
        <a-col :span="24" class="gutter-row">
            <a-space direction="horizontal">
                <a-input-group compact>
                    <a-input v-model:value="key" style="width: 100px" />
                    <a-button type="primary" @click="getIteration(key)">Get</a-button>
                    <a-button type="primary" @click="saveIteration(key, data)">Save</a-button>
                </a-input-group>
                <a-checkbox v-model:checked="autoSave">Auto Save</a-checkbox>
                <a-button @click="router.push(`/view/prompt/${key}`)">Goto Source</a-button>
            </a-space>
        </a-col>
    </a-row>
    <a-row :gutter="[16, 16]">
        <a-col :span="8" v-for="(prompt, index) in data" align="center" :key="index">
            <a-card>
                <!--        response-->
                <a-textarea v-model:value="prompt.response" :auto-size="{ minRows: 5, maxRows: 10 }">

                </a-textarea>

                <!--        button-->
                <a-button @click="doChat(prompt)">Request</a-button>
                <a-button @click="gotoDebug(prompt)">Goto Debug</a-button>
                <a-button @click="writeSource(prompt)">Write Source</a-button>
                <a-button @click="nextIteration(prompt)">Next</a-button>
                <a-button @click="dropIteration(index)">Drop</a-button>


                <!--        prompt-->
                <PromptInput :messages="prompt.messages" mode="simple" with-copy>

                </PromptInput>

            </a-card>


        </a-col>
    </a-row>
</template>

<style></style>
