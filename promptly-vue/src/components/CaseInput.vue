<script setup lang="ts">

const props = defineProps<{
    args: {
        key: string, value: string
    }[]
}>()


</script>

<template>
    <a-list item-layout="horizontal" :data-source="props.args">

        <template #renderItem="{ item }">
            <a-list-item>
                <!-- <template #actions>
                    <a key="list-loadmore-edit">edit</a>
                    <a key="list-loadmore-more">more</a>
                </template> -->
                <a-input-group>
                    <a-space direction="horizontal">
                        <a-typography-text>
                            Key
                        </a-typography-text>
                        <a-input v-model:value="item.key"></a-input>

                        <a-typography-text>
                            Value
                        </a-typography-text>
                        <a-input v-model:value="item.value"></a-input>

                    </a-space>

                </a-input-group>
            </a-list-item>
        </template>
    </a-list>
</template>

<style scoped></style>
