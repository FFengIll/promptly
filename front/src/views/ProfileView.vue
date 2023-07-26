

<template>
    <a-card title="Click to Open Prompt Detail">
        <a-list v-for="item in keys" :key="item" size="small">
            <a-list-item>
                <a v-bind:href="handleButtonClick(item)">{{ item }}</a>
            </a-list-item>
        </a-list>

    </a-card>
</template>
  
<script lang="ts">
import { DefaultApiFactory } from "../../sdk/apis/default-api";

const api = DefaultApiFactory(undefined, "http://localhost:8000")

export default {
    data() {
        return {

            keys: [
                '1', '2', '3'
            ]
        };
    },
    created() {
        this.fetchList()
    },
    computed: {
        api: () => api
    },
    methods: {
        redirectToPage(key: string) {
            this.$router.push('/view/prompt/' + key);
        },

        handleButtonClick(key: string) {
            // 处理按钮点击事件
            console.log("Button clicked for item with ID:", key);

            // TODO: jump to another page /prompt/id
            // this.redirectToPage(key)

            return '/view/prompt/' + key
        },

        async fetchList() {
            return this.api.listProfileProfileGet().then(
                response => {
                    console.log(response.data)
                    this.keys = response.data.keys
                    return response.data
                }
            ).catch(
                error => {
                    return {
                        keys: [
                            '1', '2', '3'
                        ]
                    };
                }
            )
        }
    }
};
</script>