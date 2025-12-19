import { Outlet } from 'react-router-dom';
import { LogOut, BarChart2 } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export function Layout() {
    const { logout } = useAuth();

    return (
        <div className="min-h-screen bg-brand-beige flex flex-col">
            {/* Minimal Top Bar */}
            <header className="px-8 py-4 flex items-center justify-between bg-white/50 backdrop-blur-sm border-b border-brand-primary/10">
                <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-tr from-brand-primary to-brand-light rounded-lg flex items-center justify-center">
                        <BarChart2 className="text-white w-5 h-5" />
                    </div>
                    <h1 className="text-xl font-bold text-brand-dark tracking-tight">RetentionAI</h1>
                </div>

                <button
                    onClick={logout}
                    className="flex items-center space-x-2 text-slate-500 hover:text-red-500 transition-colors text-sm font-medium"
                >
                    <LogOut size={16} />
                    <span>Sign Out</span>
                </button>
            </header>

            {/* Main Content Area */}
            <main className="flex-1 overflow-auto p-8 flex justify-center">
                <div className="w-full max-w-5xl">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
