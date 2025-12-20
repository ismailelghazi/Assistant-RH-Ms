import { Search, Bell, User } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export function Header() {
    const { user } = useAuth();

    return (
        <header className="px-8 py-5 flex items-center justify-between bg-brand-beige/50 backdrop-blur-sm sticky top-0 z-10">
            <div className="flex-1 max-w-xl">
                <div className="relative group">
                    <Search className="absolute left-4 top-3.5 text-brand-dark/40 group-focus-within:text-brand-primary transition-colors" size={20} />
                    <input
                        type="text"
                        placeholder="Search employees, reports, or settings..."
                        className="w-full bg-white/50 border border-brand-primary/10 rounded-2xl py-3 pl-12 pr-4 text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-primary/20 focus:border-brand-primary/30 transition-all shadow-sm"
                    />
                </div>
            </div>

            <div className="flex items-center space-x-6 ml-8">
                <button className="relative p-2 text-brand-dark/60 hover:text-brand-primary transition-colors">
                    <Bell size={22} />
                    <span className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border-2 border-brand-beige" />
                </button>

                <div className="flex items-center space-x-3 pl-6 border-l border-brand-primary/10">
                    <div className="text-right hidden md:block">
                        <p className="text-sm font-bold text-brand-dark">{user?.username || 'Admin User'}</p>
                        <p className="text-xs text-brand-primary font-medium">HR Manager</p>
                    </div>
                    <div className="w-10 h-10 bg-gradient-to-br from-brand-primary to-brand-dark rounded-xl flex items-center justify-center text-white shadow-lg">
                        <User size={20} />
                    </div>
                </div>
            </div>
        </header>
    );
}
