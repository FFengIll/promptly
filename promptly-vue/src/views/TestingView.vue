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
                <a-card :title="`Prompt Snapshot [ name = ${store.source.name} ]`">



                    <CaseInput :setting="argSetting" :args="args" @select="(key, value) => { args.set(key, value) }">
                    </CaseInput>
                    <a-divider></a-divider>
                    <a-space direction="vertical" :style="{ width: '100%' }">
                        <div v-for="item in store.source.messages" :key="item.id">
                            <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
                            <span>
                                <a-textarea v-model:value="item.content" :auto-size="{ maxRows: 3 }">
                                </a-textarea>
                            </span>
                        </div>
                    </a-space>
                </a-card>
            </a-col>
            <a-col :span="12">

                <!-- show dataset info -->
                <a-card title="Case List">
                    <a-checkbox v-model:checked="useCase">Use Case</a-checkbox>

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


                    <a-select style="width:300px" @change="(value: string) => { caseKey = value }">
                        <a-select-option v-for="key in args.keys()" :key="key">
                            {{ key }}
                        </a-select-option>
                    </a-select>


                    <a-divider />

                    <div v-for="(item, index) in config.data" :key="index">
                        <a-list-item>
                            <a-typography-text> {{ item }}</a-typography-text>
                            <a-button @click="debugOne(item)">Request</a-button>
                            <a-button @click="sendBack(item)">Send Back</a-button>
                            <a-button @click="gotoSource(store.source.name)"> Go To Source</a-button>
                        </a-list-item>

                    </div>



                </a-card>

                <a-card title="Operation">
                    <a-space align="middle">

                        <!-- loop -->
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
                        <a-button type="primary" @click="debugAll">Run Test</a-button>
                        <a-button @click="gotoSource(store.source.name)"> Go To Source</a-button>
                    </a-space>
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
                                <a-button @click="gotoSource(store.source.name)"> Go To Source</a-button>

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

import { useSnapshotStore } from "@/stores/snapshot";

import CaseInput from '@/components/CaseInput.vue';

import router from "@/router";
import { ArgumentHelper } from '@/scripts/argument';
import type { ArgumentSetting, TestingRequestBody } from 'sdk/models';
import { DefaultApiFactory } from '../../sdk/apis/default-api';


const store = useSnapshotStore()

const api = DefaultApiFactory(undefined, "http://localhost:8000")

const repeat = ref<number>(1);

const useCase = ref<boolean>(false)

const argSetting = ref<ArgumentSetting>(
    {
        name: "",
        args: {}
    }
)
const args = ref<Map<string, string>>(new Map())

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
    data: [

    ],
    description: "description"

})

const caseList = ref(
    [
        { id: 1, name: "test", description: "test", data: [1, 2, 3, 4] },
    ],
)


onMounted(
    () => {
        listCase(false)

        let key = store.source.name
        api.apiPromptArgsGet(key)
            .then(response => {
                argSetting.value = response.data

                console.log('response', argSetting.value)

                let tmp = argSetting.value.args
                for (let key in tmp) {
                    if (tmp.hasOwnProperty(key)) {
                        const values = tmp[key];
                        console.log(tmp, key, values)
                        args.value.set(key, values[0])
                    }
                }
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

const testcase = ref(toTestcase())


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

    let res = store.source.messages.map(item => {
        let copied = { ...item };
        copied.content = copied.content.replace('{{}}', source)
        console.log(copied)
        return copied
    })

    api.apiPromptPost(res, store.source.name)
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

    var res = store.source.messages.filter(item => {
        return item.enable == true
    })



    let body: TestingRequestBody = {
        messages: res,
        key: caseKey.value,
        sources: [source],
        args: ArgumentHelper.toArgumentList(args.value)
    }

    await api.apiTestingPost(body, repeat.value).then(
        (response) => {
            let element = response.data[0]
            result.value.splice(0, 0, element)
        }
    )
}


async function debugAll() {
    var res = store.source.messages.map(item => item)



    if (useCase.value) {
        let body: TestingRequestBody = {
            messages: res,
            sources: config.value.data
        }
        await api.apiTestingPost(body, repeat.value).then(
            (response) => {
                result.value.splice(0, 0, ...response.data)
            }
        )
    } else {
        let body: TestingRequestBody = {
            messages: res,
            sources: ['']
        }
        await api.apiTestingPost(body, repeat.value).then(
            (response) => {
                result.value.splice(0, 0, ...response.data)
            }
        )
    }
}

async function listCase(refresh: boolean) {
    await api.apiCaseGet(refresh).then(
        (response) => {
            caseList.value = response.data
            console.log(caseList.value)
        }
    )
}

async function getCase(id: string) {
    await api.apiCaseKeyGet(id).then((response) => {

        console.log(response.data)

        config.value = response.data
    })
}


</script>