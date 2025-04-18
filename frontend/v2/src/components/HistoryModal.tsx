import { Button, Modal } from 'antd';
import React, { useState } from 'react';

const HistoryModal: React.FC = () => {
    const [open, setOpen] = useState<boolean>(true);

    const showModal = () => {
        setOpen(true);
    };

    const handleOk = () => {
        console.log("Modal confirmed");
        setOpen(false);
    };

    const handleCancel = () => {
        console.log("Modal cancelled");
        setOpen(false);
    };

    return (
        <div>
            <Modal
                title="Basic Modal"
                open={open}
                onOk={handleOk}
                onCancel={handleCancel}
                okText="OK"
                cancelText="Cancel"
            >
                <p>Some contents...</p>
                <p>Some contents...</p>
                <p>Some contents...</p>
            </Modal>
            {/* You can add a button to trigger the modal */}
            <Button type="primary" onClick={showModal}>
                Show Modal
            </Button>
        </div>
    );
};

export default HistoryModal;
