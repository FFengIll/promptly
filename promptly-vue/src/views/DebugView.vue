<template>
    <div>
        <!-- prompt view -->
        <a-row :gutter="12">
            <a-col :span="12">
                <a-card title="Prompt Snapshot">
                    <a-space direction="vertical" :style="{ width: '100%' }">
                        <div v-for="item in store.debug" :key="item.id">
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
                        <a-button type="primary" @click="run">Run Test</a-button>

                        <a-checkbox v-model:checked="useCase">Use Case</a-checkbox>

                    </a-space>
                </a-card>

                <!-- show dataset info -->
                <a-card title="Case List">
                    <!-- case select -->
                    Select Case to Debug:&nbsp;&nbsp;
                    <a-select style="width:300px" @change="getCase" v-model:value="config.id">
                        <a-select-option v-for="item in caseList" :key="item.id">
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
                                <a-button @click="do_request(record)">Request</a-button>
                            </span>
                        </template>
                    </template>

                </a-table>
            </a-col>
        </a-row>
    </div>
</template>
<script lang="ts" setup>
import {ref} from 'vue';

import {useSnapshotStore} from "@/stores/snapshot";


import type {DebugRequestBody} from '../../sdk/models';
import {DefaultApiFactory} from '../../sdk/apis/default-api';


const store = useSnapshotStore()

const api = DefaultApiFactory(undefined, "http://localhost:8000")

const loopCount = ref<number>(1);

const useCase = ref<boolean>(false)

const result = ref(
    [
        {id: 1, source: "test", target: "test"},
        {id: 2, source: "test", target: "test"},
        {id: 3, source: "test", target: "test"},
        // 其他数据项
    ]
)

const config = ref({
    id: 1,
    data: ["1", "2"],
    description: "description"

})

const caseList = ref(
    [
        {id: 1, name: "test", description: "test", data: [1, 2, 3, 4]},
        {id: 2, name: "test", description: "test", data: [1, 3, 4]},
    ],
)

listCase()


const columns = [
    {
        title: 'id',
        dataIndex: 'id',
        key: 'id',
    },
    {
        title: 'case',
        dataIndex: 'source',
        key: 'source',
    },
    {
        title: 'result',
        dataIndex: 'target',
        key: 'target',
    },
    {
        title: 'action',
        dataIndex: 'action',
        key: 'action',
    },
]

async function do_request(params: { id: 1, source: "" }) {
    console.log(params)

    var res = store.debug.map(item => item)
    let body: DebugRequestBody = {
        messages: res,
        source: params.source
    }
    await api.apiDebugSourcePost(body).then(
        (response) => {
            response.data.forEach(element => {
                result.value[params.id] = element
            });
        }
    )
}


async function run() {

    if (useCase.value) {
        var res = store.debug.map(item => item)
        await api.apiDebugPost(res, config.value.id,).then(
            (response) => {
                result.value = response.data
            }
        )
    } else {
        var res = store.debug.map(item => item)
        await api.apiDebugLoopPost(res, loopCount.value).then(
            (response) => {
                result.value = response.data
            }
        )
    }
}

async function listCase() {
    await api.caseGet().then(
        (response) => {
            caseList.value = response.data
            console.log(caseList.value)
        }
    )
}

async function getCase(id: number) {
    await api.caseKeyGet(id).then((response) => {
        config.value = response.data

        let array: string[] = config.value.data

        result.value = array.map(
            (elem, index) => {
                return {id: index, source: elem, target: ""}
            }
        )
    })
}


</script>