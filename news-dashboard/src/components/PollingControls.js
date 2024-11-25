import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Button, Typography, Stack } from '@mui/material';

const PollingControls = () => {
    const [status, setStatus] = useState({ is_polling: false, is_classifying: false });

    const resetClassifications = async () => {
        try {
            // Send a POST request to the reset endpoint
            await axios.get('http://localhost:8000/reset_classifications');
            console.log('Classifications reset successfully.');
            await updateStatus();
        } catch (error) {
            console.error("Error resetting classifications:", error);
        }
    };

    const updateStatus = async () => {
        try {
            const response = await axios.get('http://localhost:8000/polling_status');
            setStatus(response.data);
        } catch (error) {
            console.error("Error updating status:", error.response || error.message);
        }
    };

    const togglePolling = async (start) => {
        try {
            await axios.get(`http://localhost:8000/${start ? 'start_polling' : 'stop_polling'}`);
            await updateStatus();
        } catch (error) {
            console.error("Error toggling polling:", error.response || error.message);
        }
    };

    const toggleClassifying = async (start) => {
        try {
            await axios.get(`http://localhost:8000/${start ? 'start_classifying' : 'stop_classifying'}`);
            await updateStatus();
        } catch (error) {
            console.error("Error toggling classification:", error.response || error.message);
        }
    };

    useEffect(() => {
        updateStatus();
    }, []);

    return (
        <Box sx={{ p: 2, border: '1px solid #ddd', borderRadius: 2, backgroundColor: '#f9f9f9', maxWidth: 600, margin: '0 auto' }}>
            <Typography variant="h5" gutterBottom>Polling and Classification Controls</Typography>
            <Stack direction="row" spacing={2} justifyContent="center" sx={{ mb: 2 }}>
                <Button variant="contained" color="primary" onClick={() => togglePolling(true)}>Start Polling</Button>
                <Button variant="contained" color="secondary" onClick={() => togglePolling(false)}>Stop Polling</Button>
                <Button variant="contained" color="primary" onClick={() => toggleClassifying(true)}>Start Classifying</Button>
                <Button variant="contained" color="secondary" onClick={() => toggleClassifying(false)}>Stop Classifying</Button>
                <Button variant="contained" color="primary" onClick={resetClassifications}>Reset Articles</Button>
            </Stack>
            <Typography variant="body1">Polling Status: {status.is_polling ? "Active" : "Inactive"}</Typography>
            <Typography variant="body1">Classification Status: {status.is_classifying ? "Active" : "Inactive"}</Typography>
        </Box>
    );
};

export default PollingControls;