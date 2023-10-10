import type { Argument, Message } from "@/sdk/models";
import * as defaultApi from "@/sdk/api";
import { format } from "./template";


function ApiFactory() {
    let baseURL = import.meta.env.VITE_BASE_API
    return defaultApi.DefaultApiFactory(undefined, baseURL)
}

export const backend = ApiFactory()

export class BackendHelper {
    static replace(messages: Message[], args: Argument[]) {
        let another: Message[] = JSON.parse(JSON.stringify(messages))
        another.forEach((item) => {
            item.content = format(item.content, args)
            console.log(item.content)
        })
        return another
    }

    static async doChat(model: string, messages: Message[], args: Argument[],) {

        console.log("origin message", messages)
        console.log("origin argument", args)

        let enables = messages?.filter((item: Message) => item.enable)

        let another = BackendHelper.replace(enables, args)
        console.log("will chat with messages", another)

        return backend.apiActionChatPost(another, model)
    }
}
