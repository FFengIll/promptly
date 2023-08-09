<script setup lang="ts">
import PromptInput from "@/components/PromptInput.vue";
import router from "@/router";
import { ApiFactory } from "@/scripts/api";
import { format } from "@/scripts/template";
import { useSnapshotStore } from "@/stores/snapshot";
import { PlusOutlined, SyncOutlined } from "@ant-design/icons-vue";
import { storeToRefs } from "pinia";
import type { ArgItem, IterationRequest, Message } from "sdk/models";
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

const args = ref<ArgItem[]>(
    [

    ]
)

console.log("store source", source.value)

getIteration(source.value.name)

async function getIteration(name: string) {
    await api.apiIterationGet(name).then(
        response => {
            console.log('request', response.data)

            data.value = response.data.iters.filter(item => item.messages.length > 0)
            console.log('data', data.value)

            args.value = response.data.args
            console.log('args', args.value)

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
    data.value[0].response = ""

    if (autoSave) {
        await saveIteration(key.value, data.value, args.value)
    }

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

function gotoDebug(it: Iteration) {
    store.sendSource(it.messages, store.source.name)
    router.push('/view/debug')
}

async function saveIteration(key: string, data: Iteration[], args: ArgItem[]) {
    let req: IterationRequest = {
        iters: data,
        args: args
    }

    await api.apiIterationPost(req, key).then(
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

function clean() {
    args.value = args.value.filter(item => item.key != '' && item.value != '')
    console.log(args.value)
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
            <a-button @click="() => {
                args.push({ key: '', value: '' })
            }">
                <template #icon>
                    <PlusOutlined />
                </template>
            </a-button>
            <a-button @click="clean()">
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
                    <a-button type="primary" @click="getIteration(key)">Get</a-button>
                    <a-button type="primary" @click="saveIteration(key, data, args)">Save</a-button>
                </a-input-group>
                <a-checkbox v-model:checked="autoSave">Auto Save</a-checkbox>
                <a-button @click="router.push(`/view/prompt/${key}`)">Goto Source</a-button>
            </a-space>
        </a-col>
    </a-row>
    <a-row :gutter="[16, 16]">
        <a-col :span="8" v-for="(  prompt, index  ) in   data  " align="center" :key="index">
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
