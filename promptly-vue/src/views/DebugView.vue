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
                                <a-textarea v-model:value="item.content" auto-size></a-textarea>
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
                                <ArrowUpOutlined />
                            </template>
                            <template #downIcon>
                                <ArrowDownOutlined />
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
                    <a-select style="width:300px" @change="getCase">
                        <div v-for="item in data.case_list" :key="item.id">
                            <a-select-option value="item.id">
                                {{ item.name }}
                            </a-select-option>
                        </div>
                    </a-select>
                    <a-divider />

                    <!-- case description -->
                    Case Description:&nbsp;&nbsp;
                    <span>{{ data.option.case.description }}</span>
                    <a-divider />

                    <div v-for="item in data.option.case.data" :key="item">
                        <a-list-item>{{ item }}</a-list-item>
                    </div>
                </a-card>
            </a-col>
        </a-row>
        <a-row>
            <a-col :span="24">

                <!-- show result -->
                <a-table :dataSource="result" :columns="columns" :rowKey="(record: any) => record.id" />
            </a-col>
        </a-row>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue';

import { useSnapshotStore } from "@/stores/snapshot";

import { ArrowDownOutlined, ArrowUpOutlined } from '@ant-design/icons-vue';

import { DefaultApiFactory } from '../../sdk/apis/default-api';


const store = useSnapshotStore()

const api = DefaultApiFactory(undefined, "http://localhost:8000")

const loopCount = ref<number>(1);

const useCase = ref<boolean>(false)

const result = ref(
    [
        { id: 1, source: "test", target: "test" },
        { id: 2, source: "test", target: "test" },
        { id: 3, source: "test", target: "test" },
        // 其他数据项
    ]
)

const data = ref({
    option: {
        case: {
            id: 1,
            data: ["1", "2"],
            description: "description"
        },

    },
    case_list: [
        { id: 1, name: "test", describe: "test", data: [1, 2, 3, 4] },
        { id: 2, name: "test", describe: "test", data: [1, 3, 4] },
    ],

}
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
]


async function run() {

    if (useCase.value) {
        var res = store.debug.map(item => item)
        await api.apiDebugPost(res, data.value.option.case.id,).then(
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
            data.value.case_list = response.data
            console.log(data.value.case_list)
        }
    )
}

async function getCase(id: number) {
    await api.caseKeyGet(id).then((response) => {
        data.value.option.case = response.data
    })
}


</script>