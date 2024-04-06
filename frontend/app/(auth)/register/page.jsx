'use client'
import { useState } from 'react';
import Router from 'next/router';

export default function Register() {
    const [formData, setFormData] = useState({ userId: '', password: '', role: 'Student' });
    const [alert, setAlert] = useState({ show: false, message: '', type: '' });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        try {
            e.preventDefault();

            const res = await fetch('http://localhost:8080/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (res.ok) {
                setAlert({
                    show: true,
                    message: 'Registration successful! Redirecting to login...',
                    type: 'success',
                });
                setTimeout(() => {
                    Router.push('/login');
                }, 3000); // Adjust time as needed for UX
            } else {
                const errorData = await res.json();
                setAlert({
                    show: true,
                    message: errorData.error || 'Failed to register. Please try again.',
                    type: 'error',
                });
            }
        } catch (error) {
            setAlert({
                show: true,
                message: error.message || 'Failed to register. Please try again.',
                type: 'error',
            });
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="px-8 py-6 mt-4 text-left bg-white shadow-lg">
                <h3 className="text-2xl font-bold text-center">Register</h3>
                <form onSubmit={handleSubmit}>
                    <div className="mt-4">
                        <div>
                            <label className="block" htmlFor="userId">User ID</label>
                            <input 
                                type="text" 
                                placeholder="User ID" 
                                name="userId"
                                onChange={handleChange} 
                                className="w-full px-4 py-2 mt-2 border rounded-md"
                                required 
                            />
                        </div>
                        <div className="mt-4">
                            <label className="block" htmlFor="password">Password</label>
                            <input 
                                type="password" 
                                placeholder="Password" 
                                name="password"
                                onChange={handleChange} className="w-full px-4 py-2 mt-2 border rounded-md"
                                required 
                            />
                        </div>
                        <div className="mt-4">
                            <label className="block" htmlFor="role">Role</label>
                            <select 
                                name="role" 
                                onChange={handleChange} 
                                className="w-full px-4 py-2 mt-2 border rounded-md"
                            >
                                <option value="Student">Student</option>
                                <option value="Lecturer">Lecturer</option>
                                <option value="Admin">Admin</option>
                            </select>
                        </div>
                        <div className="flex items-baseline justify-between">
                            <button type="submit" className="px-6 py-2 mt-4 text-white bg-blue-600 rounded-lg hover:bg-blue-900">Register</button>
                        </div>
                    </div>
                </form>
                {alert.show && (
                    <div className={`mt-4 text-white px-6 py-2 rounded-md ${alert.type === 'error' ? 'bg-red-500' : 'bg-green-500'}`}>
                        {alert.message}
                    </div>
                )}
            </div>
        </div>
    );
}
