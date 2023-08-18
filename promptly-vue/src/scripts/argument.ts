export interface Argument {
    key: string
    value: string
}

export class ArgumentHelper {
    static toArgumentList(args: Map<string, string>) {
        let items: Argument[] = []

        // map for each params are different
        args.forEach((value, key) => {
            let item = <Argument>{ key: key, value: value }
            items.push(item)
        })

        return items
    }
}