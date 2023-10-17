import type { Argument, ArgumentSetting, ModelSetting } from '@/sdk/models';
import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';

export const useConfigStore = defineStore('config', {
    getters: {},

    state: () => ({
        globalArgs: useLocalStorage('args',
            <ArgumentSetting>{}
        ),
        globalModels: useLocalStorage('models',
            <ModelSetting>{
                defaultModel: "gpt-3.5-turbo",
                models: [
                    // openai
                    "gpt-3.5-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo-instruct",

                    // openrouter
                    'anthropic/claude-instant-v1',

                    // special
                    "gpt-3.5-turbo-0613",
                    "gpt-4-0613",
                    'codellama-7b',
                ]
            }
        )
    })
    ,
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