import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 flex flex-col justify-center items-center">
      <h1 className="text-5xl text-center text-gray-800 font-bold mb-6">
        Welcome to Our Course Management System
      </h1>
      <p className="text-lg text-gray-700 mb-8 text-center">
        A platform where students and lecturers collaborate for a better learning experience.
      </p>
      <div className="flex space-x-4">
        <Link 
          href="/register"
          className="px-6 py-3 rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition duration-300"
        >
          Register
        </Link>
        <Link 
          href="/login"
          className="px-6 py-3 rounded-lg text-blue-600 border border-blue-600 hover:bg-blue-50 transition duration-300"
        >
          Login
        </Link>
      </div>
    </main>
  );
}
