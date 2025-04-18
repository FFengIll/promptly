<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterView, useRoute, useRouter } from 'vue-router';

import { MenuFoldOutlined, MenuUnfoldOutlined } from "@ant-design/icons-vue";
import { backend } from "./scripts/backend";
import { useConfigStore } from "./stores/global-config";


const router = useRouter()
const r = useRoute()

const collapsed = ref(false)

const store = useConfigStore()

onMounted(
    () => {
        if (store.globalArgs.args == null) {
            console.log("fetch global args")
            backend.apiGlobalArgsGet()
                .then((res) => {
                    store.updateArgs(res.data.args ?? [])
                })
        }
        if (store.globalModels.models == null) {
            console.log("fetch global models")
            backend.apiGlobalModelsGet()
                .then((res) => {
                    store.updateModels(res.data)
                })
        }
    }
)

function routerTo(view: string) {
    const key = r.params.key;
    let path = `/view/${view}`
    console.log(view)
    if (view != 'index') {
        if (key && key.length > 0) {
            console.log(router.currentRoute)
            path = `${path}/${key}`
        }
    }

    router.push(path)
}

</script>

<template>
    <a-layout theme="light">
        <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible>
            <div class="logo" />


          <menu-unfold-outlined v-if="collapsed" class="trigger icon-white"  @click="() => (collapsed = !collapsed)" />
          <menu-fold-outlined v-else class="trigger icon-white"  @click="() => (collapsed = !collapsed)" />

            <a-menu theme="dark" @click="(e) => routerTo(e.key)" mode="inline" :style="{ lineHeight: '64px' }">
                <a-menu-item key="index">Index</a-menu-item>
                <a-menu-item key="prompt">Prompt</a-menu-item>
                <a-menu-item key="commit">Commit</a-menu-item>
                <a-menu-item key="testing">Testing</a-menu-item>
                <!-- <a-menu-item key="/view/compare">Compare</a-menu-item> -->
            </a-menu>
        </a-layout-sider>

        <a-layout>
            <a-layout-content :style="{ margin: '24px 16px', padding: '24px', background: '#fff', minHeight: '280px' }">
                <RouterView />
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
    justify-content: center;
    align-items: center;
}

.trigger:hover {
    color: #1890ff;
}

.icon-white {
  color: white;
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