import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';
import type { ArgumentOutput as Argument, ArgumentSetting } from '../../sdk/models';

export const useConfigStore = defineStore('config', {
    getters: {},

    state: () => ({
        globalArgs: useLocalStorage('args',
            <ArgumentSetting>{

            }
        ),
    })
    ,
    actions: {
        updateArgs(args: Argument[]) {
            this.$patch(
                {
                    globalArgs: { args: args }
                }
            )
        },
    },
})