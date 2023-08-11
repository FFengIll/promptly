import router from "@/router";

export class RouteHelper {
    static toPrompt(key: string) {
        console.log('to prompt', key)
        router.push(`/view/prompt/${key}`)
    }

    static toCommit(key: string) {
        router.push(`/view/commit/${key}`)
    }

    static toTesting(key: string) {
        router.push('/view/testing')
    }
}

