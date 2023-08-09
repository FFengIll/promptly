import {defineStore} from 'pinia'
import type {Message} from '../../sdk/models'

export const useSnapshotStore = defineStore('snapshot', {
    state: () => {
        return {
            source: {
                name: "",
                messages: <Message[]>[
                    {
                        id: 1,
                        role: 'user',
                        content: "{{}}"
                    },
                ]
            },
            compare: {
                left: {
                    name: "",
                    messages: <Message[]>[
                        {
                            id: 1,
                            role: 'user',
                            content: "test"
                        }
                    ]
                },
                right: {
                    name: "",
                    messages: <Message[]>[
                        {
                            id: 1,
                            role: 'user',
                            content: "test"
                        }
                    ]
                }
            }

        }
    },
    actions: {
        sendSource(ms: Message[], source: string) {
            var res = ms.filter(item => {
                return item.enable
            });
            this.source.messages = res
            this.source.name = source
        },

        sendToCompareLeft(ms: Message[]) {
            // var res  = ms.filter(item => {
            //     return item.enable
            // });
            var res = ms
            this.compare.right.messages = res
        },
        sendToCompareRight(ms: Message[]) {
            // var res  = ms.filter(item => {
            //     return item.enable
            // });
            var res = ms
            this.compare.right.messages = res
        },
    },
})