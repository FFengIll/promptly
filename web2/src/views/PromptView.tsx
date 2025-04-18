import {
    PlusOutlined,
    SyncOutlined
} from '@ant-design/icons';
import {
    Button,
    Card,
    Col,
    Collapse,
    Divider,
    Input,
    InputNumber,
    List,
    Row,
    Select,
    Skeleton,
    Space,
    Switch,
    Tabs,
    Typography
} from 'antd';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useParams } from 'react-router-dom';

// Assuming these components would be created separately
import ArgumentPanel from '../components/ArgumentPanel';
import ModelSelect from '../components/ModelSelect';
import PromptInput from '../components/PromptInput';

// Utility functions that would replace the Vue backend and notification services
import { backend, BackendHelper } from '../scripts/backend';
import { openNotification } from '../scripts/notice';
import { useConfigStore } from '../stores/global';

const { Title } = Typography;
const { Panel } = Collapse;
const { TabPane } = Tabs;
const { Option } = Select;

// CSS classes
const styles = {
    scrollShort: {
        height: '200px',
        overflow: 'auto',
    }
};

function PromptView() {
    const { key } = useParams();
    const store = useConfigStore();

    // State variables
    const [loading, setLoading] = useState(false);
    const [model, setModel] = useState("");
    const [timecost, setTimecost] = useState(0);
    const [description, setDescription] = useState("");
    const [withEmbed, setWithEmbed] = useState(false);
    const [argValue, setArgValue] = useState("");
    const [argKey, setArgKey] = useState("");
    const [response, setResponse] = useState("test");
    const [responseMode, setResponseMode] = useState("1");
    const [argSetting, setArgSetting] = useState({ name: "", args: [] });
    const [args, setArgs] = useState([]);
    const [prompt, setPrompt] = useState({ messages: [] });
    const [options, setOptions] = useState({});

    // Effects
    useEffect(() => {
        fetchPrompt(key);
    }, [key]);

    // Methods
    const copy = (text) => {
        navigator.clipboard.writeText(text).then(() => {
            openNotification('Copied to clipboard', 'success');
        }).catch(err => {
            openNotification('Failed to copy: ' + err, 'error');
        });
    };

    const reloadModels = async () => {
        try {
            const res = await backend.apiGlobalModelsGet();
            store.setGlobalModels(res.data);
        } catch (err) {
            openNotification(err.toString(), 'error');
        }
    };

    const updatePreferModel = (modelName) => {
        const newOptions = { ...options, prefer: modelName };
        setOptions(newOptions);

        const body = { options: newOptions };
        backend.apiPromptNamePut(body, prompt.name)
            .catch(err => {
                openNotification(err, 'error');
            });
    };

    const selectArg = (key, value) => {
        const newArgs = [...args];
        const existingArg = newArgs.find(item => item.key === key);

        if (existingArg) {
            existingArg.value = value;
        } else {
            newArgs.push({ key, value, candidates: [] });
        }

        setArgs(newArgs);
    };

    const newArg = async () => {
        if (argKey === "" || argValue === "") {
            return;
        }

        const body = {
            key: argKey,
            value: argValue
        };

        try {
            await backend.apiPromptArgsNamePut(body, key);
            selectArg(argKey, argValue);
            await fetchArgument(key);
        } catch (err) {
            openNotification(err.toString(), "error");
        }
    };

    const responseToPrompt = () => {
        addPrompt(prompt.messages.length, 'assistant', response);
    };

    const deletePrompt = (index) => {
        const newMessages = [...prompt.messages];
        newMessages.splice(index, 1);
        setPrompt({ ...prompt, messages: newMessages });
    };

    const doCommit = async () => {
        const body = {
            name: key,
            commit: {
                messages: prompt.messages,
                response,
                args,
                options,
                timecost,
            },
        };

        try {
            await backend.apiCommitPost(body);
        } catch (err) {
            openNotification(err.toString(), "error");
        }
    };

    const addPrompt = (index, role, content) => {
        const newMessages = [...prompt.messages];
        const newMessage = { content, role, enable: true };

        let insertIndex = index;
        while (insertIndex > 0 && newMessages[insertIndex - 1].role === 'system') {
            insertIndex -= 1;
        }

        newMessages.splice(insertIndex, 0, newMessage);
        setPrompt({ ...prompt, messages: newMessages });
    };

    const order = (index, delta) => {
        const anotherIndex = index + delta;
        if (anotherIndex < 0 || anotherIndex >= prompt.messages.length) {
            return;
        }

        const newMessages = [...prompt.messages];
        const temp = newMessages[index];
        newMessages[index] = newMessages[anotherIndex];
        newMessages[anotherIndex] = temp;

        setPrompt({ ...prompt, messages: newMessages });
    };

    const fetchArgument = async (name) => {
        try {
            const response = await backend.apiPromptArgsNameGet(name);
            setArgSetting(response.data);
        } catch (err) {
            openNotification(err.toString(), "error");
        }
    };

    const fetchPrompt = async (name) => {
        try {
            await fetchArgument(name);

            const response = await backend.apiPromptNameGet(name);
            const promptData = response.data;

            setPrompt(promptData);
            setDescription(promptData.description || "");
            setArgs(promptData.args || []);
            setOptions(promptData.options || {});
            setModel(promptData.options?.model || "");

            const hasEmbed = promptData.plugins?.includes('embed');
            setWithEmbed(hasEmbed);
        } catch (err) {
            openNotification(err.toString(), "error");
        }
    };

    const reload = () => {
        fetchPrompt(key);
    };

    const update = async () => {
        const body = {
            messages: prompt.messages,
            args: args,
            options: options,
            description: description,
        };

        try {
            await backend.apiPromptNamePut(body, key);
        } catch (err) {
            openNotification(err.toString(), "error");
        }
    };

    const chat = async () => {
        if (withEmbed) {
            await chatWithRAG();
        } else {
            await chatWithPrompt();
        }
    };

    const chatWithRAG = async () => {
        try {
            const messages = prompt.messages;

            const body = {
                messages: prompt.messages,
                options: options,
                args: args,
                plugins: ['embed']
            };

            await backend.apiPromptNamePut(body, key);

            setLoading(true);
            setResponse('');

            const res = await backend.apiActionRetrieveGeneratePost({
                name: key,
                messages: messages.filter(item => item.enable)
            });

            setResponse(res.data);
        } catch (err) {
            openNotification(err.toString(), "error");
        } finally {
            setLoading(false);
        }
    };

    const chatWithPrompt = async () => {
        try {
            const body = {
                messages: prompt.messages,
                args: args,
                options: options,
            };

            await backend.apiPromptNamePut(body, key);

            setLoading(true);
            setResponse('');

            const newOptions = { ...options, model };
            setOptions(newOptions);

            const start = new Date().getTime();
            const res = await BackendHelper.doChat(newOptions, prompt.messages, args);
            const end = new Date().getTime();

            setResponse(res.data);
            setTimecost(end - start);
        } catch (err) {
            openNotification(err.toString(), "error");
        } finally {
            setLoading(false);
        }
    };

    const handleEmbedChange = (checked) => {
        setWithEmbed(checked);
        if (checked) {
            const plugins = prompt.plugins || [];
            if (!plugins.includes('embed')) {
                const newPlugins = [...plugins, 'embed'];
                setPrompt({ ...prompt, plugins: newPlugins });
            }
        }
    };

    return (
        <div>
            <Space align="center" style={{ width: '100%' }}>
                <Title>{key}</Title>
                <Space direction="horizontal" align="baseline">
                    <Button onClick={reload}>
                        <SyncOutlined />
                    </Button>
                    <Divider type="vertical" />
                </Space>
            </Space>
            <Space>
                <Input style={{ width: 400 }} value={description} onChange={e => setDescription(e.target.value)} />
            </Space>

            <Row gutter={6}>
                <Col span={12}>
                    <Card
                        title="Replace Args"
                        extra={
                            <Button onClick={() => fetchArgument(key)}>
                                <SyncOutlined />
                            </Button>
                        }
                    >
                        <ArgumentPanel
                            setting={argSetting}
                            args={args}
                            onSelect={selectArg}
                            extra={
                                <Space direction="horizontal">
                                    <Select
                                        value={argKey}
                                        style={{ width: 120 }}
                                        showSearch
                                        onChange={value => setArgKey(value)}
                                    >
                                        {args.map(arg => (
                                            <Option key={arg.key} value={arg.key}>{arg.key}</Option>
                                        ))}
                                    </Select>
                                    <Input
                                        value={argKey}
                                        placeholder="key"
                                        onChange={e => setArgKey(e.target.value)}
                                    />
                                    <Input
                                        value={argValue}
                                        placeholder="value"
                                        onChange={e => setArgValue(e.target.value)}
                                    />
                                    <Button onClick={newArg}>
                                        <PlusOutlined />
                                        New
                                    </Button>
                                </Space>
                            }
                        />
                    </Card>

                    <Card
                        title="Prompt"
                        extra={
                            <Space>
                                <Button onClick={() => copy(JSON.stringify({
                                    name: key,
                                    prompt: prompt.messages.filter(item => item.enable)
                                }, null, 2))}>
                                    CopyAll
                                </Button>
                                <Divider type="vertical" />
                                <Button onClick={() => {
                                    const newMessages = prompt.messages.map(item => ({ ...item, enable: false }));
                                    setPrompt({ ...prompt, messages: newMessages });
                                }}>
                                    DisableAll
                                </Button>
                                <Button onClick={() => {
                                    const newMessages = prompt.messages.map(item => ({ ...item, enable: true }));
                                    setPrompt({ ...prompt, messages: newMessages });
                                }}>
                                    EnableAll
                                </Button>
                            </Space>
                        }
                    >
                        <Row justify="space-around">
                            <PromptInput
                                messages={prompt.messages}
                                withCopy={true}
                                withControl={true}
                                onOrderUp={index => order(index, -1)}
                                onOrderDown={index => order(index, 1)}
                                onRemove={index => deletePrompt(index)}
                                onAdd={(index, role, content) => addPrompt(index, role, content)}
                            />
                        </Row>

                        <Divider>
                            <Space>
                                <Button onClick={() => {
                                    const newMessages = [...prompt.messages, { role: 'system', enable: true, content: '' }];
                                    setPrompt({ ...prompt, messages: newMessages });
                                }}>
                                    <PlusOutlined />
                                </Button>
                            </Space>
                        </Divider>
                    </Card>
                </Col>

                <Col span={12}>
                    <Card
                        title="Response"
                        extra={
                            <Space direction="horizontal">
                                <Button onClick={update}>Update</Button>
                                <Button onClick={chat}>Request</Button>
                                <Button onClick={doCommit}>Commit</Button>
                                <Button onClick={() => copy(response)}>Copy</Button>
                                <Button onClick={responseToPrompt}>Append</Button>
                            </Space>
                        }
                    >
                        <Skeleton loading={loading} active avatar>
                            <div>
                                <Typography.Text>time cost: {timecost / 1000} second</Typography.Text>
                                <Divider />
                                <Tabs activeKey={responseMode} onChange={key => setResponseMode(key)}>
                                    <TabPane key="1" tab="Markdown">
                                        <ReactMarkdown>{response}</ReactMarkdown>
                                    </TabPane>
                                    <TabPane key="2" tab="Text" forceRender>
                                        <Input.TextArea
                                            value={response}
                                            onChange={e => setResponse(e.target.value)}
                                            autoSize={{ maxRows: 16 }}
                                        />
                                    </TabPane>
                                </Tabs>
                            </div>
                        </Skeleton>
                    </Card>

                    <Card title="LLM Options">
                        <List itemLayout="horizontal">
                            <List.Item>
                                <Space>
                                    Model:
                                    <ModelSelect
                                        style={{ width: 200 }}
                                        selected={model}
                                        prefer={options?.prefer}
                                        models={store.globalModels?.models || []}
                                        onSelect={value => setModel(value)}
                                        onPrefer={value => updatePreferModel(value)}
                                    />
                                    <Button onClick={reloadModels}>
                                        <SyncOutlined />
                                    </Button>
                                </Space>
                            </List.Item>

                            <List.Item>
                                <Space>
                                    Temperature:
                                    <InputNumber
                                        style={{ width: 100 }}
                                        min={0}
                                        max={2}
                                        step={0.1}
                                        value={options.temperature}
                                        onChange={value => setOptions({ ...options, temperature: value })}
                                    />
                                </Space>
                                <Space>
                                    Top_P:
                                    <InputNumber
                                        style={{ width: 100 }}
                                        min={0}
                                        max={2}
                                        step={0.1}
                                        value={options.topP}
                                        onChange={value => setOptions({ ...options, topP: value })}
                                    />
                                </Space>
                            </List.Item>

                            <List.Item>
                                Use Embed
                                <Switch
                                    checked={withEmbed}
                                    onChange={handleEmbedChange}
                                />
                            </List.Item>

                            <Space>
                                <ArgumentPanel
                                    setting={store.globalArgs}
                                    args={args}
                                    onSelect={selectArg}
                                />
                            </Space>
                        </List>
                    </Card>
                </Col>
            </Row>
        </div>
    );
}

export default PromptView;