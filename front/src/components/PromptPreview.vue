<script setup lang="ts">
import {useRouter} from 'vue-router';
import type {PromptItem} from "../../sdk";

const router = useRouter()

defineProps<{
    messages: PromptItem[]
}>()


</script>

<template>
    <div v-for="item in messages">
        <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
        <span style="white-space: pre-line"> {{ item.content }}</span>
    </div>
</template>

<style scoped>

</style>