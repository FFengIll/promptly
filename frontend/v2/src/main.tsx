import '@ant-design/v5-patch-for-react-19';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';
import './index.css';
import CommitView from './views/CommitView';
import IndexView from './views/IndexView';
import PromptView from './views/PromptView';
import WelcomeView from './views/Welcome';



// 导入你的页面组件
const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            {
                path: '/',
                element: <WelcomeView />,
            },
            {
                path: '/view/index/:key',
                element: <IndexView />,
            },
            {
                path: '/view/prompt/:key',
                element: <PromptView />,
            },
            {
                path: '/view/commit/:key',
                element: <CommitView />,
            },
            // {
            //     path: 'testing',
            //     element: <Testing />,
            // },
        ],
    },
]);



createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <RouterProvider router={router}></RouterProvider>
    </StrictMode>,
)
