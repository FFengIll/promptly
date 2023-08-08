<script setup lang="ts">
import {useClipboard} from '@vueuse/core';
import {useRouter} from 'vue-router';
import type {PromptItem} from "../../sdk";


const {text, copy, copied, isSupported} = useClipboard({})

const router = useRouter()

const props = defineProps<{
    messages: PromptItem[]
}>()


function copyRaw() {
    let res: string[] = []
    props.messages.forEach((m) => {
        res.push(m.role + ":\n" + m.content)
    })
    let whole = res.join('\n')
    copy(whole)

}

function copyJson() {
    let payload = JSON.stringify(props.messages)
    copy(payload)
}


</script>

<template>
    <a-space direction="horizontal">
        <a-space class="scroll-short" direction="vertical">
            <div v-for="item in messages">
                <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
                <span style="white-space: pre-line"> {{ item.content }}</span>
            </div>
        </a-space>
        <a-space direction="vertical">
            <a-button @click="copyJson" class="right">Copy to JSON</a-button>
            <a-button @click="copyRaw" class="right">Copy to RAW</a-button>
        </a-space>
    </a-space>
</template>

<style scoped>
.scroll-short {
    height: 200px;
    /* 设置组件容器的固定高度 */
    overflow: auto;
    /* 设置溢出部分自动滚动 */
}

.floating-container {
    position: fixed;

}

.right {
    float: right;
    text-align: right;
    /* additional styles if needed */
}
</style>