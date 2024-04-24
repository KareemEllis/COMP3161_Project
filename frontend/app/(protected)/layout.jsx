'use client'
import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react';

import { getUserData } from '@/services/auth';

import Navbar from '@/app/components/Navbar';

export default function RootLayout({ children }) {
    const router = useRouter();

    useEffect(() => {
        const checkUserData = async () => {
            try {
                const userData = await getUserData();
                console.log('User data found:', userData);
            } catch (error) {
                console.error('Error retrieving user data:', error);
                router.push('/login');
            }
        };

        checkUserData();
    }, [router]);

    return (
        <>
        <Navbar />
        {children}
        </>
    );
}
