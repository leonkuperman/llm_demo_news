import React from 'react';
import './App.css';
import PollingControls from './components/PollingControls';
import ArticleTable from './components/ArticleTable';
import SentimentTimeline from './components/SentimentTimeline';

function App() {
    return (
        <div className="App">
            <h1>News Polling and Classification Dashboard</h1>
            <PollingControls />
            <SentimentTimeline />
            <ArticleTable />
        </div>
    );
}

export default App;