<script setup lang="ts">
import { RouterView } from 'vue-router';
import type { CSSProperties } from 'vue';
import 'ant-design-vue/dist/reset.css';

import { useRouter } from 'vue-router';

const router = useRouter()

const headerStyle: CSSProperties = {
    textAlign: 'center',
    color: '#fff',
    height: 64,
    paddingInline: 50,
    lineHeight: '64px',
    backgroundColor: '#7dbcea',
};

const contentStyle: CSSProperties = {
    // textAlign: 'center',
    // minHeight: 120,
    // lineHeight: '120px',
    // color: '#fff',
    // backgroundColor: '#108ee9',
};

const siderStyle: CSSProperties = {
    // textAlign: 'center',
    // lineHeight: '120px',
    // color: '#fff',
    // backgroundColor: '#3ba0e9',
    width: "200",
    backgroundColor: "#fff"
};

const footerStyle: CSSProperties = {
    // textAlign: 'center',
    // color: '#fff',
    // backgroundColor: '#7dbcea',
};

function routerTo(key: string) {
    router.push(key)
}

</script>

<template>
    <a-layout class="layout">
        <a-layout-header>
            <div class="logo"></div>
            <a-menu theme="dark" @click="(e) => routerTo(e.key)" mode="horizontal" :style="{ lineHeight: '64px' }">
                <a-menu-item key="/view/profile">Profile</a-menu-item>
                <a-menu-item key="/view/debug">Debug</a-menu-item>
                <a-menu-item key="/view/compare">Compare</a-menu-item>
            </a-menu>
        </a-layout-header>

        <a-layout>
            <!-- <a-layout-sider :style="siderStyle">
                <a-menu v-model:selectedKeys="selectedKeys2" v-model:openKeys="openKeys" mode="inline"
                    :style="{ height: '100%', borderRight: 0 }">
                    <a-sub-menu key="sub1">
                        <template #title>
                            <span>
                                <user-outlined />
                                subnav 1
                            </span>
                        </template>
                        <a-menu-item key="1">option1</a-menu-item>
                        <a-menu-item key="2">option2</a-menu-item>
                        <a-menu-item key="3">option3</a-menu-item>
                        <a-menu-item key="4">option4</a-menu-item>
                    </a-sub-menu>
                </a-menu>

            </a-layout-sider> -->
            <a-layout-content :style="contentStyle">
                <RouterView />
            </a-layout-content>
        </a-layout>
        <!-- <a-layout-footer :style="footerStyle">Footer</a-layout-footer> -->
    </a-layout>
</template>

<style scoped>
.site-layout-content {
    min-height: 280px;
    padding: 24px;
    background: #fff;
}

#components-layout-demo-top .logo {
    float: left;
    width: 120px;
    height: 31px;
    margin: 16px 24px 16px 0;
    background: rgba(255, 255, 255, 0.3);
}

.ant-row-rtl #components-layout-demo-top .logo {
    float: right;
    margin: 16px 0 16px 24px;
}

[data-theme='dark'] .site-layout-content {
    background: #141414;
}
</style>