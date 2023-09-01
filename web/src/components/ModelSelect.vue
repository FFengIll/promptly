<script setup lang="ts">
const props = defineProps<{
    model: string,
}>()


const emit = defineEmits<{
    (e: 'select', value: string): void
}>()

function onSelect(value: string) {
    console.log(value)
    emit('select', value)
}

const models = [
    "gpt-3.5-turbo",
    'anthropic/claude-instant-v1'
]

</script>

<template>
    <a-select ref="select" v-model:value="props.model" style="width: 120px" @change="onSelect">
        <a-select-option v-for="value in models" :value="value">{{ value }}</a-select-option>

    </a-select>
</template>

<style scoped></style>
