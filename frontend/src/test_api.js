import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TestApi = () => {
    const [message, setMessage] = useState('');

    useEffect(() => {
        axios.get('/api/test')
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error('There was an error fetching the API!', error);
            }); 
    }, []);
    return (
        <div>
        <h2>Backend says:</h2>
        <p>{message}</p>
        </div>
    );      
};
export default TestApi;