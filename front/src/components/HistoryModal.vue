<template>
    <div>
        <a-modal v-model:open="open" title="Basic Modal"
            @ok="handleOk">
            <p>Some contents...</p>
            <p>Some contents...</p>
            <p>Some contents...</p>
        </a-modal>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue';

const open = ref<boolean>(true);

const showModal = () => {
    open.value = true;
};

const handleOk = (e: MouseEvent) => {
    console.log(e);
    open.value = false;
};
</script>
  
  