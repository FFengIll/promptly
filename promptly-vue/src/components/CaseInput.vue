<script setup lang="ts">
import type { ArgumentSetting } from 'sdk/models';


const props = defineProps<{
    setting: ArgumentSetting,
    args: Map<string, string>

}>()


console.log(props.setting)

const emit = defineEmits<{
    (e: 'select', key: string, value: string): void
}>()

function onSelect(key, value) {
    console.log(key, value)
    emit('select', key, value)
}


function data() {
    return [{ key: 1, values: 2 }]
    return Object.keys(props.setting.args!!.keys).map(key => {
        return {
            key: key,
            values: props.setting.args!![key]
        }
    }
    )
}


const columns = [
    {
        name: 'Key',
        dataIndex: 'key',
        key: 'key',
    },
    {
        title: 'Age',
        dataIndex: 'values',
        key: 'values',
    },
    {
        title: 'Action',
        key: 'action',
    },
];

</script>

<template>
    <a-list item-layout="horizontal">
        <!-- <a-table :columns="columns" :data-source="data"> -->
        <!-- </a-table> -->

        <a-list-item v-for="(values, key) in  setting.args " :key="key">

            <a-input-group>
                <a-space direction="horizontal">
                    <a-typography-text>
                        {{ key }}
                    </a-typography-text>

                    <a-select ref="select" :value="args.get(key)" style="width: 300px"
                        @select="(value, option) => onSelect(key, value)">
                        <a-select-option v-for=" (v, index) in values" :key="v">{{ v }}</a-select-option>
                        <a-select-option :key="''">
                        </a-select-option>
                    </a-select>

                </a-space>

            </a-input-group>
        </a-list-item>


    </a-list>

    <slot name="extra"></slot>
</template>

<style scoped></style>
