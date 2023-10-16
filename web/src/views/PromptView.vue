<style>
.scroll-short {
    height: 200px;
    /* 设置组件容器的固定高度 */
    overflow: auto;
    /* 设置溢出部分自动滚动 */
}
</style>

<template>
    <div>
        <a-space align="center">
            <a-typography-title>{{ key }}</a-typography-title>
            <a-button @click="reload">
                <template #icon>
                    <SyncOutlined />
                </template>
            </a-button>
        </a-space>
        <a-row :gutter='6'>
            <a-col class="gutter-row" :span="12">

                <!-- <a-collapse>
                    <a-collapse-panel header="History">
                        <a-space direction="horizontal" align="baseline" v-for="h in prompt.history">
                            <a-button @click="copy(h)">
                                <template #icon>
                                    <CopyOutlined />
                                </template>
                            </a-button>
                            <p>{{ h }}</p>



                        </a-space>
                    </a-collapse-panel>
                </a-collapse> -->


                <a-card title="Prompt">
                    <template #extra>

                        <!-- <template #icon>
                                <SyncOutlined />
                            </template> -->
                        <a-button
                            @click="() => { copy(JSON.stringify({ name: key, prompt: prompt.messages.filter((item: Message) => { return item.enable }) }, null, 2)) }">
                            Copy To JSON
                        </a-button>
                        <a-button @click="() => { prompt.messages.forEach((item) => item.enable = false) }">Disable
                            All
                        </a-button>
                        <a-button @click="() => { prompt.messages.forEach((item) => item.enable = true) }">Enable
                            All
                        </a-button>
                    </template>


                    <a-row justify="space-around">
                        <PromptInput :messages="prompt.messages" with-copy with-control
                            @order-up="index => order(index, -1)" @order-down="index => order(index, 1)"
                            @remove="index => deletePrompt(index)" @add="index => addPrompt(index, 'user', '')">
                        </PromptInput>
                    </a-row>

                    <a-divider>
                        <a-space>
                            <a-button @click="() => prompt.messages.push({ role: 'system', enable: true, content: '' })">
                                <template #icon>
                                    <PlusOutlined />
                                </template>
                            </a-button>
                        </a-space>

                    </a-divider>

                </a-card>

            </a-col>


            <a-col class="gutter-row" :span="12">


                <a-card title="Preference">

                    <a-list item-layout="horizontal">
                        <a-list-item>
                            Model
                            <ModelSelect :model="model" :defaultModel="(() => { return prompt.defaultModel })()"
                                v-on:select="(value) => { model = value }"
                                v-on:default="(value) => updateDefaultModel(value)" style="width: 200px">
                            </ModelSelect>
                            <a-button @click="fetchArgument(key)">
                                <template #icon>
                                    <SyncOutlined />
                                </template>
                            </a-button>
                        </a-list-item>

                        <a-space>
                            <ArgumentPanel :setting="store.globalArgs" :args="args" @select=selectArg>
                            </ArgumentPanel>
                        </a-space>

                        <a-list-item>
                            Use Embed
                            <a-switch v-model:checked="withEmbed" @change="(e) => {
                                if (e.target.checked) {
                                    let idx = prompt.plugins!!.findIndex(it => { return it == 'embed' })
                                    if (idx >= 0) {
                                        return
                                    }
                                    prompt.plugins!!.push('embed')
                                }
                            }"></a-switch>

                        </a-list-item>

                        <a-list-item>
                            Temperature:
                            <a-input-number style="width: 200px" :min="0" :max="2" :step="0.1"
                                v-model:value="options.temperature" placeholder="key">
                            </a-input-number>
                        </a-list-item>
                        <a-list-item>
                            Top_P:
                            <a-input-number style="width: 200px" :min="0" :max="2" :step="0.1" v-model:value="options.topP"
                                placeholder="key">
                            </a-input-number>
                        </a-list-item>
                    </a-list>

                </a-card>


                <a-card title="Message Replace">

                    <template #extra>
                        <a-button @click="fetchArgument(key)">
                            <template #icon>
                                <SyncOutlined />
                            </template>
                        </a-button>
                    </template>



                    <ArgumentPanel :setting="argSetting" :args="args" @select=selectArg>
                        <template #extra>
                            <a-space direction="horizontal">
                                <a-select ref="select" v-model:value="argKey" style="width: 120px" show-search>
                                    <a-select-option v-for="k in args" :key="k.key">{{ k.key }}</a-select-option>
                                </a-select>

                                <a-input v-model:value="argKey" placeholder="key">
                                </a-input>

                                <a-input v-model:value="argValue" placeholder="value">
                                </a-input>

                                <a-button @click="newArg()">
                                    <template #icon>
                                        <PlusOutlined />
                                    </template>
                                    New
                                </a-button>
                            </a-space>
                            <a-divider></a-divider>

                        </template>
                    </ArgumentPanel>


                </a-card>


                <a-card title="Operation">

                    <a-space direction="horizontal">
                        <a-button @click="chat">Request</a-button>
                        <a-button @click="doCommit">Commit</a-button>
                    </a-space>
                    <!--<a-space direction="horizontal">-->
                    <!--<a-button @click="gotoTesting">Goto Testing</a-button>-->
                    <!--<a-button @click="gotoCommit">Goto Commit</a-button>-->
                    <!--</a-space>-->

                </a-card>

                <a-divider></a-divider>


                <a-card title="Response">
                    <template #extra>
                        <a-space direction="horizontal">
                            <a-button>Good</a-button>
                            <a-button>Bad</a-button>
                            <a-button @click="() => copy(response)">Copy</a-button>

                        </a-space>

                        <a-space>
                            <a-button @click="responseToPrompt">Append to prompt</a-button>
                        </a-space>

                    </template>
                    <a-skeleton :loading="loading" active avatar>
                        <div>
                            <a-collapse>

                                <a-collapse-panel header="Prompt Preview">
                                    <PromptCard :messages="prompt.messages.filter((i) => i.enable)"></PromptCard>
                                </a-collapse-panel>
                            </a-collapse>

                            <a-divider></a-divider>

                            <a-tabs v-model:activeKey="responseMode">
                                <a-tab-pane key="1" tab="Markown"> <vue-markdown :source="response"
                                        :options="{}"></vue-markdown></a-tab-pane>
                                <a-tab-pane key="2" tab="Text" force-render>
                                    <a-textarea v-model:value="response" :auto-size="{ maxRows: 16 }">
                                    </a-textarea>
                                </a-tab-pane>
                            </a-tabs>



                        </div>
                    </a-skeleton>

                </a-card>

            </a-col>
        </a-row>
    </div>
</template>

<script lang="ts" setup>
import { PlusOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { useClipboard } from '@vueuse/core';
import { onMounted, ref } from 'vue';

import { useRoute } from 'vue-router';

import ArgumentPanel from '@/components/ArgumentPanel.vue';
import ModelSelect from '@/components/ModelSelect.vue';
import PromptInput from "@/components/PromptInput.vue";
import { backend, BackendHelper } from "@/scripts/backend";
import { openNotification } from "@/scripts/notice";
import { RouteHelper } from '@/scripts/router';
import { useConfigStore } from "@/stores/global-config";
import type {
    ArgRequest,
    Argument,
    ArgumentSetting,
    LLMOption,
    Message,
    NewCommitBody,
    Prompt,
    UpdatePromptBody
} from "src/sdk";
import VueMarkdown from 'vue-markdown-render';
import PromptCard from '../components/PromptCard.vue';

const store = useConfigStore()
// use
const r = useRoute()
const { text, copy, copied, isSupported } = useClipboard({})

const key = r.params.key.toString()

const responseMode = ref()

// props
const props = defineProps<{}>()

// field
const loading = ref(false)
const model = ref<string>("")



const withEmbed = ref<boolean>(false)

const argValue = ref<string>("")
const argKey = ref<string>("")
const response = ref(<string>"test")
const argSetting = ref<ArgumentSetting>(
    {
        name: "",
        args: []
    }
)
const args = ref<Argument[]>([])
const prompt = ref<Prompt>(<Prompt>{})
const options = ref<LLMOption>(<LLMOption>{})

// created
onMounted(
    () => {
        fetchPrompt(key)
    }
)



function updateDefaultModel(model: string) {
    let body: UpdatePromptBody = <UpdatePromptBody>({ defaultModel: model })
    backend.apiPromptNamePut(body, prompt.value.name)
        .then(() => {
            console.log(model)
            prompt.value.defaultModel = model
        })
        .catch(err => {
            openNotification(err, 'error')
        })
}


function selectArg(key: string, value: string) {
    for (const item of args.value) {
        if (item.key == key) {
            item.value = value
            return
        }
    }
    args.value.push({ key: key, value: value, candidates: [] })
}

async function newArg() {
    let body: ArgRequest = {
        key: argKey.value,
        value: argValue.value
    }

    if (argKey.value == "" || argValue.value == "") {
        return
    }

    await backend.apiPromptArgsNamePut(body, key)
        .then(response => {
            selectArg(argKey.value, argValue.value)
        })
        .catch(err => {
            openNotification(err.toString(), "error")
        })

    await fetchArgument(key)

}


// methods
function responseToPrompt() {
    addPrompt(prompt.value.messages.length, 'assistant', response.value)
}

function deletePrompt(index: number) {
    let ms = prompt.value.messages

    ms.splice(index, 1); // 删除指定索引的元素
}

function gotoCommit() {
    console.log(key)

    RouteHelper.toCommit(key)
}

async function gotoTesting() {
    let body: UpdatePromptBody = {
        messages: prompt.value.messages!!,
        model: model.value,
        args: args.value,
    }

    await backend.apiPromptNamePut(body, key).catch((err) => {
        console.log(err)
        openNotification(err.toString(), "error")
    })

    RouteHelper.toTesting(key)
}


async function doCommit() {
    let body: NewCommitBody = {
        name: key,
        commit: {
            messages: prompt.value.messages,
            response: response.value,
            args: args.value,
            model: model.value,
        },
    }
    backend.apiCommitPost(body)
        .then(() => {

        })
        .catch(err => {
            openNotification(err.toString(), "error")
        })
}

function addPrompt(index: number, role: string, content: string) {
    let m: Message = { content: content, role: role, enable: true, }
    let ms = prompt.value.messages
    while (1) {
        if (ms[index - 1].role == 'system') {
            index -= 1
        } else {
            break
        }
    }

    prompt.value.messages.splice(index, 0, m)

    console.log(prompt.value.messages)
}

function order(index: number, delta: number) {
    let another = index + delta
    console.log('index', index, another)
    if (another < 0 || another >= prompt.value.messages.length) {
        return
    }
    let current = prompt.value.messages[index]
    let next = prompt.value.messages[index + delta]

    prompt.value.messages[index] = next
    prompt.value.messages[index + delta] = current

    console.log(prompt.value.messages)
}


async function fetchArgument(name: string) {
    await backend.apiPromptArgsNameGet(name)
        .then(response => {
            argSetting.value = response.data

            console.log('response', argSetting.value)

        })
        .catch(err => {
            openNotification(err.toString(), "error")
        })

}

async function fetchPrompt(name: string) {
    await fetchArgument(name)

    await backend.apiPromptNameGet(name)
        .then(response => {
            console.log(response.data)
            prompt.value = response.data;

            args.value = prompt.value.args!!
            console.log(args.value)

            options.value = prompt.value.options!!
            console.log(options.value)

            model.value = options.value.model!!
            console.log(model.value)


            let idx = prompt.value.plugins?.findIndex(it => { return it == 'embed' })
            console.info(idx)
            if (idx !== undefined && idx >= 0) {
                withEmbed.value = true
            }
        })
        .catch(err => {
            openNotification(err.toString(), "error")
        })
}

function reload() {
    fetchPrompt(key);
}


async function chat() {
    if (withEmbed.value) {
        await chatWithRAG()
    } else {
        await chatWithPrompt()
    }
}

async function chatWithRAG() {
    try {
        let messages = prompt.value.messages

        console.log(messages)

        // assert(messages[0].role, 'system',"")
        // assert(messages[-1].role, 'user',"")

        // // replace first system prompt
        // await backend.apiActionRetrievePost({ name: key, message: messages[-1].content })
        //     .then((res) => {
        //         messages[0].content = res.data
        //     })


        let body: UpdatePromptBody = {
            messages: prompt.value.messages!!,
            model: model.value,
            args: args.value,
            plugins: [
                'embed'
            ]
        }
        await backend.apiPromptNamePut(body, key).catch((err) => {
            console.log(err)
            openNotification(err.toString(), "error")
        })

        loading.value = true
        response.value = ''

        await backend.apiActionRetrieveGeneratePost(
            {
                name: key,
                messages: messages?.filter((item: Message) => item.enable)
            },
        )
            .then(
                (res) => {
                    response.value = res.data;
                }
            )
    } catch (err) {
        openNotification(err.toString(), "error")
    } finally {
        loading.value = false
    }
}

async function chatWithPrompt() {
    console.log("model", model.value)
    console.log(prompt.value.messages)
    let body: UpdatePromptBody = {
        messages: prompt.value.messages!!,
        args: args.value,
        options: options.value,
    }
    await backend.apiPromptNamePut(body, key).catch((err) => {
        console.log(err)
        openNotification(err.toString(), "error")
    })

    try {
        loading.value = true
        response.value = ''
        await BackendHelper.doChat(options.value, prompt.value.messages, args.value)
            .then(
                (res) => {
                    response.value = res.data;
                }
            )

    } catch (err) {
        console.log(err)
        openNotification(err.toString(), "error")
    } finally {
        loading.value = false
    }
}
</script>
@/stores/global-config