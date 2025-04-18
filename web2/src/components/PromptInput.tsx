import {
    CloseOutlined,
    CopyOutlined,
    DownOutlined,
    PlusOutlined,
    UpOutlined,
} from '@ant-design/icons';
import { Button, Divider, Input, Popconfirm, Radio, Row, Space, Switch } from 'antd';
import React, { useState } from 'react';

interface Message {
    role: string;
    content: string;
    enable: boolean;
}

interface Props {
    messages: Message[];
    withControl?: boolean;
    withCopy?: boolean;
    withSidebar?: boolean;
    title?: string;
    withEnable?: boolean;
    setMessages: (messages: Message[]) => void;
    onOrderUp: (index: number) => void;
    onOrderDown: (index: number) => void;
    onRemove: (index: number) => void;
    onAdd: (index: number) => void;
}

const PromptInput: React.FC<Props> = ({
    messages,
    withControl = false,
    withCopy = false,
    withSidebar = false,
    title = '',
    withEnable = false,
    setMessages,
    onOrderUp,
    onOrderDown,
    onRemove,
    onAdd,
}) => {
    const [selectedRole, setSelectedRole] = useState<string>('');

    const color = (role: string) => {
        switch (role) {
            case 'user':
                return { color: 'blue' };
            case 'system':
                return { color: 'red' };
            case 'assistant':
                return { color: 'black' };
            default:
                return {};
        }
    };

    const handleCopy = (content: string) => {
        navigator.clipboard.writeText(content).then(() => {
            alert('Content copied to clipboard');
        });
    };

    const dragData = () => {
        return messages.map((_, index) => index);
    };

    return (
        <>
            {messages.map((item, index) => (
                <div key={index}>
                    {(withEnable && item.enable) || !withEnable ? (
                        <>
                            {withControl && (
                                <Divider>
                                    <Space>
                                        <Button onClick={() => onAdd(index)}>
                                            <PlusOutlined />
                                        </Button>
                                        <Divider type="vertical" />
                                        <Button
                                            type="primary"
                                            shape="round"
                                            onClick={() => onOrderUp(index)}
                                        >
                                            <UpOutlined />
                                        </Button>
                                        <Button
                                            type="primary"
                                            shape="round"
                                            onClick={() => onOrderDown(index)}
                                        >
                                            <DownOutlined />
                                        </Button>
                                        <Divider type="vertical" />
                                        <Popconfirm
                                            title="Are you sure delete this task?"
                                            onConfirm={() => onRemove(index)}
                                            okText="Yes"
                                            cancelText="No"
                                        >
                                            <Button>
                                                <CloseOutlined />
                                            </Button>
                                        </Popconfirm>
                                    </Space>
                                </Divider>
                            )}
                            <Row>
                                <Space direction="horizontal" style={{ width: '100%', display: 'flex', justifyContent: 'space-between' }}>
                                    <div>
                                        {!withSidebar && (
                                            <Radio.Group
                                                value={item.role}
                                                onChange={(e) => {
                                                    const updatedMessages = [...messages];
                                                    updatedMessages[index].role = e.target.value;
                                                    setMessages(updatedMessages);
                                                }}
                                                buttonStyle="solid"
                                            >
                                                <Radio.Button value="user">User</Radio.Button>
                                                <Radio.Button value="system">System</Radio.Button>
                                                <Radio.Button value="assistant">Assistant</Radio.Button>
                                            </Radio.Group>
                                        )}
                                    </div>

                                    {withSidebar && (
                                        <Button style={color(item.role)}>
                                            {item.role}
                                        </Button>
                                    )}

                                    <Divider type="vertical" />

                                    <div>

                                        {withCopy && (
                                            <Button
                                                onClick={() => handleCopy(JSON.stringify(item.content))}
                                                icon={<CopyOutlined />}
                                            />
                                        )}

                                        <Divider type="vertical" />

                                        {withControl && (
                                            <Switch
                                                checked={item.enable}
                                                onChange={(checked) => {
                                                    const updatedMessages = [...messages];
                                                    updatedMessages[index].enable = checked;
                                                    setMessages(updatedMessages);
                                                }}
                                                checkedChildren="Enable"
                                                unCheckedChildren="Disable"
                                            />
                                        )}

                                        <Divider type="vertical" />

                                        <Switch
                                            checked={item.maxRows === item.content.split('\n').length}
                                            onChange={(checked) => {
                                                const updatedMessages = [...messages];
                                                updatedMessages[index].maxRows = checked
                                                    ? item.content.split('\n').length
                                                    : 5;
                                                setMessages(updatedMessages);
                                            }}
                                            checkedChildren="Expanded"
                                            unCheckedChildren="Collapsed"
                                        />
                                    </div>
                                </Space>
                            </Row>
                            <Row gutter={12} align="middle">
                                <Input.TextArea
                                    disabled={!item.enable}
                                    value={item.content}
                                    onChange={(e) => {
                                        const updatedMessages = [...messages];
                                        updatedMessages[index].content = e.target.value;
                                        setMessages(updatedMessages);
                                    }}
                                    autoSize={{ minRows: 3, maxRows: item.maxRows ? item.maxRows : 5 }}
                                    placeholder="textarea with clear icon"
                                    style={{ width: '100%' }}
                                />
                            </Row>
                        </>
                    ) : null}
                </div >
            ))}
        </>
    );
};

export default PromptInput;
