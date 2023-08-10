import type { Argument, Message } from "sdk/models";
import * as defaultApi from "../../sdk/apis/default-api";
import { format } from "./template";

export function ApiFactory() {
    return defaultApi.DefaultApiFactory(undefined, "http://localhost:8000")
}


const api = ApiFactory()

export class ApiHelper {
    static async doChat(key: string, messages: Message[], args: Argument[]) {
        return await api.apiCommitArgsPost(args, key)
            .then(
                (response) => {

                    console.log(messages)

                    let ms = messages?.filter((item: Message) => item.enable)

                    let another: Message[] = JSON.parse(JSON.stringify(ms))
                    another.forEach((item) => {
                        item.content = format(item.content, args)
                    })
                    console.log("will chat with messages", another)

                    return api.apiChatPost(another).then(
                        (response) => {
                            return response
                        }
                    )
                }
            )
    }
}