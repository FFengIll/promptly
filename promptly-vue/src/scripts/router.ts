import router from "@/router";

export class RouteHelper {
    static toAdvance(key: string) {
        router.push(`/view/prompt/${key}/advance`)
    }

    static toDev(key: string) {
        router.push(`/view/prompt/${key}`)
    }
}

