import * as defaultApi from "../sdk/api";
import type { Argument, LLMOption, Message } from "../sdk";
import { format } from "./template";


function ApiFactory() {
    const baseURL = import.meta.env.VITE_BASE_API
    return defaultApi.DefaultApiFactory(undefined, baseURL)
}

export const backend = ApiFactory()

export class BackendHelper {
    static replace(messages: Message[], args: Argument[]) {
        const another: Message[] = JSON.parse(JSON.stringify(messages))
        another.forEach((item) => {
            item.content = format(item.content, args)
            console.log(item.content)
        })
        return another
    }

    static async doChat(options: LLMOption, messages: Message[], args: Argument[],) {

        console.log("origin message", messages)
        console.log("origin argument", args)
        console.log("origin options", options)

        const enables = messages?.filter((item: Message) => item.enable)

        const another: Message[] = BackendHelper.replace(enables, args)
        console.log("will chat with messages", another)

        return backend.apiActionChatPost({
            messages: another,
            options: options
        })
    }
}
