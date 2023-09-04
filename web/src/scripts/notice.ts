import { notification, type NotificationPlacement } from "ant-design-vue";
import type { NotificationInstance } from "ant-design-vue/es/notification";

const [notificationApi, contextHolder] = notification.useNotification();


export const openNotification = (api: NotificationInstance, message: string, status: string) => {
    let placement: NotificationPlacement = 'bottomRight' as NotificationPlacement

    console.log(message, status)

    notification[status]({
        message: `${status}`,
        description: message,
        placement,
        duration: 0
    });
};