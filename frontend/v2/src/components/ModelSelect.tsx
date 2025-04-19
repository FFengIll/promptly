import { HeartOutlined, HeartTwoTone } from '@ant-design/icons';
import { Button, Select } from 'antd';
import React from 'react';

interface Props {
    selected: string;
    prefer: string;
    models: string[];
    onSelect: (value: string) => void;
    onPrefer: (value: string) => void;
}

const ModelSelect: React.FC<Props> = ({ selected, prefer, models, onSelect, onPrefer }) => {
    const handleSelect = (value: string) => {
        console.log(value);
        onSelect(value);
    };

    const handleDefault = (value: string) => {
        console.log(value);
        onPrefer(value);
    };

    return (
        <div>
            <Select
                style={{ width: 200 }}
                value={selected}
                onChange={handleSelect}
            >
                {Array.isArray(models) ? models.map((value) => (
                    <Select.Option key={value} value={value}>
                        <Button 
                            onClick={() => handleDefault(value)}
                            style={{ marginRight: 8, border: 'none', background: 'none', padding: 0 }}
                        >
                            {value === prefer ? (
                                <HeartTwoTone twoToneColor="#eb2f96" />
                            ) : (
                                <HeartOutlined />
                            )}
                        </Button>
                        <span>{value}</span>
                    </Select.Option>
                )) : null}
            </Select>
        </div>
    );
};

export default ModelSelect;
