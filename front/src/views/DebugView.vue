<template>
    <div>
        <!-- prompt view -->
        <a-row :gutter="12">
            <a-col :span="12">
                <a-card title="Prompt Snapshot">
                    <a-space direction="vertical" :style="{ width: '100%' }">
                        <div v-for="item in debug" :key="item.id">
                            <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
                            <span>
                                <a-textarea v-model:value="item.content" auto-size></a-textarea>
                            </span>
                        </div>
                    </a-space>
                </a-card>
            </a-col>
            <a-col :span="12">





                <!-- show dataset info -->
                <a-card title="Case List">
                    <!-- case select -->
                    Select Case to Debug:&nbsp;&nbsp;
                    <a-select style="width:300px" @change="getCase">
                        <div v-for="item in case_list" :key="item.id">
                            <a-select-option value="item.id">
                                {{ item.name }}
                            </a-select-option>
                        </div>
                    </a-select>
                    <a-divider />

                    <!-- case description -->
                    Case Description:&nbsp;&nbsp;
                    <span>{{ option.case.description }}</span>
                    <a-divider />

                    <div v-for="item in option.case.data" :key="item">
                        <a-list-item>{{ item }}</a-list-item>
                    </div>
                </a-card>
            </a-col>


        </a-row>
        <a-row>
            <a-col :span="24">
                <!-- click to run -->
                <a-button type="primary" @click="run">Run Test</a-button>

                <!-- show result -->
                <a-table :dataSource="dataSource" :columns="columns" :rowKey="(record) => record.id" />
            </a-col>
        </a-row>
    </div>
</template>
<script lang="ts">
import { useSnapshotStore } from '@/stores/snapshot';
import { mapActions, mapState } from 'pinia';
import { DefaultApiFactory } from '../../sdk/apis/default-api';

const api = DefaultApiFactory(undefined, "http://localhost:8000")

export default {
    data() {
        return {
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
            result: [
                { id: 1, source: "test", target: "test" },
                { id: 2, source: "test", target: "test" },
                { id: 3, source: "test", target: "test" },
                // 其他数据项
            ]
        };
    },
    created() {
        // load test case list
        // await this.api.getExtensionsExtensionsGet()
        // load test case data
        // load profile snapshot
        this.listCase()
    },
    computed: {
        ...mapState(useSnapshotStore, ['debug']),
        api() {
            return api
        },
        dataSource() {
            return this.result
        },
        columns() {
            return [
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
        }
    },

    methods: {
        ...mapActions(useSnapshotStore, ['sendToDebug']),
        async run() {
            var res = this.debug.map(item => item)

            await this.api.debugDebugPost(res, this.option.case.id,).then(
                (response) => {
                    this.result = response.data
                }
            )
        },
        async listCase() {
            await this.api.listCaseCaseGet().then(
                (response) => {
                    this.case_list = response.data
                    console.log(this.case_list)
                }
            )
        },
        async getCase(id: number) {
            await this.api.getCaseCaseKeyGet(id).then((response) => {
                this.option.case = response.data
            })
        }

    },
};
</script>