import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';
import type { Message } from '../../sdk/models';

export const useSnapshotStore = defineStore('snapshot', {
    getters: {

    },

    state: () => ({
        source: useLocalStorage('source',
            {
                name: "",
                messages: <Message[]>[

                ]
            }),
    })
    ,
    actions: {
        sendSource(ms: Message[], source: string) {
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

        // sendToCompareLeft(ms: Message[]) {
        //     // var res  = ms.filter(item => {
        //     //     return item.enable
        //     // });
        //     var res = ms
        //     this.compare.right.messages = res
        // },
        // sendToCompareRight(ms: Message[]) {
        //     // var res  = ms.filter(item => {
        //     //     return item.enable
        //     // });
        //     var res = ms
        //     this.compare.right.messages = res
        // },
    },
})