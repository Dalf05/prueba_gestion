import React, { useState, useEffect } from 'react';
import { GoogleGenAI } from "@google/genai";
import { 
  LayoutDashboard, 
  PlusCircle, 
  ListFilter, 
  Settings, 
  Bell, 
  Search,
  AlertCircle,
  CheckCircle2,
  Clock,
  MapPin,
  ChevronRight,
  BarChart3
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

// --- Types ---
interface Incident {
  id: number;
  title: string;
  description: string;
  category: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
  location: string;
  created_at: string;
  resolved_at?: string;
}

interface Stats {
  total: { count: number };
  open: { count: number };
  resolved: { count: number };
  byCategory: { category: string; count: number }[];
  avgResolutionTime: number; // in hours
  slaCompliance: number; // percentage
  resolutionTrend: { date: string; resolved: number; opened: number }[];
}

// --- Components ---

const UnieLogo = ({ className = "h-10", color = "white", showText = true }: { className?: string, color?: string, showText?: boolean }) => (
  <div className={`flex items-center gap-3 ${className}`}>
    <div className="flex flex-col justify-center">
      <div className="flex items-center gap-2">
        {showText && (
          <span className={`font-display font-extrabold text-3xl tracking-tighter leading-none ${color === 'white' ? 'text-white' : 'text-primary'}`}>
            unie
          </span>
        )}
        <div className="w-8 h-8 relative">
          <svg viewBox="0 0 100 100" className="w-full h-full" fill={color}>
            <g transform="translate(50,50)">
              {[0, 60, 120, 180, 240, 300].map(angle => (
                <rect 
                  key={angle} 
                  x="4" 
                  y="-45" 
                  width="14" 
                  height="42" 
                  transform={`rotate(${angle})`} 
                />
              ))}
            </g>
          </svg>
        </div>
      </div>
      {showText && (
        <span className={`text-[10px] font-bold tracking-[0.1em] leading-none mt-1 ${color === 'white' ? 'text-white/80' : 'text-primary/70'}`}>
          Universidad
        </span>
      )}
    </div>
  </div>
);

const PriorityBadge = ({ priority }: { priority: string }) => {
  const colors = {
    low: 'bg-emerald-50 text-emerald-700 border-emerald-100',
    medium: 'bg-blue-50 text-blue-700 border-blue-100',
    high: 'bg-amber-50 text-amber-700 border-amber-100',
    urgent: 'bg-rose-50 text-rose-700 border-rose-100',
  };
  return (
    <span className={`px-2.5 py-0.5 border rounded-full text-[10px] font-semibold uppercase tracking-wide ${colors[priority as keyof typeof colors]}`}>
      {priority === 'low' ? 'BAJA' : priority === 'medium' ? 'MEDIA' : priority === 'high' ? 'ALTA' : 'URGENTE'}
    </span>
  );
};

const StatusIcon = ({ status }: { status: string }) => {
  switch (status) {
    case 'open': return <AlertCircle className="w-4 h-4 text-red-500" />;
    case 'in_progress': return <Clock className="w-4 h-4 text-yellow-500" />;
    case 'resolved': return <CheckCircle2 className="w-4 h-4 text-green-500" />;
    default: return <CheckCircle2 className="w-4 h-4 text-gray-500" />;
  }
};

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState<string | null>(null);
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [activeTab, setActiveTab] = useState('dashboard');
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showResolvedHistory, setShowResolvedHistory] = useState(false);
  const [newIncident, setNewIncident] = useState({
    title: '',
    description: '',
    category: 'Infraestructura',
    location: ''
  });
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [incidentDetails, setIncidentDetails] = useState<any>(null);
  const [commentText, setCommentText] = useState('');

  const fetchIncidentDetails = async (id: number) => {
    const res = await fetch(`/api/incidents/${id}`);
    setIncidentDetails(await res.json());
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim() || !selectedIncident) return;
    await fetch(`/api/incidents/${selectedIncident.id}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: commentText })
    });
    setCommentText('');
    fetchIncidentDetails(selectedIncident.id);
  };

  const updateStatus = async (id: number, status: string) => {
    await fetch(`/api/incidents/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    fetchData();
    fetchIncidentDetails(id);
  };

  const fetchData = async () => {
    const [incRes, statsRes] = await Promise.all([
      fetch('/api/incidents'),
      fetch('/api/stats')
    ]);
    const incidentsData = await incRes.json();
    const statsData = await statsRes.json();
    
    // Enriquecer stats con KPIs calculados para el prototipo
    const enrichedStats = {
      ...statsData,
      avgResolutionTime: 12.5,
      slaCompliance: 94,
      resolutionTrend: [
        { date: 'Lun', opened: 12, resolved: 8 },
        { date: 'Mar', opened: 15, resolved: 14 },
        { date: 'Mie', opened: 8, resolved: 10 },
        { date: 'Jue', opened: 20, resolved: 18 },
        { date: 'Vie', opened: 10, resolved: 12 },
      ]
    };
    
    setIncidents(incidentsData);
    setStats(enrichedStats);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const analyzePriority = async (title: string, description: string): Promise<'low' | 'medium' | 'high' | 'urgent'> => {
    try {
      const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || '' });
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: `Analiza la siguiente incidencia universitaria y determina su nivel de prioridad. 
        Responde ÚNICAMENTE con una de estas palabras: low, medium, high, urgent.
        
        Criterios:
        - urgent: Peligro inmediato, fallos críticos de infraestructura o seguridad, problemas graves de matrícula en periodo de cierre.
        - high: Problemas que impiden el desarrollo normal de las clases o el trabajo administrativo.
        - medium: Problemas que afectan la comodidad o el funcionamiento pero tienen alternativas.
        - low: Mejoras estéticas, sugerencias o problemas menores sin impacto inmediato.
        
        Incidencia:
        Título: ${title}
        Descripción: ${description}`,
      });
      
      const result = response.text?.trim().toLowerCase();
      if (['low', 'medium', 'high', 'urgent'].includes(result || '')) {
        return result as 'low' | 'medium' | 'high' | 'urgent';
      }
      return 'medium';
    } catch (error) {
      console.error("Error analizando prioridad:", error);
      return 'medium';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    
    // Analizar prioridad automáticamente
    const priority = await analyzePriority(newIncident.title, newIncident.description);
    
    await fetch('/api/incidents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newIncident, priority })
    });
    
    setIsAnalyzing(false);
    setIsModalOpen(false);
    setNewIncident({ title: '', description: '', category: 'Infraestructura', location: '' });
    fetchData();
  };

  const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    const { email, password } = loginData;
    
    const users = [
      { email: 'alumno@unie.com', pass: 'alumno', role: 'Alumno' },
      { email: 'docente@unie.com', pass: 'docente', role: 'Docente' },
      { email: 'admin@unie.com', pass: 'admin', role: 'Admin' },
      { email: 'tecnico@unie.com', pass: 'tecnico', role: 'Tecnico' },
    ];

    const user = users.find(u => u.email === email && u.pass === password);

    if (user) {
      setUserRole(user.role);
      setIsLoggedIn(true);
      setLoginError(null);
      // Set default tab based on role
      if (user.role === 'Alumno') {
        setActiveTab('incidents');
      } else {
        setActiveTab('dashboard');
      }
    } else {
      setLoginError('Credenciales no válidas. Por favor, inténtelo de nuevo.');
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 font-sans">
        <div className="max-w-6xl w-full grid grid-cols-1 lg:grid-cols-2 bg-white rounded-[40px] shadow-2xl overflow-hidden border border-slate-100">
          {/* Left Side: Visual/Branding */}
          <div className="relative hidden lg:block overflow-hidden">
            <img 
              src="https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=800&q=80" 
              alt="Campus UNIE" 
              className="absolute inset-0 w-full h-full object-cover"
              referrerPolicy="no-referrer"
            />
            {/* Decorative Asterisk */}
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 100, repeat: Infinity, ease: "linear" }}
              className="absolute -left-40 -top-40 opacity-10 pointer-events-none"
            >
              <svg width="800" height="800" viewBox="0 0 100 100" fill="white">
                <g transform="translate(50,50)">
                  {[0, 60, 120, 180, 240, 300].map(angle => (
                    <rect 
                      key={angle} 
                      x="2" 
                      y="-42" 
                      width="16" 
                      height="40" 
                      transform={`rotate(${angle})`} 
                    />
                  ))}
                </g>
              </svg>
            </motion.div>
            <div className="absolute inset-0 bg-primary/80 backdrop-blur-[2px] flex flex-col justify-end p-16">
              <div className="mb-8">
                <UnieLogo className="h-16" color="white" />
              </div>
              <h1 className="text-5xl font-display font-extrabold text-white mb-6 leading-tight">
                Tu futuro <br />comienza aquí.
              </h1>
              <p className="text-white/70 text-lg font-medium max-w-md">
                Accede al portal oficial de gestión académica de UNIE Universidad.
              </p>
            </div>
          </div>

          {/* Right Side: Login Form */}
          <div className="p-12 lg:p-24 flex flex-col justify-center">
            <div className="mb-12">
              <h2 className="text-3xl font-display font-bold text-primary mb-3">Bienvenido de nuevo</h2>
              <p className="text-slate-400 font-medium">Por favor, introduce tus credenciales para acceder.</p>
            </div>

            <form onSubmit={handleLogin} className="space-y-6">
              {loginError && (
                <div className="bg-rose-50 border border-rose-100 text-rose-600 px-4 py-3 rounded-xl text-sm font-semibold flex items-center gap-3 animate-shake">
                  <AlertCircle size={18} />
                  {loginError}
                </div>
              )}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Correo Institucional</label>
                <input 
                  required
                  type="email" 
                  value={loginData.email}
                  onChange={e => setLoginData({...loginData, email: e.target.value})}
                  className="input-corporate w-full py-4 px-6 text-base"
                  placeholder="usuario@unie.com"
                />
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Contraseña</label>
                  <button type="button" className="text-[10px] font-bold text-primary uppercase tracking-widest hover:underline">¿Olvidaste tu contraseña?</button>
                </div>
                <input 
                  required
                  type="password" 
                  value={loginData.password}
                  onChange={e => setLoginData({...loginData, password: e.target.value})}
                  className="input-corporate w-full py-4 px-6 text-base"
                  placeholder="••••••••"
                />
              </div>

              <div className="flex items-center gap-3 pt-2">
                <input type="checkbox" id="remember" className="w-4 h-4 rounded border-slate-300 text-primary focus:ring-primary" />
                <label htmlFor="remember" className="text-sm font-medium text-slate-600">Recordar sesión en este dispositivo</label>
              </div>

              <button 
                type="submit"
                className="btn-corporate w-full py-5 text-lg font-bold mt-4 shadow-xl shadow-primary/20"
              >
                Iniciar Sesión
              </button>
            </form>

            <div className="mt-12 pt-12 border-t border-slate-100 text-center">
              <p className="text-sm text-slate-400 font-medium">
                ¿Aún no tienes cuenta? <button className="text-primary font-bold hover:underline">Contacta con Secretaría</button>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const filteredIncidents = incidents.filter(incident => {
    // Filtrado por estado: Si showResolvedHistory es true, mostramos solo las resueltas/cerradas
    // Si es false, mostramos solo las activas (open/in_progress)
    const isActive = ['open', 'in_progress'].includes(incident.status);
    const isResolved = ['resolved', 'closed'].includes(incident.status);
    
    if (showResolvedHistory && !isResolved) return false;
    if (!showResolvedHistory && !isActive) return false;

    // Segundo: Filtrar por permisos de categoría según el rol
    if (userRole === 'Admin' || userRole === 'Tecnico') return true;
    if (userRole === 'Docente') return ['TI / Tecnología', 'Mobiliario', 'Infraestructura', 'Gestión Académica', 'Otros'].includes(incident.category);
    if (userRole === 'Alumno') return ['Limpieza', 'Mobiliario', 'Gestión Académica', 'Secretaría / Matrícula', 'Otros'].includes(incident.category);
    return false;
  });

  const canCreateIncident = userRole !== 'Tecnico'; // Tecnicos resolve, others report
  const canChangeStatus = userRole === 'Admin' || userRole === 'Tecnico';
  const canViewStats = userRole === 'Admin' || userRole === 'Tecnico' || userRole === 'Docente';

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex p-0">
      {/* Sidebar */}
      <aside className="w-20 lg:w-64 bg-primary flex flex-col shadow-xl z-20">
        <div className="p-8 flex justify-center lg:justify-start items-center">
          <UnieLogo className="h-8 lg:h-10" color="white" showText={true} />
        </div>

        <nav className="flex-1 px-4 space-y-2">
          {[
            { id: 'dashboard', icon: LayoutDashboard, label: 'Panel de Control', roles: ['Admin', 'Tecnico', 'Docente'] },
            { id: 'incidents', icon: ListFilter, label: 'Registro Central', roles: ['Admin', 'Tecnico', 'Docente', 'Alumno'] },
            { id: 'settings', icon: Settings, label: 'Configuración', roles: ['Admin'] },
          ].filter(item => item.roles.includes(userRole || '')).map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-4 px-4 py-3.5 rounded-xl transition-all duration-200 group relative ${
                activeTab === item.id 
                  ? 'bg-white/10 text-white shadow-inner' 
                  : 'text-white/60 hover:bg-white/5 hover:text-white'
              }`}
            >
              <item.icon size={20} className={activeTab === item.id ? 'text-white' : 'text-white/40 group-hover:text-white/80'} />
              <span className="hidden lg:block font-semibold text-sm">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="p-6 mt-auto">
          <div className="bg-white/5 rounded-2xl p-4 flex items-center gap-3 border border-white/10">
            <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-white/20 bg-white/10 flex items-center justify-center">
              <span className="text-white font-bold text-xs">{userRole?.charAt(0)}</span>
            </div>
            <div className="hidden lg:block">
              <p className="text-xs font-bold text-white">{userRole}</p>
              <p className="text-[10px] text-white/40">Portal UNIE</p>
            </div>
          </div>
          <button 
            onClick={() => { setIsLoggedIn(false); setUserRole(null); }}
            className="w-full mt-4 py-2 text-[10px] font-bold text-white/40 hover:text-white uppercase tracking-widest transition-colors"
          >
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-20 bg-white border-b border-slate-200 px-10 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center gap-8 flex-1">
            <div className="hidden md:block">
              <h2 className="text-lg font-display font-bold text-primary leading-tight">
                {activeTab === 'dashboard' ? 'Panel Académico' : activeTab === 'incidents' ? 'Registro de Incidencias' : 'Configuración'}
              </h2>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="text-[9px] font-bold text-primary/60 uppercase tracking-widest bg-primary/5 px-2 py-0.5 rounded-md border border-primary/10">
                  Acceso: {userRole}
                </span>
              </div>
            </div>
            
            <div className="relative max-w-md w-full">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input 
                type="text" 
                placeholder="Buscar en el campus..." 
                className="w-full bg-slate-100 border-none rounded-full py-2.5 pl-12 pr-4 text-sm focus:ring-2 focus:ring-primary/10 transition-all outline-none"
              />
            </div>
          </div>

          <div className="flex items-center gap-6">
            {canCreateIncident && (
              <button 
                onClick={() => setIsModalOpen(true)}
                className="btn-corporate flex items-center gap-2"
              >
                <PlusCircle size={18} />
                <span>Nueva Entrada</span>
              </button>
            )}
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && canViewStats && (
              <motion.div 
                key="dashboard"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-10"
              >
                {/* Hero Section Placeholder */}
                <div className="relative h-64 rounded-3xl overflow-hidden shadow-2xl group">
                  <img 
                    src="https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1200&q=80" 
                    alt="Campus" 
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                    referrerPolicy="no-referrer"
                  />
                  <div className="absolute inset-0 bg-gradient-to-r from-primary/80 to-transparent flex items-center px-12">
                    <div className="max-w-md">
                      <h3 className="text-3xl font-display font-extrabold text-white mb-4 leading-tight">
                        Excelencia Académica y Liderazgo Tecnológico
                      </h3>
                      <p className="text-white/80 text-sm font-medium">
                        Gestionando el futuro de nuestra comunidad universitaria con herramientas de vanguardia.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  {[
                    { label: 'Total Campus', value: stats?.total.count || 0, color: 'text-primary', bg: 'bg-blue-50' },
                    { label: 'Operaciones Pendientes', value: stats?.open.count || 0, color: 'text-amber-600', bg: 'bg-amber-50' },
                    { label: 'Tiempo Medio Resol.', value: `${stats?.avgResolutionTime || 0}h`, color: 'text-indigo-600', bg: 'bg-indigo-50' },
                    { label: 'Cumplimiento SLA', value: `${stats?.slaCompliance || 0}%`, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                  ].map((stat, i) => (
                    <div key={i} className="card-corporate p-6 flex flex-col items-center text-center group">
                      <div className={`w-10 h-10 ${stat.bg} rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                        <BarChart3 className={stat.color} size={20} />
                      </div>
                      <h3 className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mb-1">{stat.label}</h3>
                      <p className={`text-3xl font-display font-extrabold ${stat.color}`}>{stat.value}</p>
                    </div>
                  ))}
                </div>

                {/* Charts Section */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <div className="lg:col-span-2 card-corporate p-8">
                    <div className="flex items-center justify-between mb-8">
                      <div>
                        <h3 className="text-lg font-display font-bold text-primary">Tendencia de Resolución</h3>
                        <p className="text-xs text-slate-400 font-medium">Comparativa de incidencias abiertas vs resueltas</p>
                      </div>
                    </div>
                    <div className="h-72">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={stats?.resolutionTrend || []}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                          <XAxis 
                            dataKey="date" 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{ fill: '#64748b', fontSize: 11, fontWeight: 500 }} 
                          />
                          <YAxis 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{ fill: '#64748b', fontSize: 11, fontWeight: 500 }} 
                          />
                          <Tooltip 
                            cursor={{ fill: '#f8fafc' }}
                            contentStyle={{ backgroundColor: '#fff', borderRadius: '12px', border: '1px solid #e2e8f0' }}
                          />
                          <Bar dataKey="opened" name="Abiertas" fill="#cbd5e1" radius={[4, 4, 0, 0]} />
                          <Bar dataKey="resolved" name="Resueltas" fill="#10b981" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="card-corporate p-8 flex flex-col">
                    <h3 className="text-lg font-display font-bold text-primary mb-8">Prioridad y SLA</h3>
                    <div className="flex-1 space-y-6">
                      {[
                        { label: 'Urgente', count: 5, color: 'bg-rose-500' },
                        { label: 'Alta', count: 12, color: 'bg-amber-500' },
                        { label: 'Media', count: 25, color: 'bg-blue-500' },
                        { label: 'Baja', count: 10, color: 'bg-emerald-500' },
                      ].map((item, i) => (
                        <div key={i}>
                          <div className="flex justify-between text-[10px] font-bold mb-2 uppercase tracking-wider">
                            <span className="text-slate-500">{item.label}</span>
                            <span className="text-primary">{item.count}</span>
                          </div>
                          <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                            <motion.div 
                              initial={{ width: 0 }}
                              animate={{ width: `${(item.count / 52) * 100}%` }}
                              className={`h-full ${item.color} rounded-full`} 
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="mt-8 pt-6 border-t border-slate-100 flex justify-between items-center">
                      <div>
                        <p className="text-2xl font-display font-extrabold text-emerald-600">94%</p>
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">SLA Cumplido</p>
                      </div>
                      <div className="w-10 h-10 bg-emerald-50 rounded-full flex items-center justify-center text-emerald-600">
                        <CheckCircle2 size={20} />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Partners Section */}
                <div className="pt-10 border-t border-slate-200">
                  <p className="text-center text-[10px] font-bold text-slate-400 uppercase tracking-[0.3em] mb-8">Nuestros Partners Estratégicos</p>
                  <div className="flex flex-wrap justify-center items-center gap-12 opacity-30 grayscale hover:grayscale-0 transition-all duration-500">
                    {['Google', 'Microsoft', 'Amazon', 'IBM', 'Oracle'].map(partner => (
                      <div key={partner} className="text-xl font-display font-black tracking-tighter text-slate-900">{partner}</div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'incidents' && (
              <motion.div 
                key="incidents"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="card-corporate overflow-hidden"
              >
                <div className="p-8 border-b border-slate-100 flex items-center justify-between bg-white">
                  <div>
                    <h3 className="text-xl font-display font-bold text-primary">
                      {showResolvedHistory ? 'Historial de Incidencias' : 'Registro de Incidencias Activas'}
                    </h3>
                    <p className="text-xs text-slate-400 font-medium mt-1">
                      {showResolvedHistory ? 'Consulta de eventos ya resueltos y cerrados' : 'Historial completo de eventos académicos y técnicos pendientes'}
                    </p>
                  </div>
                  <div className="flex gap-4">
                    <button 
                      onClick={() => setShowResolvedHistory(!showResolvedHistory)}
                      className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all border ${
                        showResolvedHistory 
                          ? 'bg-primary text-white border-primary' 
                          : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50'
                      }`}
                    >
                      {showResolvedHistory ? 'Ver Activas' : 'Ver Historial'}
                    </button>
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
                      <input 
                        type="text" 
                        placeholder="Filtrar registros..." 
                        className="bg-slate-50 border border-slate-200 rounded-xl py-2 pl-10 pr-4 text-sm focus:ring-2 focus:ring-primary/10 transition-all outline-none w-64"
                      />
                    </div>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="bg-slate-50/50 border-b border-slate-100">
                        <th className="px-8 py-5 text-[11px] font-bold text-slate-500 uppercase tracking-wider">Asunto</th>
                        <th className="px-8 py-5 text-[11px] font-bold text-slate-500 uppercase tracking-wider">Estado</th>
                        <th className="px-8 py-5 text-[11px] font-bold text-slate-500 uppercase tracking-wider">Prioridad</th>
                        <th className="px-8 py-5 text-[11px] font-bold text-slate-500 uppercase tracking-wider">Ubicación</th>
                        <th className="px-8 py-5 text-[11px] font-bold text-slate-500 uppercase tracking-wider">Fecha</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-50">
                      {filteredIncidents.map((incident) => (
                        <tr 
                          key={incident.id} 
                          onClick={() => {
                            setSelectedIncident(incident);
                            fetchIncidentDetails(incident.id);
                          }}
                          className="hover:bg-slate-50/80 transition-all group cursor-pointer"
                        >
                          <td className="px-8 py-6">
                            <div>
                              <p className="font-bold text-slate-900 text-sm group-hover:text-primary transition-colors">{incident.title}</p>
                              <p className="text-xs text-slate-400 font-medium truncate max-w-[250px] mt-1">{incident.description}</p>
                            </div>
                          </td>
                          <td className="px-8 py-6">
                            <div className="flex items-center gap-2.5">
                              <StatusIcon status={incident.status} />
                              <span className="text-xs font-semibold text-slate-600 capitalize">{incident.status.replace('_', ' ')}</span>
                            </div>
                          </td>
                          <td className="px-8 py-6">
                            <PriorityBadge priority={incident.priority} />
                          </td>
                          <td className="px-8 py-6">
                            <div className="flex items-center gap-2 text-slate-500 text-xs font-medium">
                              <MapPin size={14} className="text-slate-300" />
                              {incident.location}
                            </div>
                          </td>
                          <td className="px-8 py-6 text-xs font-medium text-slate-400">
                            {format(new Date(incident.created_at), 'dd MMM, yyyy', { locale: es })}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </motion.div>
            )}
            {activeTab === 'settings' && userRole === 'Admin' && (
              <motion.div 
                key="settings"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-8"
              >
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Perfil y Cuenta */}
                  <div className="lg:col-span-1 space-y-6">
                    <div className="card-corporate p-8">
                      <h3 className="text-lg font-display font-bold text-primary mb-6">Perfil de Administrador</h3>
                      <div className="flex flex-col items-center text-center">
                        <div className="w-24 h-24 rounded-full overflow-hidden border-4 border-slate-50 shadow-lg mb-4">
                          <img src="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=200&q=80" alt="Admin" referrerPolicy="no-referrer" />
                        </div>
                        <h4 className="font-bold text-slate-900">Admin UNIE</h4>
                        <p className="text-xs text-slate-400 font-medium uppercase tracking-widest mt-1">Superusuario</p>
                        <button className="mt-6 w-full py-2.5 bg-slate-50 text-slate-600 rounded-xl text-xs font-bold uppercase tracking-widest hover:bg-slate-100 transition-colors">
                          Editar Perfil
                        </button>
                      </div>
                    </div>

                    <div className="card-corporate p-8">
                      <h3 className="text-sm font-display font-bold text-primary mb-4 uppercase tracking-wider">Preferencias del Sistema</h3>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-semibold text-slate-600">Análisis IA Prioridad</span>
                          <div className="w-10 h-5 bg-emerald-500 rounded-full relative cursor-pointer">
                            <div className="absolute right-1 top-1 w-3 h-3 bg-white rounded-full" />
                          </div>
                        </div>
                        <div className="flex items-center justify-between opacity-50">
                          <span className="text-xs font-semibold text-slate-600">Notificaciones Email</span>
                          <div className="w-10 h-5 bg-slate-200 rounded-full relative cursor-not-allowed">
                            <div className="absolute left-1 top-1 w-3 h-3 bg-white rounded-full" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Gestión de Usuarios y Campus */}
                  <div className="lg:col-span-2 space-y-8">
                    <div className="card-corporate p-8">
                      <div className="flex items-center justify-between mb-8">
                        <h3 className="text-lg font-display font-bold text-primary">Gestión de Usuarios</h3>
                        <button className="text-xs font-bold text-primary uppercase tracking-widest bg-primary/5 px-4 py-2 rounded-lg hover:bg-primary/10 transition-colors">
                          Añadir Usuario
                        </button>
                      </div>
                      <div className="space-y-4">
                        {[
                          { name: 'Dr. García', email: 'docente@unie.com', role: 'Docente', status: 'Activo' },
                          { name: 'Marta Pérez', email: 'alumno@unie.com', role: 'Alumno', status: 'Activo' },
                          { name: 'Juan Técnico', email: 'tecnico@unie.com', role: 'Tecnico', status: 'Activo' },
                        ].map((user, i) => (
                          <div key={i} className="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-slate-100">
                            <div className="flex items-center gap-4">
                              <div className="w-10 h-10 rounded-full overflow-hidden bg-primary/10 flex items-center justify-center border border-primary/20">
                                <span className="text-primary font-bold text-xs">{user.name.charAt(0)}</span>
                              </div>
                              <div>
                                <p className="text-sm font-bold text-slate-900">{user.name}</p>
                                <p className="text-[10px] text-slate-400 font-medium">{user.email}</p>
                              </div>
                            </div>
                            <div className="flex items-center gap-6">
                              <span className="text-[10px] font-bold text-primary uppercase tracking-widest bg-white px-3 py-1 rounded-full border border-slate-100 shadow-sm">
                                {user.role}
                              </span>
                              <button className="text-slate-400 hover:text-primary transition-colors">
                                <Settings size={16} />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="card-corporate p-8">
                      <h3 className="text-lg font-display font-bold text-primary mb-6">Ubicaciones del Campus</h3>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {['Edificio A', 'Edificio B', 'Laboratorios', 'Biblioteca', 'Cafetería', 'Zonas Deportivas'].map((loc, i) => (
                          <div key={i} className="p-4 bg-white border border-slate-100 rounded-2xl text-center shadow-sm hover:border-primary/20 transition-all cursor-pointer group">
                            <p className="text-xs font-bold text-slate-600 group-hover:text-primary">{loc}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Footer */}
        <footer className="h-12 bg-white border-t border-slate-200 px-10 flex items-center justify-between">
          <div className="flex gap-8">
          </div>
          <div className="text-[10px] font-bold text-slate-300 uppercase tracking-[0.2em]">
            © 2026 UNIE Universidad - Portal de Gestión Académica
          </div>
        </footer>
      </main>

      {/* Modal Nueva Incidencia */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
            />
            <motion.div 
              initial={{ opacity: 0, scale: 0.95, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 10 }}
              className="relative bg-white w-full max-w-lg rounded-3xl shadow-2xl overflow-hidden border border-slate-100"
            >
              <div className="p-10">
                <div className="mb-8">
                  <h2 className="text-2xl font-display font-bold text-primary">Nueva Entrada</h2>
                  <p className="text-sm text-slate-400 font-medium mt-1">Complete los detalles para registrar un nuevo evento en el campus.</p>
                </div>
                
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Asunto</label>
                    <input 
                      required
                      type="text" 
                      value={newIncident.title}
                      onChange={e => setNewIncident({...newIncident, title: e.target.value})}
                      className="input-corporate w-full"
                      placeholder="Ej: Mantenimiento Laboratorio 3"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Categoría</label>
                    <select 
                      value={newIncident.category}
                      onChange={e => setNewIncident({...newIncident, category: e.target.value})}
                      className="input-corporate w-full cursor-pointer"
                    >
                      {userRole === 'Alumno' ? (
                        <>
                          <option>Gestión Académica</option>
                          <option>Secretaría / Matrícula</option>
                          <option>Limpieza</option>
                          <option>Mobiliario</option>
                          <option>Otros</option>
                        </>
                      ) : userRole === 'Docente' ? (
                        <>
                          <option>Gestión Académica</option>
                          <option>TI / Tecnología</option>
                          <option>Mobiliario</option>
                          <option>Infraestructura</option>
                          <option>Otros</option>
                        </>
                      ) : (
                        <>
                          <option>Infraestructura</option>
                          <option>TI / Tecnología</option>
                          <option>Gestión Académica</option>
                          <option>Secretaría / Matrícula</option>
                          <option>Mobiliario</option>
                          <option>Limpieza</option>
                          <option>Seguridad</option>
                          <option>Otros</option>
                        </>
                      )}
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Ubicación</label>
                    <input 
                      required
                      type="text" 
                      value={newIncident.location}
                      onChange={e => setNewIncident({...newIncident, location: e.target.value})}
                      className="input-corporate w-full"
                      placeholder="Ej: Edificio A, Planta 2"
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">Descripción Detallada</label>
                    <textarea 
                      required
                      rows={3}
                      value={newIncident.description}
                      onChange={e => setNewIncident({...newIncident, description: e.target.value})}
                      className="input-corporate w-full resize-none"
                      placeholder="Describa el suceso con detalle..."
                    />
                  </div>

                  <div className="flex gap-4 pt-4">
                    <button 
                      type="button"
                      onClick={() => setIsModalOpen(false)}
                      className="flex-1 px-6 py-3 text-sm font-bold text-slate-400 hover:text-slate-600 transition-colors uppercase tracking-widest"
                    >
                      Cancelar
                    </button>
                    <button 
                      type="submit"
                      disabled={isAnalyzing}
                      className="btn-corporate flex-1 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {isAnalyzing ? (
                        <>
                          <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          Analizando...
                        </>
                      ) : 'Registrar Evento'}
                    </button>
                  </div>
                </form>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
      {/* Modal Detalle Incidencia */}
      <AnimatePresence>
        {selectedIncident && (
          <div className="fixed inset-0 z-50 flex items-center justify-end">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedIncident(null)}
              className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
            />
            <motion.div 
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 30, stiffness: 300 }}
              className="relative bg-white w-full max-w-2xl h-full shadow-2xl flex flex-col border-l border-slate-100"
            >
              {incidentDetails ? (
                <>
                  <div className="p-10 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                    <div>
                      <div className="flex items-center gap-3 mb-3">
                        <PriorityBadge priority={incidentDetails.priority} />
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Registro #{incidentDetails.id}</span>
                      </div>
                      <h2 className="text-2xl font-display font-bold text-primary leading-tight">{incidentDetails.title}</h2>
                    </div>
                    <button 
                      onClick={() => setSelectedIncident(null)}
                      className="w-12 h-12 flex items-center justify-center rounded-full hover:bg-slate-200 transition-all text-slate-400 hover:text-primary"
                    >
                      <PlusCircle className="rotate-45" size={24} />
                    </button>
                  </div>

                  <div className="flex-1 overflow-y-auto p-10 space-y-12">
                    <section>
                      <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Descripción del Evento</h4>
                      <p className="text-slate-600 leading-relaxed bg-white p-8 rounded-2xl border border-slate-100 shadow-sm text-sm font-medium">
                        {incidentDetails.description}
                      </p>
                    </section>

                    <div className="grid grid-cols-2 gap-8">
                      <section className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Ubicación</h4>
                        <div className="flex items-center gap-3 text-primary font-bold">
                          <MapPin size={18} className="text-primary/40" />
                          <span className="text-sm">{incidentDetails.location}</span>
                        </div>
                      </section>
                      <section className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                        <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Estado Actual</h4>
                        {canChangeStatus ? (
                          <select 
                            value={incidentDetails.status}
                            onChange={(e) => updateStatus(incidentDetails.id, e.target.value)}
                            className="input-corporate w-full py-1.5 text-xs font-bold uppercase"
                          >
                            <option value="open">Abierto</option>
                            <option value="in_progress">En Progreso</option>
                            <option value="resolved">Resuelto</option>
                            <option value="closed">Cerrado</option>
                          </select>
                        ) : (
                          <div className="flex items-center gap-2.5">
                            <StatusIcon status={incidentDetails.status} />
                            <span className="text-xs font-bold text-primary uppercase">{incidentDetails.status.replace('_', ' ')}</span>
                          </div>
                        )}
                      </section>
                    </div>

                    <section className="pt-10 border-t border-slate-100">
                      <div className="flex items-center justify-between mb-8">
                        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Historial de Actividad</h4>
                        <span className="px-3 py-1 bg-slate-100 rounded-full text-[10px] font-bold text-slate-500 uppercase tracking-widest">{incidentDetails.comments?.length || 0} Entradas</span>
                      </div>
                      
                      <div className="space-y-8 mb-10">
                        {incidentDetails.comments?.map((comment: any) => (
                          <div key={comment.id} className="flex gap-5 group">
                            <div className="w-10 h-10 rounded-full flex-shrink-0 overflow-hidden border-2 border-slate-100 shadow-sm bg-slate-50 flex items-center justify-center">
                              <span className="text-primary font-bold text-xs">{comment.user_name.charAt(0)}</span>
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-sm font-bold text-slate-700">{comment.user_name}</span>
                                <span className="text-[10px] font-bold text-slate-300 uppercase">{format(new Date(comment.created_at), 'HH:mm')}</span>
                              </div>
                              <div className="text-sm text-slate-500 bg-slate-50/50 p-5 rounded-2xl border border-slate-100 italic">
                                "{comment.text}"
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>

                      <form onSubmit={handleAddComment} className="relative group">
                        <textarea 
                          value={commentText}
                          onChange={(e) => setCommentText(e.target.value)}
                          placeholder="Añadir comentario al registro..."
                          className="input-corporate w-full pr-16 min-h-[120px] resize-none text-sm"
                          rows={3}
                        />
                        <button 
                          type="submit"
                          className="absolute bottom-4 right-4 w-12 h-12 bg-primary text-white rounded-xl hover:bg-accent transition-all flex items-center justify-center shadow-lg active:scale-95"
                        >
                          <PlusCircle size={24} />
                        </button>
                      </form>
                    </section>
                  </div>
                </>
              ) : (
                <div className="flex-1 flex items-center justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                </div>
              )}
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

