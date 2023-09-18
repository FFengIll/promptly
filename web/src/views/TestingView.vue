<style scoped>
.tooltip {
    width: 300px;
}
</style>

<template>
    <div>
        <!-- prompt view -->
        <a-row :gutter="12">
            <a-col :span="12">
                <a-card :title="`Prompt Snapshot [ name = ${prompt.name} ]`">

                    <ArgumentPanel :setting="argSetting" :mask="caseKey" :args="args" @select="selectArg">
                    </ArgumentPanel>


                    <a-divider></a-divider>

                    <ModelSelect :model="model" v-on:select="(value) => { model = value }" style="width: 200px">

                    </ModelSelect>

                    <a-divider></a-divider>


                    <a-space direction="horizontal">
                        <!-- repeat -->
                        <a-input-group>
                            <a-space align="middle">
                                <a-typography-text>Repeat</a-typography-text>
                                <a-input-number id="inputNumber" v-model:value="repeat" :min="1" :max="10">
                                    <template #upIcon>
                                        <ArrowUpOutlined />
                                    </template>
                                    <template #downIcon>
                                        <ArrowDownOutlined />
                                    </template>
                                </a-input-number>
                            </a-space>
                        </a-input-group>

                        <!-- click to run -->
                        <a-button type="primary" @click="runTest(repeat)">Run Test</a-button>
                    </a-space>

                    <a-divider></a-divider>


                    <a-space direction="vertical" :style="{ width: '100%' }">
                        <!-- <PromptCard :messages="prompt.messages.filter(item => item.enable)"></PromptCard> -->
                        <div v-for="(item, index) in prompt.messages" :key="index">
                            <div v-if="item.enable">
                                <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
                                <span>
                                    <a-textarea v-model:value="item.content" :auto-size="{ maxRows: 3 }">
                                    </a-textarea>
                                </span>
                            </div>
                        </div>
                    </a-space>
                </a-card>
            </a-col>
            <a-col :span="12">

                <!-- show dataset info -->
                <a-card title="Case List">

                    <a-divider></a-divider>
                    <!-- case select -->
                    Select Case to Debug:&nbsp;&nbsp;
                    <a-select style="width:300px" @change="getCase">
                        <a-select-option v-for="item in caseList" :key="item.name">
                            {{ item.name }}
                            <a-divider type="vertical" />
                            {{ item.description }}
                        </a-select-option>
                    </a-select>

                    <a-button @click="listCase(true)">Refresh</a-button>

                    <a-divider />


                    <!-- case description -->
                    Case Description:&nbsp;&nbsp;
                    <span>{{ config.description }}</span>

                    <a-divider />


                    <a-space direction="horizontal">
                        <a-select style="width:300px" @change="(value: string) => { caseKey = value }">
                            <a-select-option v-for="key in args.keys()" :key="key">
                                {{ key }}
                            </a-select-option>
                        </a-select>

                        <a-button type="primary" @click="runTestWithCase">Run With Case</a-button>
                    </a-space>

                    <a-divider />


                    <div v-for="(item, index) in config.data" :key="index">
                        <a-list-item>
                            <a-button @click="debugOne(item)">Request</a-button>
                            <a-button @click="sendBack(item)">Send Back</a-button>
                            <a-button @click="gotoSource(prompt.name)"> Go To Source</a-button>
                            <a-typography-text :ellipsis="true" :copyable="true" :content="item"></a-typography-text>
                            <a-divider />
                        </a-list-item>

                    </div>


                </a-card>


            </a-col>
        </a-row>
        <a-row>
            <a-col :span="24">

                <!-- show result -->
                <a-table :dataSource="result" :columns="columns" :rowKey="(record: any) => record.id">
                    <template #bodyCell="{ column, record }">
                        <template v-if="column.key === 'action'">
                            <span>
                                <a-button @click="debugOne(record.source)">Request</a-button>
                                <a-button @click="sendBack(record.source)">Send Back</a-button>
                                <a-button @click="gotoSource(prompt.name)"> Go To Source</a-button>

                            </span>
                        </template>
                        <template v-else-if="column.key === 'source'">
                            <a-tooltip placement="topLeft" :overlay-inner-style="{ width: '500px' }">
                                <template #title>
                                    {{ JSON.stringify(record.source) }}
                                </template>
                                {{ JSON.stringify(record.source) }}

                            </a-tooltip>
                        </template>
                        <template v-else-if="column.key === 'target'">
                            <a-tooltip placement="topLeft" :overlay-inner-style="{ width: '500px' }">
                                <template #title>
                                    {{ JSON.stringify(record.target) }}
                                </template>
                                {{ JSON.stringify(record.target) }}
                            </a-tooltip>

                        </template>

                    </template>

                </a-table>
            </a-col>
        </a-row>
    </div>
</template>
<script lang="ts" setup>
import { onMounted, ref } from 'vue';

import type { TableColumnType } from 'ant-design-vue';



import ArgumentPanel from '@/components/ArgumentPanel.vue';

import ModelSelect from "@/components/ModelSelect.vue";
import router from "@/router";
import { backend } from '@/scripts/backend';
import { openNotification } from '@/scripts/notice';
import { useConfigStore } from '@/stores/global-config';
import type { Argument, ArgumentSetting, Message, Prompt, TestingRequestBody, UpdatePromptBody } from 'sdk/models';
import { useRoute } from 'vue-router';
const r = useRoute()


const key = r.params.key.toString()

const store = useConfigStore()

const repeat = ref<number>(1);

const model = ref<string>("")

const argSetting = ref<ArgumentSetting>(
    {
        name: "",
        args: []
    }
)
const args = ref<Argument[]>(new Array())

const prompt = ref<Prompt>(
    <Prompt>{
        "name": "",
        "history": [],
        "messages": <Message[]>[
            { role: "角色1", content: "内容1", enable: true },
            // 其他数据项
        ],
        model: "",
        plugins: [""]
    }
)

interface ResultItem {
    id: number,
    source: string,
    target: string
}

const result = ref(
    <ResultItem[]>[]
)

const config = ref({
    id: "",
    data: [],
    description: "description"

})

const caseList = ref(
    [
        { id: 1, name: "test", description: "test", data: [1, 2, 3, 4] },
    ],
)

onMounted(
    async () => {
        listCase(false)

        await backend.apiPromptNameGet(key)
            .then(response => {
                console.log(response.data)
                prompt.value = response.data;
            })


        await backend.apiPromptArgsNameGet(key)
            .then(response => {
                argSetting.value = response.data

                console.log('response', argSetting.value)

            }).catch(error => {
                console.log(error)
            })
    }
)


function toTestcase() {
    return config.value.data.map((item, index) => {
        return { id: index, source: item, target: "" }
    })
}

const caseKey = ref("")



const columns: TableColumnType[] = [
    {
        title: 'id',
        dataIndex: 'id',
        key: 'id',
    },
    {
        title: 'source',
        dataIndex: 'source',
        key: 'source',
        ellipsis: { showTitle: false },
    },
    {
        title: 'target',
        dataIndex: 'target',
        key: 'target',
    },
    {
        title: 'action',
        dataIndex: 'action',
        key: 'action',
    },
]

interface Params {
    id: number,
    source: string
}

function sendBack(source: string) {

    let messages = prompt.value.messages.map((item: any) => {
        let copied = { ...item };
        copied.content = copied.content.replace('{{}}', source)
        console.log(copied)
        return copied
    })

    let body: UpdatePromptBody = {
        messages: messages
    }

    backend.apiPromptNamePut(body, prompt.value.name)
        .then(
            response => {
                console.log(response)
            }
        )
        .catch(error => {
            console.error(error)
        })
}

function gotoSource(source: string) {
    router.push(`/view/prompt/${source}`)
}

async function debugOne(source: string) {

    var res = prompt.value.messages.filter((item: { enable: boolean; }) => {
        return item.enable == true
    })


    let body: TestingRequestBody = {
        messages: res,
        argKey: caseKey.value,
        sources: [source],
        args: args.value
    }

    await backend.apiActionTestingPost(body, repeat.value)
        .then(
            (response) => {
                let element = response.data[0]
                result.value.splice(0, 0, element)
            }
        )
        .catch(err => {
            openNotification(err, 'error')
        })
}

async function doRunTest(body: TestingRequestBody) {
    await backend.apiActionTestingPost(body, 1)
        .then(
            (response) => {
                result.value.splice(0, 0, ...response.data)
            }
        )
        .catch(err => {
            openNotification(err, 'error')
        })
}

async function runTestWithCase() {
    var res = prompt.value.messages.map((item: any) => item)

    config.value.data.forEach(source => {
        let body: TestingRequestBody = {
            messages: res,
            argKey: caseKey.value,
            sources: [source],
            args: args.value,
            model: model.value,
        }

        doRunTest(body)
    })

}


async function runTest(repeat: number) {
    var res = prompt.value.messages.map((item: any) => item)

    let body: TestingRequestBody = {
        messages: res,
        argKey: caseKey.value,
        sources: [''],
        args: (args.value),
        model: model.value,
    }

    for (let i = 0; i < repeat; i++) {
        doRunTest(body)
    }
}

async function listCase(refresh: boolean) {
    await backend.apiCaseGet(refresh).then(
        (response) => {
            caseList.value = response.data
            console.log(caseList.value)
        }
    )
        .catch(err => {
            openNotification(err, 'error')
        })
}

async function getCase(id: string) {
    await backend.apiCaseKeyGet(id).then((response) => {
        console.log(response.data)
        config.value = response.data
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
    args.value.push({ key: key, value: value })
}

</script>