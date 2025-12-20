import { useLocation, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    BarChart2,
    LogOut,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const menuItems = [
    { icon: BarChart2, label: 'Analytics', path: '/' },
];

export function Sidebar() {
    const location = useLocation();
    const { logout } = useAuth();

    return (
        <div className="h-screen w-64 bg-brand-dark flex flex-col shadow-2xl relative z-20">
            {/* Logo Area */}
            <div className="p-8 pb-4">
                <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-tr from-brand-primary to-brand-light rounded-lg flex items-center justify-center">
                        <BarChart2 className="text-white w-5 h-5" />
                    </div>
                    <h1 className="text-xl font-bold text-white tracking-tight">RetentionAI</h1>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-4 py-6 space-y-2">
                {menuItems.map((item) => {
                    const isActive = location.pathname === item.path || (location.pathname === '/analytics'); // Keep active for both / and /analytics if using alias
                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className="relative block group"
                        >
                            {isActive && (
                                <motion.div
                                    layoutId="activeTab"
                                    className="absolute inset-0 bg-brand-primary/20 rounded-xl"
                                    initial={false}
                                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                                />
                            )}
                            <div className={`relative px-4 py-3 flex items-center space-x-3 rounded-xl transition-colors duration-200 ${isActive ? 'text-brand-light' : 'text-slate-400 group-hover:text-white'}`}>
                                <item.icon size={20} className={isActive ? 'text-brand-primary' : ''} />
                                <span className="font-medium">{item.label}</span>
                            </div>
                        </Link>
                    );
                })}
            </nav>

            {/* User Section */}
            <div className="p-4 border-t border-white/5">
                <button
                    onClick={logout}
                    className="w-full px-4 py-3 flex items-center space-x-3 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-xl transition-all"
                >
                    <LogOut size={20} />
                    <span className="font-medium">Sign Out</span>
                </button>
            </div>
        </div>
    );
}
