import type { Argument, ArgumentSetting, ModelSetting } from '../sdk/models';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ConfigState {
    globalArgs: ArgumentSetting;
    globalModels: ModelSetting;
    updateModels: (setting: ModelSetting) => void;
    updateArgs: (args: Argument[]) => void;
}

export const useConfigStore = create<ConfigState>()(
    persist(
        (set) => ({
            globalArgs: {} as ArgumentSetting,
            globalModels: {
                defaultModel: "gpt-3.5-turbo",
                models: [],
            } as ModelSetting,
            updateModels: (setting: ModelSetting) => 
                set(() => ({ globalModels: setting })),
            updateArgs: (args: Argument[]) => 
                set(() => ({ globalArgs: { args } })),
        }),
        {
            name: 'config-storage',
        }
    )
);
