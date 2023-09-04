<script setup lang="ts">
import { HeartOutlined, HeartTwoTone } from "@ant-design/icons-vue";

const props = defineProps<{
    model: string,
    defaultModel: string,
}>()


const emit = defineEmits<{
    (e: 'select', value: string): void
    (e: 'default', value: string): void

}>()

function onSelect(value: string) {
    console.log(value)
    emit('select', value)
}

function onDefault(value: string) {
    console.log(value)
    emit('default', value)
}

const models = [
    "gpt-3.5-turbo-0613",
    "gpt-4-0613",
    'anthropic/claude-instant-v1',
    "local/codellama-7b",
]

</script>

<template>
    <a-select ref="select" v-model:value="props.model" style="width: 120px" @change="onSelect">
        <a-select-option v-for="value in models" :value="value">
            <a-button @click="onDefault(value)">
                <template #icon>
                    <HeartTwoTone v-if="value == defaultModel" two-tone-color="#eb2f96" />
                    <HeartOutlined v-else />
                </template>
            </a-button>
            {{ value }}
        </a-select-option>

    </a-select>
</template>

<style scoped></style>
