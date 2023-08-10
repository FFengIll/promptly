<script setup lang="ts">

import { CloseOutlined, DownOutlined, PlusOutlined, UpOutlined } from "@ant-design/icons-vue";

import { useClipboard } from '@vueuse/core';
import { useRouter } from 'vue-router';

import type { Message } from "../../sdk";


const { text, copy, copied, isSupported } = useClipboard({})

const router = useRouter()

const emit = defineEmits<{
    (e: 'orderUp', id: number): void
    (e: 'orderDown', id: number): void
    (e: 'remove', id: number): void
    (e: 'add', id: number): void
}>()


const props = defineProps<{
    messages: Message[],
    withControl?: boolean,
    withCopy?: boolean
    withSidebar?: boolean
}>(

)


function orderUp(id,) {
    emit('orderUp', id,)
}

function orderDown(id,) {
    emit('orderDown', id,)
}

function add(id) {
    emit('add', id)
}

function remove(id) {
    emit('remove', id)
}

function color(role: string) {
    switch (role) {
        case 'user':
            return { color: 'blue' }

            break;
        case 'system':
            return { color: 'red' }

        case 'assitant':
            return { color: 'black' }
            break
        default:
            break;
    }
}

</script>

<template>
    <a-card v-for="item in messages" :key="item.id">
        <!-- <template #extra><a href="#">more</a></template> -->

        <a-row v-if="withControl">
            <a-divider>
                <a-space>
                    <a-button @click="add(item.id)">
                        <template #icon>
                            <PlusOutlined />
                        </template>
                    </a-button>

                    <a-divider type="vertical"></a-divider>

                    <!-- up down the order -->
                    <a-button type="primary" shape="round" @click="orderUp(item.id,)">
                        <template #icon>
                            <UpOutlined />
                        </template>
                    </a-button>
                    <a-button type="primary" shape="round" @click="orderDown(item.id,)">
                        <template #icon>
                            <DownOutlined />
                        </template>
                    </a-button>

                    <a-divider type="vertical"></a-divider>

                    <a-popconfirm title="Are you sure delete this task?" ok-text="Yes" cancel-text="No"
                        @confirm="remove(item.order)">
                        <a-button>
                            <template #icon>
                                <CloseOutlined />
                            </template>
                        </a-button>
                    </a-popconfirm>

                </a-space>

            </a-divider>

        </a-row>
        <a-row>

            <!-- role -->
            <a-space direction="vertical">
                <a-radio-group v-if="!withSidebar" v-model:value="item.role" option-type="button" button-style="solid">
                    <a-radio-button value="user">User</a-radio-button>
                    <a-radio-button value="system">System</a-radio-button>
                    <a-radio-button value="assistant">Assitant</a-radio-button>
                </a-radio-group>
            </a-space>
            <a-divider type="vertical"></a-divider>

            <!-- role select -->
            <!-- <a-select ref="select" v-model:value="item.role" style="width: 120px">
                <a-select-option value="user">
                    <span style="color: black">User</span></a-select-option>
                <a-select-option value="system">
                    <span style="color: red">System</span>
                </a-select-option>
                <a-select-option value="assistant">
                    <span style="color: blue">Assistant</span>
                </a-select-option>
            </a-select> -->

            <!-- enable toggle -->
            <a-space direction="horizontal">
                <a-button v-if="withSidebar" :style="color(item.role)">
                    {{ item.role }}
                </a-button>
                <a-space v-if="withControl">
                    <a-typography-text>Enable</a-typography-text>
                    <a-switch v-model:checked="item.enable"></a-switch>
                </a-space>
                <a-button v-if="withCopy" @click="copy(JSON.stringify(item.content))">Copy JSON</a-button>
            </a-space>
        </a-row>
        <a-row :gutter="12" align="middle">

            <a-col :span='24'>
                <!-- content edit -->
                <a-textarea v-model:value="item.content" :auto-size="{ minRows: 3, maxRows: 5 }"
                    placeholder="textarea with clear icon" />
            </a-col>

        </a-row>


    </a-card>
</template>

<style scoped></style>