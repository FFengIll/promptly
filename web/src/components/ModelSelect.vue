<script setup lang="ts">
import { HeartOutlined, HeartTwoTone } from "@ant-design/icons-vue";


interface Props {
    selected: string,
    defaultModel: string,
    models: string[],
}

const props = withDefaults(defineProps<Props>(), {
    model: "",
    defaultModel: "",
    models: () => [],
})


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

</script>

<template>
    <a-select ref="select" v-model:value="props.selected" style="width: 120px" @change="onSelect">
        <a-select-option v-for="item, key in models" :value="item">
            <a-button @click="onDefault(item)">
                <template #icon>
                    <HeartTwoTone v-if="item == defaultModel" two-tone-color="#eb2f96" />
                    <HeartOutlined v-else />
                </template>
            </a-button>
            {{ item }}
        </a-select-option>

    </a-select>
</template>

<style scoped></style>
