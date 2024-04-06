'use client'
import { useState } from 'react';
import Router from 'next/router';

export default function CreateCourse() {
    const [formData, setFormData] = useState({
        courseId: '',
        courseName: '',
        period: ''
    });
    const [alert, setAlert] = useState({ show: false, message: '', type: '' });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        try {
            e.preventDefault();

            const response = await fetch('http://localhost:8080/api/course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                alert('Course created successfully');
                setAlert({ show: true, message: 'Course created successfully', type: 'success' });
                Router.push('/'); // Adjust the redirect as necessary
            } else {
                const errorData = await response.json();
                setAlert({ show: true, message: errorData.error || 'Failed to create course', type: 'error' });
            }
        } catch (error) {
            setAlert({ show: true, message: errorData.error || 'Failed to create course', type: 'error' });
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="px-8 py-6 mt-4 text-left bg-white shadow-lg">
                <h3 className="text-2xl font-bold text-center">Create New Course</h3>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label className="block" htmlFor="courseId">Course ID</label>
                        <input
                            type="text"
                            name="courseId"
                            onChange={handleChange}
                            className="w-full p-2 mt-2 border rounded-md"
                            required
                        />
                    </div>
                    <div className="mt-4">
                        <label className="block" htmlFor="courseName">Course Name</label>
                        <input
                            type="text"
                            name="courseName"
                            onChange={handleChange}
                            className="w-full p-2 mt-2 border rounded-md"
                            required
                        />
                    </div>
                    <div className="mt-4">
                        <label className="block" htmlFor="period">Period</label>
                        <input
                            type="text"
                            name="period"
                            onChange={handleChange}
                            className="w-full p-2 mt-2 border rounded-md"
                            required
                        />
                    </div>
                    <div className="flex justify-center mt-6">
                        <button type="submit" className="px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700">
                            Create Course
                        </button>
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
