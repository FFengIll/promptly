<script setup lang="ts">
import {RouterView} from 'vue-router';
import {useRouter} from 'vue-router';
import {ref} from "vue";

import {MenuUnfoldOutlined, MenuFoldOutlined} from "@ant-design/icons-vue"

const router = useRouter()

const collapsed = ref(false)

function routerTo(key: string) {
    router.push(key)
}

</script>

<template>

    <a-layout theme="light">
        <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible>
            <div class="logo"/>

            <a-menu theme="dark" @click="(e) => routerTo(e.key)"
                    mode="inline"
                    :style="{ lineHeight: '64px' }">
                <a-menu-item key="/view/profile">Profile</a-menu-item>
                <a-menu-item key="/view/debug">Debug</a-menu-item>
                <a-menu-item key="/view/iteration">Iteration</a-menu-item>
                <a-menu-item key="/view/compare">Compare</a-menu-item>
            </a-menu>

            <!--                <a-menu v-model:selectedKeys="selectedKeys2" v-model:openKeys="openKeys" mode="inline"-->
            <!--                        :style="{ height: '100%', borderRight: 0 }">-->
            <!--                    <a-sub-menu key="sub1">-->
            <!--                        <template #title>-->
            <!--                      <span>-->
            <!--                          <user-outlined/>-->
            <!--                          subnav 1-->
            <!--                      </span>-->
            <!--                        </template>-->
            <!--                        <a-menu-item key="1">option1</a-menu-item>-->
            <!--                        <a-menu-item key="2">option2</a-menu-item>-->
            <!--                        <a-menu-item key="3">option3</a-menu-item>-->
            <!--                        <a-menu-item key="4">option4</a-menu-item>-->
            <!--                    </a-sub-menu>-->
            <!--                </a-menu>-->

        </a-layout-sider>

        <a-layout>
            <a-layout-header style="background: #fff; padding: 0">
                <menu-unfold-outlined
                    v-if="collapsed"
                    class="trigger"
                    @click="() => (collapsed = !collapsed)"
                />
                <menu-fold-outlined
                    v-else class="trigger"
                    @click="() => (collapsed = !collapsed)"/>

            </a-layout-header>

            <a-layout-content
                :style="{ margin: '24px 16px', padding: '24px', background: '#fff', minHeight: '280px' }">
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