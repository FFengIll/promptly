import { CheckOutlined, FileOutlined, HomeOutlined, MenuFoldOutlined, MenuUnfoldOutlined } from "@ant-design/icons";
import type { MenuProps } from 'antd';
import { ConfigProvider, Layout, Menu, Typography } from "antd";
import { Header } from "antd/es/layout/layout";
import zhCN from 'antd/es/locale/zh_CN';
import 'dayjs/locale/zh-cn';
import React, { useState } from 'react';
import { Link, Outlet, useNavigate, useParams } from 'react-router-dom';


const { Sider, Content } = Layout;
type MenuItem = Required<MenuProps>['items'][number];


const headerStyle: React.CSSProperties = {
    textAlign: 'center',
    display: 'flex',
    alignItems: 'center'
};

const contentStyle: React.CSSProperties = {
    // textAlign: 'center',
    // minHeight: 120,
    // lineHeight: '120px',
    // color: '#fff',
    // backgroundColor: '#0958d9',
};

const layoutStyle = {
    borderRadius: 8,
    minWidth: '1600px',
    // minHeight: '900px',
    // maxWidth: 'calc(100% - 8px)',
};

const App = () => {
    const locale = zhCN;

    const navigate = useNavigate();
    const params = useParams();
    const [collapsed, setCollapsed] = useState(false);

    const items: MenuItem[] = [
        {
            label: (
                <Link to={`/view/index${params.key ? `/${params.key}` : ''}`}>Index</Link>
            ),
            key: 'index',
            icon: <HomeOutlined />,
        },
        {
            label: (
                <Link to={`/view/prompt${params.key ? `/${params.key}` : ''}`}>Prompt</Link>
            ),
            key: 'prompt',
            icon: <FileOutlined />,
        },
        {
            label: (
                <Link to={`/view/commit${params.key ? `/${params.key}` : ''}`}>Commit</Link>
            ),
            key: 'commit',
            icon: <CheckOutlined />,
        },
    ]

    // useEffect(() => {
    //     if (store.globalArgs.args == null) {
    //         console.log("fetch global args");
    //         backend.apiGlobalArgsGet()
    //             .then((res) => {
    //                 store.updateArgs(res.data.args ?? []);
    //             });
    //     }
    //     if (store.globalModels.models == null) {
    //         console.log("fetch global models");
    //         backend.apiGlobalModelsGet()
    //             .then((res) => {
    //                 store.updateModels(res.data);
    //             });
    //     }
    // }, [store]);

    const routerTo = (view: string) => {
        const key = params.key;
        let path = `/view/${view}`;
        console.log(view);
        if (view !== 'index') {
            if (key && key.length > 0) {
                path = `${path}/${key}`;
            }
        }
        navigate(path);
    };

    return (
        <ConfigProvider locale={locale}>
            <Layout style={layoutStyle}>
                <Header style={headerStyle}>
                    <Link to="/">
                        <Typography.Title className="logo" style={{ color: 'white', textAlign: "center" }}>
                            Promptly
                        </Typography.Title>
                    </Link>
                </Header>

                <Layout>
                    <Sider collapsed={collapsed} trigger={null} collapsible>
                        <div className="logo" />

                        {collapsed ? (
                            <MenuUnfoldOutlined
                                className="trigger icon-white"
                                onClick={() => setCollapsed(!collapsed)}
                            />
                        ) : (
                            <MenuFoldOutlined
                                className="trigger icon-white"
                                onClick={() => setCollapsed(!collapsed)}
                            />
                        )}

                        <Menu
                            theme="dark"
                            // onClick={(e) => routerTo(e.key)}
                            // mode="horizontal"
                            // style={{ lineHeight: '64px' }}

                            items={items}
                        >

                        </Menu>
                    </Sider>

                    <Content style={{ margin: '24px 16px', padding: '24px', background: '#fff', minHeight: '280px' }}>
                        <Outlet />
                    </Content>
                </Layout>
            </Layout>
        </ConfigProvider>
    );
};

export default App;