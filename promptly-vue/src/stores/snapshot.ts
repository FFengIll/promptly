import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';
import type { Argument, Message } from '../../sdk/models';

export const useSnapshotStore = defineStore('snapshot', {
    getters: {},

    state: () => ({
        source: useLocalStorage('source',
            {
                name: "",
                messages: <Message[]>[],
                args: <Argument[]>[]
            }),
    })
    ,
    actions: {
        async sendSource(source: string, ms: Message[], args: Argument[]) {
            this.$patch(
                {
                    source: {
                        messages: ms,
                        name: source,
                        args: args,
                    }
                }
            )
        },
    },
})