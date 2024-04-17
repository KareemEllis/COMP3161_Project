'use client'
import { useState } from 'react';
import Router from 'next/router';

export default function Login() {
    const [credentials, setCredentials] = useState({ userid: '', password: '' });

    const handleChange = (e) => {
        setCredentials({ ...credentials, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Substitute with your API endpoint
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials),
        });
        if (res.ok) {
            const data = await res.json();
            sessionStorage.setItem('userId', data.userId); // Assuming the API returns a userId
            Router.push('/dashboard');
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="px-8 py-6 mt-4 text-left bg-white shadow-lg">
                <h3 className="text-2xl font-bold text-center">Login</h3>
                <form onSubmit={handleSubmit}>
                    <div className="mt-4">
                        <div>
                            <label className="block" htmlFor="userid">User ID</label>
                            <input type="text" placeholder="User ID" name="userid"
                                onChange={handleChange} className="w-full px-4 py-2 mt-2 border rounded-md"
                                required />
                        </div>
                        <div className="mt-4">
                            <label className="block" htmlFor="password">Password</label>
                            <input type="password" placeholder="Password" name="password"
                                onChange={handleChange} className="w-full px-4 py-2 mt-2 border rounded-md"
                                required />
                        </div>
                        <div className="flex items-baseline justify-between">
                            <button type="submit" className="px-6 py-2 mt-4 text-white bg-blue-600 rounded-lg hover:bg-blue-900">Login</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}
