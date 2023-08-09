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
                <a-card title="Prompt Snapshot">
                    <a-typography-text>
                        Source: {{ store.source.name }}
                    </a-typography-text>
                    <a-button @click="gotoSource(store.source.name)"> Go To Source</a-button>
                    <a-divider></a-divider>
                    <a-space>
                        <a-button @click="sendBack('')">Write Back</a-button>
                    </a-space>
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

                <a-card title="Operation">
                    <a-space align="middle">

                        <!-- loop -->
                        <a-input-number title="Loop" id="inputNumber" v-model:value="loopCount" :min="1" :max="10">
                            <template #upIcon>
                                <ArrowUpOutlined/>
                            </template>
                            <template #downIcon>
                                <ArrowDownOutlined/>
                            </template>
                        </a-input-number>

                        <!-- click to run -->
                        <a-button type="primary" @click="debugAll">Run Test</a-button>

                        <a-checkbox v-model:checked="useCase">Use Case</a-checkbox>

                    </a-space>
                </a-card>

                <!-- show dataset info -->
                <a-card title="Case List">
                    <a-button @click="listCase(true)">Refresh</a-button>

                    <!-- case select -->
                    Select Case to Debug:&nbsp;&nbsp;
                    <a-select style="width:300px" @change="getCase">
                        <a-select-option v-for="item in caseList" :key="item.name">
                            {{ item.name }}
                            <a-divider type="vertical"/>
                            {{ item.description }}
                        </a-select-option>
                    </a-select>
                    <a-divider/>

                    <!-- case description -->
                    Case Description:&nbsp;&nbsp;
                    <span>{{ config.description }}</span>
                    <a-divider/>

                    <!-- <div v-for="item in config.data" :key="item">
                        <a-list-item>{{ item }}</a-list-item>
                    </div> -->
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
                                <a-button @click="debugOne(record)">Request</a-button>
                                <a-button @click="sendBack(record.source)">Send Back</a-button>
                                <a-button @click="gotoSource(store.source.name)"> Go To Source</a-button>

                            </span>
                        </template>
                        <template v-else-if="column.key === 'source'">
                            <a-tooltip placement="topLeft" :overlay-inner-style="{width:'500px'}">
                                <template #title>
                                    {{ JSON.stringify(record.source) }}
                                </template>
                                {{ JSON.stringify(record.source) }}

                            </a-tooltip>
                        </template>
                        <template v-else-if="column.key === 'target'">
                            <a-tooltip placement="topLeft" :overlay-inner-style="{width:'500px'}">
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
import {ref} from 'vue';

import type {TableColumnType} from 'ant-design-vue';

import {useSnapshotStore} from "@/stores/snapshot";


import type {DebugRequestBody} from '../../sdk';
import {DefaultApiFactory} from '../../sdk/apis/default-api';
import router from "@/router";


const store = useSnapshotStore()

const api = DefaultApiFactory(undefined, "http://localhost:8000")

const loopCount = ref<number>(1);

const useCase = ref<boolean>(false)

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
    data: ["1", "2"],
    description: "description"

})

const caseList = ref(
    [
        {id: 1, name: "test", description: "test", data: [1, 2, 3, 4]},
    ],
)

listCase(false)


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
        ellipsis: {showTitle: false},
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
        let copied = {...item};
        copied.content = copied.content.replace('{{}}', source)
        console.log(copied)
        return copied
    })

    api.apiPromptKeyPost(res, store.source.name)
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

async function debugOne(params: Params) {
    console.log(params)

    var res = store.source.messages.filter(item => {
        return item.enable == true
    })
    let body: DebugRequestBody = {
        messages: res,
        source: params.source
    }
    await api.apiTestingSourcePost(body).then(
        (response) => {
            let element = response.data[0]
            element.id = params.id
            result.value.push(element)
        }
    )
}


async function debugAll() {
    var res = store.source.messages.map(item => item)

    if (useCase.value) {
        await api.apiTestingCasePost(res, config.value.id,).then(
            (response) => {
                result.value = result.value.concat(response.data)
            }
        )
    } else {
        await api.apiTestingLoopPost(res, loopCount.value).then(
            (response) => {
                result.value = result.value.concat(response.data)
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
        config.value = response.data

        let array: string[] = config.value.data

        console.log(response.data)

        result.value = array.map(
            (elem, index) => {
                return {id: index, source: elem, target: ""}
            }
        )
    })
}


</script>