export function format(template: string, kv: { key: string, value: string }[]) {
    var res = template

    kv.forEach(item => {
        console.log('replace with', item)
        res = res.replace("${" + item.key + "}", item.value)
    })

    console.log(res)

    return res
}