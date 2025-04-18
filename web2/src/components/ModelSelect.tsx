import React, { useState } from 'react';
import { Select, Button } from 'antd';
import { HeartOutlined, HeartTwoTone } from '@ant-design/icons';

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
                {models.map((value) => (
                    <Select.Option key={value} value={value}>
                        <Button onClick={() => handleDefault(value)}>
                            {value === prefer ? (
                                <HeartTwoTone twoToneColor="#eb2f96" />
                            ) : (
                                <HeartOutlined />
                            )}
                        </Button>
                        {value}
                    </Select.Option>
                ))}
            </Select>
        </div>
    );
};

export default ModelSelect;
