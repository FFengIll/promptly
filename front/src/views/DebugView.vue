<template>
    <div>
        <!-- a dataset select -->
        <a-select style="width:300px">
            <div v-for="item in dataset" :key="item.id">
                <a-select-option value="item.id">
                    <span>{{ item.name }}</span>{{ item.describe }}
                </a-select-option>
            </div>
        </a-select>

        <!-- show dataset info -->
        <a-card>
            <p>dataset info</p>
        </a-card>


        <!-- prompt view -->
        <div>
            <a-card title="prompt view">
                <div v-for="item in profile.messages" :key="item.id">
                    <p>
                        <a-typography-text code>{{ item.role }}</a-typography-text>
                        {{ item.content }}
                    </p>
                </div>
            </a-card>
        </div>


        <!-- click to run -->
        <a-button type="primary" @click="run_test">Run Test</a-button>


        <!-- show dataset item and corresponding answer -->
        <div v-for="item in result" :key="item.id">
            <a-card>
                <p>{{ item.source }}</p>
                <p>{{ item.target }}</p>
            </a-card>
        </div>


    </div>
</template>
  
<script >
import { Button, message } from 'ant-design-vue';
import axios from 'axios';


export default {
    methods: {
        run_test() {
            axios.get(`API_TEST/${this.key}/${this.use_dataset}`)
                .then(response => {
                    this.result = response.data.result;
                })
                .catch(error => {
                    console.error(error);
                });
        }
    },
    data() {
        return {
            use_dataset: "",
            profile: {
                "messages": [
                    {
                        role: 1,
                        content: 2,
                        id: 1,
                    }
                ],
            },
            dataset: [
                { id: 1, name: "test", describe: "test" },
            ],
            result: [
                { id: 1, source: "test", target: "test" },
                { id: 2, source: "test", target: "test" },
                { id: 3, source: "test", target: "test" },
                // 其他数据项
            ]
        };
    }
};
</script>
  