import { useLocalStorage } from "@vueuse/core"
import { defineStore } from 'pinia'
import type { Message } from '../../sdk/models/message.js'

export const useCounterStore = defineStore('counter', {
    state: () => {
        return { count: 0 }
    },
    // 也可以这样定义
    // state: () => ({ count: 0 })
    actions: {
        increment() {
            this.count++
        },
    },
})

export const useSnapshotStore = defineStore('snapshot', {
    state: () => {
        return {
            snapshot:{
            messages: [
                {
                    id: 1,
                    role: 'user',
                    content: "{{}}"
                }
            ]
        },
        debug:  useLocalStorage('debug', [
                {
                    id: 1,
                    role: 'user',
                    content: "{{}}"
                },
               
            ]),
        compare:{
            left: [
                {
                    id: 1,
                    role: 'user',
                    content: "test"
                }
            ],
            right: [
                {
                    id: 1,
                    role: 'user',
                    content: "test"
                }
            ]
        }

        }
    },
    actions: {
        sendToDebug(ms:Message[]) {
            var res  = ms.filter(item => {
                return item.enable
            });
            this.debug =  res
        },
        sendToCompareLeft(ms:Message[]) {
            // var res  = ms.filter(item => {
            //     return item.enable
            // });
            var res = ms
            this.compare.right =  res
        },
        sendToCompareRight(ms:Message[]) {
            // var res  = ms.filter(item => {
            //     return item.enable
            // });
            var res = ms
            this.compare.right =  res
        },
    },
})