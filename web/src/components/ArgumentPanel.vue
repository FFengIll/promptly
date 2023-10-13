<script setup lang="ts">
import type { Argument, ArgumentSetting } from '@/sdk/models';

export interface Props {
    setting: ArgumentSetting,
    args: Argument[],
    mask: string[],
}

const props = withDefaults(
    defineProps<Props>(),
    {
        args: () => new Array<Argument>(),
        mask: () => new Array<string>()
    }
)

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

function isDisable(key: string) {
    console.log(props.mask)

    // if (props.mask.findIndex(key) >= 0) {
    //     return true
    // }

    return false
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

function getSelect(key: string) {
    for (const item of props.args) {
        if (item.key == key) {
            return item.value
        }
    }
    return ""
}

</script>

<template>
    <a-list item-layout="horizontal">
        <!-- <a-table :columns="columns" :data-source="data"> -->
        <!-- </a-table> -->
        <slot name="extra"></slot>

        <a-list-item v-for="(arg, index) in  setting.args " :key="index">

            <a-space direction="horizontal" align="baseline">
                <a-typography-text>
                    {{ arg.key }}
                </a-typography-text>

                <a-select :disabled="isDisable(arg.key)" ref="select" :value="getSelect(arg.key)" style="width: 300px"
                    @select="(value, option) => onSelect(arg.key, value)">

                    <a-select-option :key="''">
                    </a-select-option>

                    <a-select-option v-for=" (v, index) in arg.candidates" :key="v">
                        <a-popover :title="v">
                            <template #content>
                                <p> {{ v }}</p>
                            </template>
                            {{ v }}
                        </a-popover>

                    </a-select-option>

                </a-select>

            </a-space>

        </a-list-item>

    </a-list>

</template>

<style scoped></style>
