<script setup lang="ts">
import {useRouter} from 'vue-router';

const router = useRouter()

defineProps<{
    messages: [{
        role: string,
        content: string,
        enable: boolean,
    }]
}>()


</script>

<template>
    <div v-for="item in messages">
        <a-list-item v-if="item.enable">
            <span :style="{ color: 'blue' }">{{ item.role }} </span><span>:&nbsp;</span>
            <span style="white-space: pre-line"> {{ item.content }}</span>
        </a-list-item>
    </div>
</template>

<style scoped>

</style>