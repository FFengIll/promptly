<script setup lang="ts">
import { HeartOutlined, HeartTwoTone } from "@ant-design/icons-vue";


interface Props {
    selected: string,
    prefer: string,
    models: string[],
}

const props = withDefaults(defineProps<Props>(), {
    model: "",
    prefer: "",
    models: () => [],
})


const emit = defineEmits<{
    (e: 'select', value: string): void
    (e: 'prefer', value: string): void

}>()

function onSelect(value: string) {
    console.log(value)
    emit('select', value)
}

function onDefault(value: string) {
    console.log(value)
    emit('prefer', value)
}

</script>

<template>
    <div>
        <a-select style="width: 200px" ref="select" v-model:value="props.selected" @change="onSelect">
            <a-select-option v-for="(value, key)  in models" :value="value">
                <a-button @click="onDefault(value)">
                    <template #icon>
                        <HeartTwoTone v-if="value == prefer" two-tone-color="#eb2f96" />
                        <HeartOutlined v-else />
                    </template>
                </a-button>
                {{ value }}
            </a-select-option>

        </a-select>
    </div>
</template>

<style scoped></style>
