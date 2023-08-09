<script setup lang="ts">
import {ref} from "vue";
import {RouterView, useRouter} from 'vue-router';

import {MenuFoldOutlined, MenuUnfoldOutlined} from "@ant-design/icons-vue";
import {useSnapshotStore} from './stores/snapshot';

const router = useRouter()

const collapsed = ref(false)

const store = useSnapshotStore()

function routerTo(key: string) {
    router.push(key)
}

</script>

<template>
    <a-layout theme="light">
        <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible>
            <div class="logo"/>

            <a-menu theme="dark" @click="(e) => routerTo(e.key)" mode="inline" :style="{ lineHeight: '64px' }">
                <a-menu-item key="/view/index">Index</a-menu-item>
                <a-menu-item key="/view/dev">Dev</a-menu-item>
                <a-menu-item key="/view/debug">Debug</a-menu-item>
                <!-- <a-menu-item key="/view/compare">Compare</a-menu-item> -->
            </a-menu>
        </a-layout-sider>

        <a-layout>
            <a-layout-header style="background: #fff; padding: 0">
                <menu-unfold-outlined v-if="collapsed" class="trigger" @click="() => (collapsed = !collapsed)"/>
                <menu-fold-outlined v-else class="trigger" @click="() => (collapsed = !collapsed)"/>

            </a-layout-header>

            <a-layout-content :style="{ margin: '24px 16px', padding: '24px', background: '#fff', minHeight: '280px' }">
                <RouterView/>
            </a-layout-content>
        </a-layout>
        <!-- <a-layout-footer :style="footerStyle">Footer</a-layout-footer> -->
    </a-layout>
</template>

<style>
.trigger {
    font-size: 18px;
    line-height: 64px;
    padding: 0 24px;
    cursor: pointer;
    transition: color 0.3s;
}

.trigger:hover {
    color: #1890ff;
}

.logo {
    height: 32px;
    background: rgba(255, 255, 255, 0.3);
    margin: 16px;
}

.site-layout .site-layout-background {
    background: #fff;
}
</style>