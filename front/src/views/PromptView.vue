<template>
    <div>
        <a-row :span="26">
            <a-col class="gutter-row" :span="12">
                <div v-for="item in profile.messages" :key="item.id" class="card">
                    <a-card>
                        <!-- <template #extra><a href="#">more</a></template> -->
                        <!-- role select -->
                        <a-select ref="select" v-model:value="item.role" style="width: 120px">
                            <a-select-option value="user">User</a-select-option>
                            <a-select-option value="system">System</a-select-option>
                            <a-select-option value="assistant">Assistant</a-select-option>
                        </a-select>

                        <!-- enable toggle -->
                        <a-switch v-model:checked="item.enable">Enable</a-switch>

                        <a-button @click="order(item.id, -1)">Up</a-button>
                        <a-button @click="order(item.id, 1)">Down</a-button>

                        <!-- content edit -->
                        <a-textarea v-model:value="item.content" placeholder="textarea with clear icon" allow-clear
                            :auto-size="{ minRows: 4, maxRows: 6 }" />


                        <!-- TODO: history select -->
                        <a-collapse>
                            <a-collapse-panel>
                                <div v-for="h in item.history">
                                    <a-row>
                                        <a-col :span="20">
                                            <p>{{ h }}</p>
                                            <!-- <a-textarea v-bind="h"> </a-textarea> -->
                                        </a-col>
                                        <!-- <button v-on:click="copy(h)">复制到剪贴板</button> -->
                                        <a-col :span="2">
                                            <button v-on:click="setContent(item.id, h)">Set</button>
                                        </a-col>
                                    </a-row>
                                </div>
                            </a-collapse-panel>
                        </a-collapse>

                    </a-card>
                </div>
            </a-col>
            <a-col class="gutter-row" :span="12">
                <div>
                    <a-button @click="reload">reload</a-button>
                    <a-button @click="chat">Chat</a-button>
                    <a-button>Go To Test</a-button>
                    <a-button>Good</a-button>
                    <a-button>Bad</a-button>
                    <a-textarea v-model:value="response" :auto-size="{ minRows: 20 }" placeholder="textarea with clear icon"
                        allow-clear />

                </div>
            </a-col>
        </a-row>
    </div>
</template>
  
<script lang="ts">
import useClipboard from 'vue-clipboard3';

import { useRoute } from 'vue-router';
import { DefaultApiFactory } from '../../sdk/apis/default-api';

const api = DefaultApiFactory(undefined, "http://localhost:8000")
const { toClipboard } = useClipboard()

export default {
    // props: ['key'],
    data() {
        return {
            modal: false,
            key: "",
            history: [],
            response: "",
            profile: {
                "messages": [
                    { id: 1, role: "角色1", content: "内容1", enable: true, order: 0 },
                    { id: 2, role: "角色2", content: "内容2", enable: true, order: 1 },
                    { id: 3, role: "角色3", content: "内容3", enable: false, order: 2 },
                    // 其他数据项
                ]
            }
        };
    },
    mounted() {
    },
    created() {
        const route = useRoute();
        this.key = route.params.key.toString();
        this.fetchProfile(this.key);
    },
    computed: {
        api: () => api
    },
    methods: {
        order(id: number, delta: number) {
            let index = this.profile.messages.findIndex((m) => {
                return (m.id == id)
            })

            if (index < 0) {
                return
            }

            console.log(index)

            let temp = this.profile.messages[index]
            this.profile.messages[index] = this.profile.messages[index + delta]
            this.profile.messages[index + delta] = temp

            for (var i = 0; i < this.profile.messages.length; i++) {
                this.profile.messages[i].order = i
            }

            console.log(this.profile.messages)
        },
        setContent(id: number, content: string) {
            this.profile.messages.forEach((m) => {
                if (m.id == id) {
                    m.content = content
                }
            })
        },
        async copy(content: string) {
            await toClipboard(content)
        },
        handleOk(e: MouseEvent) {
            console.log(e);
            this.modal = false;
        },
        async fetchProfile(key: string) {
            this.api.loadProfileProfileKeyGet(key)
                .then(response => {
                    this.profile = response.data.profile;
                })
                .catch(error => {
                    console.error(error);
                    return null;
                });
        },
        reload() {
            this.fetchProfile(this.key);
        },
        chat() {
            var res = this.profile.messages;
            console.log(res);
            this.api.chatChatKeyPost(res, this.key)
                .then(response => {
                    console.log(response.data);
                    this.response = response.data;
                })
                .catch(error => {
                    console.error(error);
                    return;
                });

        },
    },
};
</script>
  