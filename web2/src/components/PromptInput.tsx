import React, { useState } from 'react';
import {
    CloseOutlined,
    DownOutlined,
    PlusOutlined,
    UpOutlined,
} from '@ant-design/icons';
import { Button, Divider, Popconfirm, Radio, Switch, Space, Typography, Row, Col, Input } from 'antd';

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
        <div>
            {messages.map((item, index) => (
                <div key={index}>
                    {(withEnable && item.enable) || !withEnable ? (
                        <Row>
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
                                <Space direction="vertical">
                                    {!withSidebar && (
                                        <Radio.Group
                                            value={item.role}
                                            onChange={(e) => setSelectedRole(e.target.value)}
                                            buttonStyle="solid"
                                        >
                                            <Radio.Button value="user">User</Radio.Button>
                                            <Radio.Button value="system">System</Radio.Button>
                                            <Radio.Button value="assistant">Assistant</Radio.Button>
                                        </Radio.Group>
                                    )}
                                </Space>
                                <Divider type="vertical" />
                                <Space direction="horizontal">
                                    {withSidebar && (
                                        <Button style={color(item.role)}>
                                            {item.role}
                                        </Button>
                                    )}
                                    {withControl && (
                                        <>
                                            <Typography.Text>Enable</Typography.Text>
                                            <Switch
                                                checked={item.enable}
                                                onChange={(checked) => {
                                                    item.enable = checked;
                                                }}
                                            />
                                        </>
                                    )}
                                    {withCopy && (
                                        <Button onClick={() => handleCopy(JSON.stringify(item.content))}>
                                            Copy JSON
                                        </Button>
                                    )}
                                </Space>
                            </Row>
                            <Row gutter={12} align="middle">
                                <Col span={24}>
                                    <Input.TextArea
                                        disabled={!item.enable}
                                        value={item.content}
                                        onChange={(e) => {
                                            item.content = e.target.value;
                                        }}
                                        autoSize={{ minRows: 3, maxRows: 5 }}
                                        placeholder="textarea with clear icon"
                                    />
                                </Col>
                            </Row>
                        </Row>
                    ) : null}
                </div>
            ))}
        </div>
    );
};

export default PromptInput;
