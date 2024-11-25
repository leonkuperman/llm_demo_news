import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const SentimentTimeline = () => {
    const [articles, setArticles] = useState([]);
    const maxItems = 60;  // Display up to 60 articles

    const fetchArticles = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/articles?classified=true`);
            setArticles(response.data.articles);
        } catch (error) {
            console.error("Error fetching classified articles:", error.response || error.message);
        }
    };

    useEffect(() => {
        fetchArticles();  // Initial fetch on mount
    
        // Set up polling interval to refresh articles every 5 seconds
        const intervalId = setInterval(() => {
            fetchArticles();
        }, 1000);  // 5000 milliseconds = 5 seconds
    
        // Clean up interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    // Prepare the data for the chart
    const data = {
        labels: articles.slice(-maxItems).map(() => ''),  // Empty labels for a continuous timeline
        datasets: [
            {
                label: 'Sentiment Score',
                data: articles.slice(-maxItems).map(article => article.sentiment || 0),
                backgroundColor: articles.slice(-maxItems).map(article => {
                    if (article.sentiment > 0) return 'green';  // Positive sentiment
                    if (article.sentiment < 0) return 'red';    // Negative sentiment
                    return 'blue';                               // Neutral sentiment
                }),
                borderColor: articles.slice(-maxItems).map(article => {
                    if (article.sentiment > 0) return 'green';
                    if (article.sentiment < 0) return 'red';
                    return 'blue';
                }),
                borderWidth: 1,
                barThickness: 'flex',  // Allows flexible width for bars
            }
        ]
    };

    const options = {
        animation: false,  // Disable animations
        scales: {
            x: {
                display: false  // Hide x-axis for a cleaner look
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Sentiment Score'
                }
            }
        },
        plugins: {
            legend: {
                display: false  // Hide the legend for a simpler view
            }
        }
    };

    return (
        <div style={{ width: '100%', maxWidth: '1000px', margin: '0 auto' }}>
            <h2>Sentiment Timeline</h2>
            <Bar key={articles.length} data={data} options={options} />
        </div>
    );
};

export default SentimentTimeline;