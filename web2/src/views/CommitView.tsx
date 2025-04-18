import { HeartOutlined, HeartTwoTone } from '@ant-design/icons';
import { Button, Card, Checkbox, Col, Divider, Input, Row, Space, Typography } from 'antd';
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { useParams } from 'react-router-dom';
import ArgumentPanel from '../components/ArgumentPanel';
import PromptInput from "../components/PromptInput";
import { backend, BackendHelper } from "../scripts/backend";
import { openNotification } from "../scripts/notice";
import { useConfigStore } from "../stores/global";

import type { Argument, ArgumentSetting, CommitItem, UpdatePromptBody } from "../sdk/models";

const { Text } = Typography;

export const CommitView: React.FC = () => {
    const store = useConfigStore();
    const { key } = useParams();

    const [autoSave, setAutoSave] = useState(true);
    const [starOnly, setStarOnly] = useState(false);
    const [simpleModel, setSimpleModel] = useState(true);
    const [commits, setCommits] = useState<CommitItem[]>([]);
    const [argSetting, setArgSetting] = useState<ArgumentSetting>({
        name: "",
        args: []
    });
    const [args, setArgs] = useState<Argument[]>([]);

    useEffect(() => {
        backend.apiPromptArgsNameGet(key!)
            .then(response => {
                setArgSetting(response.data);
                console.log('setting', response.data);
            });
        getCommit(key!);
    }, [key]);

    const getCommit = async (name: string) => {
        try {
            const response = await backend.apiCommitsNameGet(name);
            const filteredCommits = response.data.filter((item: CommitItem) => item.messages.length > 0);
            setCommits(filteredCommits);

            if (filteredCommits.length <= 0) {
                const promptResponse = await backend.apiPromptNameGet(name);
                setCommits([{
                    messages: promptResponse.data.messages
                }]);
            }
        } catch (error) {
            console.log(error);
        }
    };

    const saveCommits = async (key: string, data: CommitItem[]) => {
        try {
            await backend.apiCommitsNamePut(data, key);
            console.log("success");
        } catch (error) {
            console.log(error);
        }
    };

    const dropCommit = (commit: CommitItem, index: number) => {
        if (commit.star) return;
        const newCommits = [...commits];
        newCommits.splice(index, 1);
        setCommits(newCommits);
    };

    const replay = async (commit: CommitItem) => {
        const updatedCommit = { ...commit, response: "" };
        const response = await BackendHelper.doChat(commit.options!, commit.messages, commit.args!);
        updatedCommit.response = response.data;

        const newCommits = commits.map(c =>
            c === commit ? updatedCommit : c
        );
        setCommits(newCommits);
    };

    const doChat = async (commit: CommitItem) => {
        try {
            const updatedCommit = { ...commit, response: "" };
            const response = await BackendHelper.doChat(commit.options!, commit.messages, args);
            updatedCommit.response = response.data;

            const newCommits = commits.map(c =>
                c === commit ? updatedCommit : c
            );
            setCommits(newCommits);
        } catch (err) {
            openNotification(err.toString(), 'error');
        }
    };

    const gotoPrompt = async (commit: CommitItem) => {
        const body: UpdatePromptBody = {
            messages: commit.messages,
            args: args
        };
        try {
            RouteHelper.toPrompt(key!);
            await backend.apiPromptNamePut(body, key!);
        } catch (err) {
            openNotification(err.toString(), 'error');
        }
    };

    const changeStar = async (commit: CommitItem) => {
        const value = !commit.star;
        try {
            await backend.apiActionStarPost({
                name: key!,
                md5: commit.md5!,
                value
            });
            const newCommits = commits.map(c =>
                c === commit ? { ...c, star: value } : c
            );
            setCommits(newCommits);
        } catch (err) {
            openNotification(err.toString(), 'error');
        }
    };

    const selectArg = (key: string, value: string) => {
        setArgs(prevArgs => {
            const existingArgIndex = prevArgs.findIndex(item => item.key === key);
            if (existingArgIndex !== -1) {
                const newArgs = [...prevArgs];
                newArgs[existingArgIndex] = { ...newArgs[existingArgIndex], value };
                return newArgs;
            }
            return [...prevArgs, { key, value }];
        });
    };

    return (
        <>
            <Row gutter={[16, 16]}>
                <Col span={10} className="gutter-row">
                    <Space direction="vertical">
                        <Space>
                            <Space.Compact>
                                <Button type="primary" onClick={() => getCommit(key!)}>Refresh</Button>
                                <Button type="primary" onClick={() => saveCommits(key!, commits)}>Save</Button>
                            </Space.Compact>
                            <Checkbox checked={autoSave} onChange={e => setAutoSave(e.target.checked)}>Auto Save</Checkbox>
                            <Divider type="vertical" />
                            <Checkbox checked={starOnly} onChange={e => setStarOnly(e.target.checked)}>Star Only</Checkbox>
                            <Checkbox checked={simpleModel} onChange={e => setSimpleModel(e.target.checked)}>Simple</Checkbox>
                        </Space>
                    </Space>
                </Col>

                <Col span={10}>
                    <ArgumentPanel setting={argSetting} args={args} onSelect={selectArg} />
                </Col>
            </Row>

            <Divider />

            <Row gutter={[16, 16]}>
                {commits.map((commit, index) => (
                    ((starOnly && commit.star) || !starOnly) && (
                        <Col span={8} key={index}>
                            <Card>
                                {!simpleModel && (
                                    <>
                                        <Space>
                                            <Button onClick={() => doChat(commit)}>Request</Button>
                                            <Button onClick={() => replay(commit)}>Replay</Button>
                                            <Button onClick={() => gotoPrompt(commit)}>Goto Prompt</Button>
                                            <Button onClick={() => dropCommit(commit, index)}>Drop</Button>
                                        </Space>
                                        <Divider />
                                    </>
                                )}

                                <Card title="Args">
                                    <Space>
                                        {commit.args?.map((item, idx) => (
                                            <React.Fragment key={idx}>
                                                <Text>{item.key}</Text>
                                                <Input value={item.value} />
                                            </React.Fragment>
                                        ))}
                                    </Space>
                                </Card>
                                <Divider />

                                <Card
                                    title={commit.options?.model}
                                    className="highlight-ant-card-head"
                                    extra={
                                        <Button onClick={() => changeStar(commit)}>
                                            {commit.star ?
                                                <HeartTwoTone twoToneColor="#eb2f96" /> :
                                                <HeartOutlined />
                                            }
                                        </Button>
                                    }
                                >
                                    <Text>Request Timecost: {(commit.timecost ?? 0) / 1000} seconds</Text>
                                    <Divider />
                                    <div style={{ height: '100px', overflowY: 'scroll' }}>
                                        <ReactMarkdown>{commit.response || ''}</ReactMarkdown>
                                    </div>
                                </Card>
                                <Divider />

                                <PromptInput
                                    title="Prompt"
                                    messages={commit.messages!}
                                    withCopy
                                    withSidebar
                                    withEnable={simpleModel}
                                />
                            </Card>
                        </Col>
                    )
                ))}
            </Row>

            <style>
                {`
                    .highlight-ant-card-head {
                        background-color: #2feb55b6;
                    }
                    .ant-card-head {
                        background-color: #2feb55;
                    }
                `}
            </style>
        </>
    );
};

export default CommitView;
