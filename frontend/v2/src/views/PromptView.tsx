import {
    PlusOutlined,
    SyncOutlined
} from '@ant-design/icons';
import {
    Button,
    Card,
    Col,
    Divider,
    FloatButton,
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
const { Option } = Select;


function PromptView() {
    const { key } = useParams();
    console.log("param:", key);
    const store = useConfigStore();

    // State variables
    const [loading, setLoading] = useState(false);
    const [model, setModel] = useState("");
    const [models, setModels] = useState([]);
    const [timecost, setTimecost] = useState(0);
    const [description, setDescription] = useState("");
    const [withEmbed, setWithEmbed] = useState(false);
    const [argValue, setArgValue] = useState("");
    const [argKey, setArgKey] = useState("");
    const [response, setResponse] = useState("test");
    const [responseMode, setResponseMode] = useState("1");
    const [argSetting, setArgSetting] = useState({});
    const [args, setArgs] = useState([]);
    const [messages, setMessages] = useState([]); // Default empty array for messages
    const [plugins, setPlugins] = useState([]); // Default empty array for plugins
    const [options, setOptions] = useState({}); // Default empty object for options

    // Effects
    useEffect(() => {
        fetchPrompt(key);
        fetchModels();
    }, [key]);

    // Methods
    const copy = (text) => {
        navigator.clipboard.writeText(text).then(() => {
            openNotification('Copied to clipboard', 'success');
        }).catch(err => {
            openNotification('Failed to copy: ' + err, 'error');
        });
    };

    const fetchModels = async () => {
        try {
            const res = await backend.apiGlobalModelsGet();
            console.log("fetch models: ", res.data);
            setModels(res.data.models || []);
        } catch (err) {
            openNotification('Failed to reload models: ' + err.toString(), 'error');
        }
    };

    const updatePreferModel = (modelName) => {
        const newOptions = { ...(options || {}), prefer: modelName }; // 防止 options 为 undefined
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
        addPrompt(messages.length, 'assistant', response);
    };

    const deletePrompt = (index) => {
        const newMessages = [...messages];
        newMessages.splice(index, 1);
        setMessages(newMessages);
    };

    const doCommit = async () => {
        const body = {
            name: key,
            commit: {
                messages: messages,
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
        const newMessages = [...messages];
        const newMessage = { content, role, enable: true };

        let insertIndex = index;
        while (insertIndex > 0 && newMessages[insertIndex - 1].role === 'system') {
            insertIndex -= 1;
        }

        newMessages.splice(insertIndex, 0, newMessage);
        setMessages(newMessages);
    };

    const order = (index, delta) => {
        const anotherIndex = index + delta;
        if (anotherIndex < 0 || anotherIndex >= messages.length) {
            return;
        }

        const newMessages = [...messages];
        const temp = newMessages[index];
        newMessages[index] = newMessages[anotherIndex];
        newMessages[anotherIndex] = temp;

        setMessages(newMessages);
    };

    const fetchArgument = async (name) => {
        setArgSetting({})
        // try {
        //     const response = await backend.apiPromptArgsNameGet(name);
        //     // setArgSetting(response.data || { name: "", args: [] }); // 确保 response.data 有默认值
        //     setArgSetting({})
        // } catch (err) {
        //     openNotification(err.toString(), "error");
        // }
    };

    const fetchPrompt = async (name) => {
        try {
            await fetchArgument(name);

            const response = await backend.apiPromptNameGet(name);
            const promptData = response.data;

            setMessages(promptData.messages || [],)
            setPlugins(promptData.plugins || [],)
            setDescription(promptData.description || "");
            setArgs(promptData.args || []);
            setOptions(promptData.options || {});
            setModel(promptData.options?.model || "");

            const hasEmbed = (promptData.plugins || []).includes('embed');
            setWithEmbed(hasEmbed);
        } catch (err: any) {
            console.log(err);
            // openNotification("" + err.toString(), "error");
        }
    };

    const reload = () => {
        fetchPrompt(key);
    };

    const update = async () => {
        const body = {
            messages: messages,
            args: args,
            options: options,
            description: description,
        };

        try {
            await backend.apiPromptNamePut(body, key);
        } catch (err) {
            openNotification("" + err.toString(), "error");
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

            const body = {
                messages: messages,
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
            openNotification("" + err.toString(), "error");

        } finally {
            setLoading(false);
        }
    };

    const chatWithPrompt = async () => {
        try {
            const body = {
                messages: messages,
                args: args,
                options: options,
            };

            await backend.apiPromptNamePut(body, key);

            setLoading(true);
            setResponse('');

            const newOptions = { ...options, model };
            setOptions(newOptions);

            const start = new Date().getTime();
            const res = await BackendHelper.doChat(newOptions, messages, args);
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
        <>
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
                                    prompt: messages.filter(item => item.enable)
                                }, null, 2))}>
                                    CopyAll
                                </Button>
                                <Divider type="vertical" />
                                <Button onClick={() => {
                                    const newMessages = messages.map(item => ({ ...item, enable: false }));
                                    setMessages(newMessages);
                                }}>
                                    DisableAll
                                </Button>
                                <Button onClick={() => {
                                    const newMessages = messages.map(item => ({ ...item, enable: true }));
                                    setMessages(newMessages)
                                }}>
                                    EnableAll
                                </Button>
                            </Space>
                        }
                    >
                        <PromptInput
                            messages={messages}
                            setMessages={setMessages}
                            withCopy={true}
                            withControl={true}
                            onOrderUp={index => order(index, -1)}
                            onOrderDown={index => order(index, 1)}
                            onRemove={index => deletePrompt(index)}
                            onAdd={(index, role, content) => addPrompt(index, role, content)}
                        />

                        <Divider>
                            <Space>
                                <Button onClick={() => {
                                    const newMessages = [...messages, { role: 'user', enable: true, content: '' }];
                                    setMessages(newMessages);
                                }}>
                                    <PlusOutlined />
                                </Button>
                            </Space>
                        </Divider>
                    </Card>
                </Col>

                <Col span={12}>
                    <Card>
                        <Space direction="horizontal">
                            <Button onClick={update}>Update</Button>
                            <Button onClick={chat}>Request</Button>
                            <Button onClick={doCommit}>Commit</Button>
                            <Button onClick={() => copy(response)}>Copy</Button>
                            <Button onClick={responseToPrompt}>Append</Button>
                        </Space>
                    </Card>
                    <Card title="LLM Options">
                        <List itemLayout="horizontal">
                            <List.Item>
                                <Space direction="vertical">
                                    <Row align="middle">
                                        <Col span={12}>Model:</Col>
                                        <Col span={12}>
                                            <Space>
                                                <ModelSelect
                                                    selected={model}
                                                    prefer={options?.prefer}
                                                    models={models}
                                                    onSelect={value => setModel(value)}
                                                    onPrefer={value => updatePreferModel(value)}
                                                />
                                                <Button onClick={fetchModels}>
                                                    <SyncOutlined />
                                                </Button>
                                            </Space>
                                        </Col>
                                    </Row>
                                    <Row align="middle">
                                        <Col span={12}>Temperature:</Col>
                                        <Col span={12}>
                                            <InputNumber
                                                style={{ width: 100 }}
                                                min={0}
                                                max={2}
                                                step={0.1}
                                                value={options.temperature}
                                                onChange={value => setOptions({ ...options, temperature: value })}
                                            />
                                        </Col>
                                    </Row>
                                    <Row align="middle">
                                        <Col span={12}>Top_P:</Col>
                                        <Col span={12}>
                                            <InputNumber
                                                style={{ width: 100 }}
                                                min={0}
                                                max={2}
                                                step={0.1}
                                                value={options.topP}
                                                onChange={value => setOptions({ ...options, topP: value })}
                                            />
                                        </Col>
                                    </Row>
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

                    <Card
                        title="Response"
                        style={{
                            position: 'sticky',
                            top: 20,
                            zIndex: 1
                        }}
                    >
                        <Skeleton loading={loading} active>
                            <div>
                                <Typography.Text>time cost: {timecost / 1000} second</Typography.Text>
                                <Divider />
                                <Tabs
                                    activeKey={responseMode}
                                    onChange={key => setResponseMode(key)}
                                    items={[
                                        {
                                            key: "1",
                                            label: "Markdown",
                                            children: <ReactMarkdown>{response}</ReactMarkdown>
                                        },
                                        {
                                            key: "2",
                                            label: "Text",
                                            children: (
                                                <Input.TextArea
                                                    value={response}
                                                    onChange={e => setResponse(e.target.value)}
                                                    autoSize={{ minRows: 3 }}
                                                    style={{ width: '100%' }}
                                                />
                                            ),
                                            forceRender: true
                                        }
                                    ]}
                                />
                            </div>
                        </Skeleton>
                    </Card>
                </Col>
            </Row>

            <FloatButton.Group shape="circle" style={{ insetInlineEnd: 94 }} >
                {/* <FloatButton icon={<QuestionCircleOutlined />} /> */}
                {/* <FloatButton /> */}
                {/* <FloatButton icon={<SyncOutlined />} /> */}
                <FloatButton.BackTop type="primary" visibilityHeight={0} />
            </FloatButton.Group>
        </>
    );
}

export default PromptView;