<script setup lang="ts">

import {CloseOutlined, CopyOutlined, DownOutlined, PlusOutlined, UpOutlined} from "@ant-design/icons-vue";

import {useClipboard} from '@vueuse/core';
import {useRouter} from 'vue-router';

import type {Message} from "@/sdk/models";


const {text, copy, copied, isSupported} = useClipboard({})

const router = useRouter()

const emit = defineEmits<{
    (e: 'orderUp', index: number): void
    (e: 'orderDown', index: number): void
    (e: 'remove', index: number): void
    (e: 'add', index: number): void
}>()


export interface Props {
    messages: Message[],
    withControl?: boolean,
    withCopy?: boolean
    withSidebar?: boolean
    title?: string
    withEnable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
        withControl: false,
        withCopy: false,
        withSidebar: false,
        title: "",
        withEnable: false,
    }
)


function orderUp(index,) {
    emit('orderUp', index,)
}

function orderDown(index,) {
    emit('orderDown', index,)
}

function add(index) {
    emit('add', index)
}

function remove(index) {
    emit('remove', index)
}

function color(role: string) {
    switch (role) {
        case 'user':
            return {color: 'blue'}

            break;
        case 'system':
            return {color: 'red'}

        case 'assitant':
            return {color: 'black'}
            break
        default:
            break;
    }
}

const dragData = () => {
    let res = []
    for (let i = 0; i < props.messages.length; i++) {
        res.push(i)
    }
    return res
}

</script>

<template>
    <!-- <draggable v-model="props.messages" key="content">
        <template #item="{ element }">
            <div> {{ element.content }} </div>
        </template>
</draggable> -->

    <div
        v-for="(item, index) in messages"
        :key="index"
    >
        <div v-if="(withEnable && item.enable) || (!withEnable)">
            <a-row v-if="withControl">
                <a-divider>
                    <a-space>
                        <a-button
                            shape="round"
                            @click="add(index)"
                        >
                            <template #icon>
                                <PlusOutlined/>
                            </template>
                        </a-button>


                        <!-- up down the order -->
                        <a-button
                            shape="round"
                            @click="orderUp(index,)"
                        >
                            <template #icon>
                                <UpOutlined/>
                            </template>
                        </a-button>
                        <a-button
                            shape="round"
                            @click="orderDown(index)"
                        >
                            <template #icon>
                                <DownOutlined/>
                            </template>
                        </a-button>


                        <a-button
                            v-if="withSidebar"
                            :style="color(item.role)"
                        >
                            {{ item.role }}
                        </a-button>


                        <a-popconfirm
                            title="Are you sure delete this task?"
                            ok-text="Yes"
                            cancel-text="No"
                            @confirm="remove(index)"
                        >
                            <a-button shape="round">
                                <template #icon>
                                    <CloseOutlined/>
                                </template>
                            </a-button>
                        </a-popconfirm>

                        <a-divider type="vertical"></a-divider>


                        <a-button
                            shape="round"
                            v-if="withCopy"
                            @click="copy(JSON.stringify(item.content))"
                        >
                            <CopyOutlined/>
                        </a-button>

                        <a-divider type="vertical"></a-divider>

                        <a-space v-if="withControl">
                            <a-switch
                                size="default"
                                v-model:checked="item.enable"
                                checked-children="On"
                                un-checked-children="Off"
                            />
                        </a-space>

                    </a-space>

                </a-divider>
            </a-row>
            <a-row>
                <!-- role -->
                <a-space direction="vertical">
                    <a-radio-group
                        v-if="!withSidebar"
                        v-model:value="item.role"
                        option-type="button"
                        button-style="solid"
                    >
                        <a-radio-button value="user">User</a-radio-button>
                        <a-radio-button value="system">System</a-radio-button>
                        <a-radio-button value="assistant">Assitant</a-radio-button>
                    </a-radio-group>
                </a-space>
            </a-row>
            <a-row>

                <a-col :span='24'>
                    <!-- content edit -->
                    <a-textarea
                        :disabled="!item.enable"
                        v-model:value="item.content"
                        :rows="4"
                        placeholder="textarea with clear icon"
                    />
                </a-col>

            </a-row>

        </div>
    </div>
</template>

<style scoped></style>