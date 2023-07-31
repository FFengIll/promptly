<script lang="ts">
export default {
    data() {
        return {
            history: [1, 2, 3]
        }
    }
}

</script>

<template>
    <div v-for="item in history" :key="item.id">
        <a-card>

            <p>
                {{ item.content }}
            </p>
        </a-card>
    </div>
</template>