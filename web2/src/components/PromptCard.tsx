import { Button, Space } from 'antd';
import React from 'react';
import { useClipboard } from 'react-use-clipboard'; // or any other clipboard hook you prefer

interface Message {
    role: string;
    content: string;
}

interface Props {
    messages: Message[];
}

const PromptCard: React.FC<Props> = ({ messages }) => {
    const [isCopied, setCopied] = useClipboard('', { successDuration: 1000 });

    const copyRaw = () => {
        const rawText = messages
            .map((message) => `${message.role}:\n${message.content}`)
            .join('\n');
        setCopied(rawText);
    };

    const copyJson = () => {
        const jsonText = JSON.stringify(messages);
        setCopied(jsonText);
    };

    return (
        <Space direction="horizontal">
            <Space className="scroll-short" direction="vertical">
                {messages.map((item, index) => (
                    <div key={index}>
                        <span style={{ color: 'blue' }}>{item.role} </span>
                        <span>: </span>
                        <span style={{ whiteSpace: 'pre-line' }}>{item.content}</span>
                    </div>
                ))}
            </Space>
            <Space direction="vertical">
                <Button className="right" onClick={copyJson}>
                    Copy to JSON
                </Button>
                <Button className="right" onClick={copyRaw}>
                    Copy to RAW
                </Button>
            </Space>
        </Space>
    );
};

export default PromptCard;
