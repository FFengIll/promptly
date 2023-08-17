import type {Argument} from '@/scripts/models.ts'

export function format(template: string, args: Argument[]) {
    var res = template

    args.forEach(item => {
        res = res.replace("${" + item.key + "}", item.value!!)
    })

    return res
}