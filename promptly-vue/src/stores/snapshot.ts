import {useLocalStorage} from '@vueuse/core';
import {defineStore} from 'pinia';
import type {Argument, Message} from '../../sdk/models';

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
        sendSource(source: string, ms: Message[], args: Argument[]) {
            var res = ms.filter(item => {
                return item.enable
            });
            this.$patch(
                {
                    source: {
                        messages: res,
                        name: source
                    }
                }
            )
        },
    },
})