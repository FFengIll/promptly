import type { NotificationArgsProps } from 'antd';
import { notification } from "antd";



type NotificationPlacement = NotificationArgsProps['placement'];

export const openNotification = (message: string, status: string) => {
    let placement: NotificationPlacement = 'bottomRight' as NotificationPlacement
    const [notificationApi, contextHolder] = notification.useNotification();

    console.log(message, status)

    notification[status]({
        message: `${status}`,
        description: message,
        placement,
        duration: 0
    });
};