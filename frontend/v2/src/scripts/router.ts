import { useNavigate } from 'react-router-dom';

export const useRouteHelper = () => {
    const navigate = useNavigate();

    const toPrompt = (key: string) => {
        console.log('to prompt', key);
        navigate(`/view/prompt/${key}`);
    };

    const toCommit = (key: string) => {
        navigate(`/view/commit/${key}`);
    };

    const toTesting = (key: string) => {
        navigate(`/view/testing/${key}`);
    };

    return {
        toPrompt,
        toCommit,
        toTesting
    };
};
