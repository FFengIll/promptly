import type {Argument, Message} from "sdk/models";
import * as defaultApi from "../../sdk/apis/default-api";
import {format} from "./template";

export function ApiFactory() {
    let baseURL = import.meta.env.VITE_BASE_API
    return defaultApi.DefaultApiFactory(undefined, baseURL)
}

const api = ApiFactory()

export class ApiHelper {
    static async doChat(key: string, messages: Message[], args: Argument[]) {

        console.log("origin message", messages)
        console.log("origin argument", args)

        let ms = messages?.filter((item: Message) => item.enable)

        let another: Message[] = JSON.parse(JSON.stringify(ms))
        another.forEach((item) => {
            item.content = format(item.content, args)
            console.log(item.content)
        })
        console.log("will chat with messages", another)

        return api.apiChatPost(another).then(
            (response) => {
                return response
            }
        )

    }
}
