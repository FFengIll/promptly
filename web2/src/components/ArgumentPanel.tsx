import React, { useState, useEffect } from 'react';

interface Argument {
    key: string;
    value: string;
}

interface ArgumentSetting {
    args: Record<string, string[]>;
}

interface Props {
    setting: ArgumentSetting;
    args: Argument[];
    mask: string[];
    onSelect: (key: string, value: string) => void;
}

const ArgumentPanel: React.FC<Props> = ({ setting, args, mask, onSelect }) => {
    const [selectedValues, setSelectedValues] = useState<Record<string, string>>({});

    useEffect(() => {
        // Update the selected values state based on the initial args
        const initialSelected: Record<string, string> = {};
        args.forEach(arg => {
            initialSelected[arg.key] = arg.value;
        });
        setSelectedValues(initialSelected);
    }, [args]);

    const handleSelect = (key: string, value: string) => {
        console.log(key, value);
        setSelectedValues((prev) => ({ ...prev, [key]: value }));
        onSelect(key, value);
    };

    const isDisabled = (key: string) => {
        return mask.includes(key);
    };

    const getSelectValue = (key: string) => {
        return selectedValues[key] || '';
    };

    const data = Object.keys(setting.args).map((key) => ({
        key: key,
        values: setting.args[key],
    }));

    return (
        <div>
            <ul style={{ listStyleType: 'none' }}>
                {data.map((item) => (
                    <li key={item.key} style={{ marginBottom: '20px' }}>
                        <div style={{ display: 'flex', alignItems: 'baseline' }}>
                            <span style={{ marginRight: '10px' }}>{item.key}</span>

                            <select
                                disabled={isDisabled(item.key)}
                                value={getSelectValue(item.key)}
                                onChange={(e) => handleSelect(item.key, e.target.value)}
                                style={{ width: '300px' }}
                            >
                                <option key="" value="">
                                    Select
                                </option>
                                {item.values.map((v, index) => (
                                    <option key={v} value={v}>
                                        {v}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ArgumentPanel;