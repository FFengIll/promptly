import React, { useEffect, useState } from 'react';
import { Card, Space, Input, Button, Divider, Modal, List, Typography } from 'antd';
import { EditFilled, SyncOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { backend } from "../scripts/backend";

const IndexView: React.FC = () => {
    const navigate = useNavigate();
    const [group, setGroup] = useState<Record<string, string[]>>({ "": [] });
    const [open, setOpen] = useState(false);
    const [sourceKey, setSourceKey] = useState("");
    const [targetKey, setTargetKey] = useState("");
    const [newName, setNewName] = useState("");
    const [newGroup, setNewGroup] = useState("");

    useEffect(() => {
        fetchList(false);
    }, []);

    const showModal = (item: string) => {
        setOpen(true);
        setSourceKey(item);
        setTargetKey(item);
    };

    const handleOk = () => {
        setOpen(false);
        backend.apiActionRenamePost({
            source: sourceKey,
            target: targetKey
        });
    };

    const openPrompt = (key: string) => {
        navigate(`/view/prompt/${key}`);
    };

    const create_profile = async (group: string, name: string) => {
        await backend.apiPromptPost({group: group}, name);
        fetchList(true);
    };

    const fetchList = async (refresh: boolean) => {
        try {
            const response = await backend.apiPromptGet(refresh);
            setGroup(response.data.data);
            console.log(response.data);
            return response.data;
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <Card title="Project List">
            <Space direction="horizontal">
                <Input 
                    value={newGroup}
                    onChange={(e) => setNewGroup(e.target.value)}
                    placeholder="group name"
                    size="large"
                />
                <Input 
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    placeholder="prompt name"
                    size="large"
                />
                <Button onClick={() => create_profile(newGroup, newName)}>
                    Create
                </Button>
                <Button onClick={() => fetchList(true)}>
                    <SyncOutlined />
                </Button>
            </Space>

            <Divider />

            {Object.entries(group).map(([key, values]) => (
                <Card key={key} title={key || '[default]'}>
                    <Space direction="horizontal">
                        <Input 
                            value={newName}
                            onChange={(e) => setNewName(e.target.value)}
                            placeholder="prompt name"
                        />
                        <Button onClick={() => create_profile(key, newName)}>
                            Create In Group
                        </Button>
                    </Space>

                    <Divider />
                    
                    <Modal
                        open={open}
                        title="Rename"
                        onOk={handleOk}
                        onCancel={() => setOpen(false)}
                    >
                        <p>source name: {sourceKey}</p>
                        <p>
                            target name:
                            <Input 
                                value={targetKey}
                                onChange={(e) => setTargetKey(e.target.value)}
                            />
                        </p>
                    </Modal>

                    <List
                        dataSource={[...values].sort()}
                        grid={{ gutter: 16, column: 4 }}
                        size="small"
                        renderItem={(item) => (
                            <List.Item>
                                <Space>
                                    <Button type="primary" onClick={() => showModal(item)}>
                                        <EditFilled />
                                    </Button>
                                    <Typography.Link 
                                        className="large-font"
                                        onClick={() => openPrompt(item)}
                                    >
                                        {item}
                                    </Typography.Link>
                                </Space>
                            </List.Item>
                        )}
                    />
                </Card>
            ))}
        </Card>
    );
};

export default IndexView;
