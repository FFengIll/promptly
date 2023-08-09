import {DefaultApiFactory} from "../../sdk/apis/default-api";

export function ApiFactory() {
    return DefaultApiFactory(undefined, "http://localhost:8000")
}
