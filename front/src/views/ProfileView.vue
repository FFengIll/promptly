

<template>
    <div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Button</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in keys" :key="item">
                    <td>{{ item }}</td>

                    <!-- <td>{{ item.id }}</td>
                    <td>{{ item.name }}</td> -->
                    <td>
                        <!-- FIXME: now we only use a name, not id -->
                        <button @click="handleButtonClick(item)">Jump</button>

                    </td>
                </tr>
            </tbody>
        </table>
    </div>
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
    computed:{
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
            this.redirectToPage(key)
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