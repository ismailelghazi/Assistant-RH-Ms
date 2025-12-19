import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader2, AlertTriangle, CheckCircle, BrainCircuit } from 'lucide-react';
import api from '../../lib/api';

// Initial state matching backend Schema (all 30 fields)
const initialData = {
    Age: 30,
    BusinessTravel: 'Travel_Rarely',
    DailyRate: 800,
    Department: 'Research & Development',
    DistanceFromHome: 5,
    Education: 3,
    EducationField: 'Life Sciences',
    EnvironmentSatisfaction: 3,
    Gender: 'Male',
    HourlyRate: 60,
    JobInvolvement: 3,
    JobLevel: 2,
    JobRole: 'Laboratory Technician',
    JobSatisfaction: 3,
    MaritalStatus: 'Married',
    MonthlyIncome: 5000,
    MonthlyRate: 15000,
    NumCompaniesWorked: 2,
    OverTime: 'No',
    PercentSalaryHike: 15,
    PerformanceRating: 3,
    RelationshipSatisfaction: 3,
    StockOptionLevel: 1,
    TotalWorkingYears: 10,
    TrainingTimesLastYear: 2,
    WorkLifeBalance: 3,
    YearsAtCompany: 5,
    YearsInCurrentRole: 2,
    YearsSinceLastPromotion: 1,
    YearsWithCurrManager: 3
};

export function EmployeeForm() {
    const [formData, setFormData] = useState(initialData);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [plan, setPlan] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value, type } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'number' ? Number(value) : value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);
        setPlan(null);

        try {
            // 1. Get Prediction
            const predRes = await api.post('/predict', formData);
            setResult(predRes.data);

            // 2. Get Retention Plan (Parallel or sequential depending on UX preference)
            const planRes = await api.post('/generate-retention-plan', formData);
            setPlan(planRes.data.retention_plan);

        } catch (error) {
            console.error("Analysis failed", error);
            alert("Failed to run analysis. Please checks backend logs.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Form Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white p-6 rounded-2xl shadow-sm border border-brand-primary/10"
            >
                <div className="flex items-center space-x-2 mb-6">
                    <div className="p-2 bg-brand-primary/10 rounded-lg text-brand-primary">
                        <UsersIcon />
                    </div>
                    <h2 className="text-xl font-bold text-brand-dark">Employee Data</h2>
                </div>

                <form onSubmit={handleSubmit} className="space-y-8">

                    {/* Group 1: Demographics */}
                    <div className="space-y-4">
                        <h3 className="text-xs font-bold text-brand-light uppercase tracking-widest border-b border-gray-100 pb-2">Demographics</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Age</label>
                                <input type="number" name="Age" value={formData.Age} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm focus:ring-1 focus:ring-brand-primary focus:border-brand-primary transition-all output-none" />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Gender</label>
                                <select name="Gender" value={formData.Gender} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm focus:ring-1 focus:ring-brand-primary outline-none">
                                    <option>Male</option>
                                    <option>Female</option>
                                </select>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Marital Status</label>
                                <select name="MaritalStatus" value={formData.MaritalStatus} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm focus:ring-1 focus:ring-brand-primary outline-none">
                                    <option>Single</option>
                                    <option>Married</option>
                                    <option>Divorced</option>
                                </select>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Education Field</label>
                                <select name="EducationField" value={formData.EducationField} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm focus:ring-1 focus:ring-brand-primary outline-none">
                                    <option>Life Sciences</option>
                                    <option>Medical</option>
                                    <option>Marketing</option>
                                    <option>Technical Degree</option>
                                    <option>Other</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Group 2: Job Info */}
                    <div className="space-y-4">
                        <h3 className="text-xs font-bold text-brand-light uppercase tracking-widest border-b border-gray-100 pb-2">Job Details</h3>
                        <div className="grid grid-cols-1 gap-4">
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Department</label>
                                <select name="Department" value={formData.Department} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm focus:ring-1 focus:ring-brand-primary outline-none">
                                    <option>Sales</option>
                                    <option>Research & Development</option>
                                    <option>Human Resources</option>
                                </select>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Job Role</label>
                                <select name="JobRole" value={formData.JobRole} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm focus:ring-1 focus:ring-brand-primary outline-none">
                                    <option>Sales Executive</option>
                                    <option>Research Scientist</option>
                                    <option>Laboratory Technician</option>
                                    <option>Manufacturing Director</option>
                                    <option>Healthcare Representative</option>
                                    <option>Manager</option>
                                    <option>Sales Representative</option>
                                    <option>Research Director</option>
                                    <option>Human Resources</option>
                                </select>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Monthly Income ($)</label>
                                <input type="number" name="MonthlyIncome" value={formData.MonthlyIncome} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm" />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">OverTime</label>
                                <select name="OverTime" value={formData.OverTime} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm">
                                    <option>Yes</option>
                                    <option>No</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Group 3: Satisfaction */}
                    <div className="space-y-4">
                        <h3 className="text-xs font-bold text-brand-light uppercase tracking-widest border-b border-gray-100 pb-2">Satisfaction Metrics (1-4)</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Job Satisfaction</label>
                                <input type="number" min="1" max="4" name="JobSatisfaction" value={formData.JobSatisfaction} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm" />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Environment</label>
                                <input type="number" min="1" max="4" name="EnvironmentSatisfaction" value={formData.EnvironmentSatisfaction} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm" />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Work Life Balance</label>
                                <input type="number" min="1" max="4" name="WorkLifeBalance" value={formData.WorkLifeBalance} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm" />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-semibold text-brand-dark ml-1">Relation. Satisf.</label>
                                <input type="number" min="1" max="4" name="RelationshipSatisfaction" value={formData.RelationshipSatisfaction} onChange={handleChange} className="w-full bg-brand-beige/30 border border-brand-primary/10 rounded-lg px-3 py-2 text-sm" />
                            </div>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-brand-primary text-white font-bold py-4 rounded-xl shadow-xl shadow-brand-primary/10 hover:shadow-brand-primary/30 hover:-translate-y-0.5 transition-all flex items-center justify-center space-x-3 disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        {loading ? <Loader2 className="animate-spin" /> : <BrainCircuit size={20} />}
                        <span>{loading ? 'Analyzing with Gemini...' : 'Analyze Employee Churn Risk'}</span>
                    </button>
                </form>
            </motion.div>

            {/* Results Section */}
            <div className="space-y-6">
                {result && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className={`p-6 rounded-2xl border-l-4 shadow-sm ${result.churn_probability > 50 ? 'bg-red-50 border-red-500' : 'bg-green-50 border-green-500'
                            }`}
                    >
                        <div className="flex items-center space-x-3 mb-2">
                            {result.churn_probability > 50 ? <AlertTriangle className="text-red-500" /> : <CheckCircle className="text-green-500" />}
                            <h3 className={`text-xl font-bold ${result.churn_probability > 50 ? 'text-red-700' : 'text-green-700'}`}>
                                Churn Risk: {result.churn_probability.toFixed(1)}%
                            </h3>
                        </div>
                        <p className="text-sm text-gray-600 ml-9">
                            {result.churn_probability > 50
                                ? "Critical: Employee is highly likely to leave. Review retention plan immediately."
                                : "Safe: Employee is stable, but maintain engagement."}
                        </p>
                    </motion.div>
                )}

                {plan && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="bg-white p-8 rounded-2xl shadow-lg border border-brand-primary/10 relative overflow-hidden"
                    >
                        <div className="absolute top-0 right-0 p-4 opacity-10">
                            <BrainCircuit size={100} className="text-brand-primary" />
                        </div>

                        <h2 className="text-lg font-bold text-brand-dark mb-6 flex items-center space-x-2">
                            <span className="bg-gradient-to-r from-brand-primary to-brand-light text-white text-xs px-2 py-1 rounded-md uppercase tracking-wider">Gemini AI</span>
                            <span>Retention Strategy</span>
                        </h2>

                        <div className="prose prose-sm prose-slate text-brand-dark/80 whitespace-pre-wrap leading-relaxed">
                            {plan}
                        </div>
                    </motion.div>
                )}

                {!result && !loading && (
                    <div className="h-full min-h-[400px] bg-white/50 p-8 rounded-2xl border-2 border-dashed border-brand-primary/10 flex flex-col items-center justify-center text-center">
                        <div className="w-20 h-20 bg-brand-primary/5 rounded-full flex items-center justify-center mb-6 text-brand-primary/50">
                            <BrainCircuit size={40} />
                        </div>
                        <h3 className="text-xl font-bold text-brand-dark mb-2">Ready to Analyze</h3>
                        <p className="text-brand-light max-w-xs mx-auto">
                            Enter employee details on the left and our ML + Gemini AI models will generate an instant retention strategy.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}

function UsersIcon() {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>
    )
}
