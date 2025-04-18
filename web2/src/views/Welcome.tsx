import { Button, Typography } from 'antd';
import React from 'react';

const WelcomeView: React.FC = () => {
    return (
        <div style={{ maxWidth: '900px', margin: '0 auto' }}>
            <div
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    minHeight: '100vh',
                    textAlign: 'center',
                    gap: '32px'
                }}
            >
                <Typography.Title level={1}>
                    Welcome to Our Application
                </Typography.Title>

                <Typography.Title level={5} type="secondary">
                    Start your journey with us and explore amazing features
                </Typography.Title>

                <div style={{ marginTop: '32px' }}>
                    <Button
                        type="primary"
                        size="large"
                        style={{ marginRight: '16px' }}
                    >
                        Get Started
                    </Button>
                    <Button
                        size="large"
                    >
                        Learn More
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default WelcomeView;
