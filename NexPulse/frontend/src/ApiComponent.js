import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ApiComponent = () => {
    const [message, setMessage] = useState('');

    useEffect(() => {
        axios.get('http://127.0.0.1:8002/api/')
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            });
    }, []);

    return (
        <div>
            <h1>{message}</h1>
        </div>
    );
};

export default ApiComponent;
