import type { Argument } from "@/sdk/models"

export function format(template: string, args: Argument[]) {
    var res = template

    args.forEach(item => {
        if (item.value!!.length > 0) {
            res = res.replace("${" + item.key + "}", item.value!!)
        }
    })

    return res
}