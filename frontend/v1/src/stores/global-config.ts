import type { Argument, ArgumentSetting, ModelSetting } from '@/sdk/models';
import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';

export const useConfigStore = defineStore('config', {
    state: () => ({
        globalArgs: useLocalStorage('args',
            <ArgumentSetting>{}
        ),
        globalModels: useLocalStorage('models',
            <ModelSetting>{
                defaultModel: "gpt-3.5-turbo",
                models: [],
            }
        )
    }),
    actions: {
        updateModels(setting: ModelSetting) {
            this.$patch(
                {
                    globalModels: setting
                }
            )
        },
        updateArgs(args: Argument[]) {
            this.$patch(
                {
                    globalArgs: { args: args }
                }
            )
        },
    },
})