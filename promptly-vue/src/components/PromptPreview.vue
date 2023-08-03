<script setup lang="ts">
import { useClipboard } from '@vueuse/core';
import { useRouter } from 'vue-router';
import type { PromptItem } from "../../sdk";


const { text, copy, copied, isSupported } = useClipboard({  })

const router = useRouter()

const props = defineProps<{
    messages: PromptItem[]
}>()


function copyJson(){
    let payload= JSON.stringify(props.messages)
    copy(payload)
}


</script>

<template>
    <a-button @click="copyJson">Copy to JSON</a-button>
    <div v-for="item in messages">
        <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
        <span style="white-space: pre-line"> {{ item.content }}</span>
    </div>
</template>

<style scoped>

</style>