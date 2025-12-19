import { EmployeeForm } from '../components/prediction/EmployeeForm';
import { motion } from 'framer-motion';

export default function Analytics() {
    return (
        <div className="space-y-8 max-w-7xl mx-auto">
            <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
                <div>
                    <h1 className="text-3xl font-bold text-brand-dark">Predictive Analytics</h1>
                    <p className="text-brand-primary/80 mt-1 font-medium">AI-driven attrition prediction & retention planning</p>
                </div>

                <div className="flex items-center space-x-2 text-sm text-brand-light bg-white px-4 py-2 rounded-xl shadow-sm border border-brand-primary/5">
                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                    <span>Model v1.0 Active</span>
                </div>
            </motion.div>

            <EmployeeForm />
        </div>
    );
}
